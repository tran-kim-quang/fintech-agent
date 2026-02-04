"""Reviewer Node - Query validation, refinement, and decomposition using LLM"""

from finance_agent.modules.research.graph.research_state import ResearchState
from finance_agent.shared.logger import setup_logger
from finance_agent.core.config import Settings
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
import json

logger = setup_logger(__name__)
settings = Settings()


# System prompt cho Reviewer
REVIEWER_SYSTEM_PROMPT = """You are a Financial Query Reviewer for a fintech research agent.

Your tasks:
1. VALIDATE: Is this query related to finance, stocks, crypto, economics, or business?
   - If NO: Respond with validation advice for user
   - If YES: Proceed to refinement

2. REFINE: Improve the query for better search results:
   - Add context (dates, market, specifics)
   - Fix ambiguity
   - Optimize for financial search engines

3. DECOMPOSE: If query is complex, break into sub-queries:
   - "Compare VNM and FPT" → ["Analyze VNM stock", "Analyze FPT stock"]
   - "Gold price today" → ["Gold price Vietnam 04/02/2026"]

Output JSON:
{
  "is_valid": true/false,
  "message": "Feedback for user if invalid, or refinement explanation",
  "refined_queries": ["query1", "query2", ...]
}

Examples:

User: "Làm bánh pizza"
Output: {"is_valid": false, "message": "Query không liên quan đến tài chính. Vui lòng hỏi về cổ phiếu, crypto, kinh tế, hoặc đầu tư.", "refined_queries": []}

User: "VNM"
Output: {"is_valid": true, "message": "Refined query cho comprehensive analysis", "refined_queries": ["Phân tích cổ phiếu VNM giá và tin tức mới nhất 2026"]}

User: "So sánh VNM và FPT"
Output: {"is_valid": true, "message": "Decomposed into separate analyses", "refined_queries": ["Phân tích cổ phiếu VNM giá hiệu suất 2026", "Phân tích cổ phiếu FPT giá hiệu suất 2026"]}

User: "Giá vàng hôm nay"
Output: {"is_valid": true, "message": "Added date context for accuracy", "refined_queries": ["Giá vàng Việt Nam ngày hôm nay 2026"]}

Always respond with valid JSON only. No additional text.
"""


def reviewer_node(state: ResearchState) -> dict:
    """
    Reviewer - LLM validation & query refinement
    """
    logger.info("=== Reviewer Node ===")
    
    current_query = state.get("current_query", "")
    logger.info(f"Reviewing query: {current_query}")
    
    # Initialize LLM from settings
    try:
        llm = ChatOllama(model=settings.model_name, temperature=0)
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        return {
            "is_valid": False,
            "validation_message": "Lỗi hệ thống. Vui lòng thử lại sau.",
            "refined_queries": [],
            "next_step": "ask_user"
        }
    
    from datetime import datetime
    current_date = datetime.now().strftime("%d/%m/%Y")
    
    # Create messages
    messages = [
        SystemMessage(content=REVIEWER_SYSTEM_PROMPT),
        HumanMessage(content=f"Current Date: {current_date}\nUser query: {current_query}")
    ]
    
    # Call LLM
    try:
        response = llm.invoke(messages)
        logger.info(f"LLM response: {response.content}")
        
        # Parse JSON response
        result = json.loads(response.content)
        
        # Validate response structure
        if not all(key in result for key in ["is_valid", "message", "refined_queries"]):
            raise ValueError("Invalid response structure")
            
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM response as JSON: {e}")
        # Fallback: Assume invalid
        result = {
            "is_valid": False,
            "message": "Không thể xử lý query. Vui lòng diễn đạt rõ ràng hơn về tài chính, cổ phiếu, hoặc crypto.",
            "refined_queries": []
        }
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        result = {
            "is_valid": False,
            "message": "Lỗi xử lý query. Vui lòng thử lại.",
            "refined_queries": []
        }
    
    # Log result
    logger.info(f"Validation: {result['is_valid']}")
    logger.info(f"Refined queries: {result['refined_queries']}")
    
    # Return state updates
    return {
        "is_valid": result["is_valid"],
        "validation_message": result["message"],
        "refined_queries": result["refined_queries"],
        "next_step": "search" if result["is_valid"] else "ask_user"
    }
