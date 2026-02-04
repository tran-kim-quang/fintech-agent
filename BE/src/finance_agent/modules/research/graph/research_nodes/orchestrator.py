"""Orchestrator Node - LLM-based intelligent agent routing"""

from finance_agent.modules.research.graph.research_state import ResearchState
from finance_agent.shared.logger import setup_logger
from finance_agent.core.config import Settings
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from datetime import datetime
import uuid
import json

logger = setup_logger(__name__)
settings = Settings()


# System prompt for LLM Orchestrator
ORCHESTRATOR_SYSTEM_PROMPT = """You are an intelligent agent orchestrator for a fintech research system.

Your job: Analyze user queries and route to the appropriate agent(s).

**Available Agents:**

1. **research** - Financial research and analysis
   - Stock analysis, price data
   - Financial news search
   - Company information
   - Market trends
   - Crypto/forex data
   Example queries: "Giá vàng hôm nay", "Phân tích VNM", "Bitcoin price"

2. **chart** - Data visualization
   - Create charts and graphs
   - Technical analysis charts
   - Price trend visualization
   Example queries: "Vẽ biểu đồ VNM", "Chart BTC price"

3. **evaluation** - Report quality assessment
   - Evaluate research reports
   - Quality scoring
   - Fact-checking
   Example queries: "Đánh giá báo cáo", "Review report quality"

4. **sentiment** - News sentiment analysis
   - Analyze news sentiment
   - Market mood detection
   Example queries: "Sentiment về VNM", "Market mood"

**Decision Rules:**
- For CURRENT version: Always route to **research** agent (others not implemented yet)
- For FUTURE: Can route to multiple agents in sequence
- If query is unclear: route to research with note to refine

**Output Format (JSON only):**
{
  "primary_agent": "research",
  "agent_pipeline": ["research"],
  "reasoning": "Brief explanation of routing decision",
  "requires_refinement": false
}

**Examples:**

Query: "Giá vàng hôm nay"
Output: {"primary_agent": "research", "agent_pipeline": ["research"], "reasoning": "Financial price query, route to research agent", "requires_refinement": false}

Query: "Phân tích VNM và vẽ chart"
Output: {"primary_agent": "research", "agent_pipeline": ["research"], "reasoning": "Research query. Chart agent not yet available.", "requires_refinement": false}

Query: "Hello"
Output: {"primary_agent": "research", "agent_pipeline": ["research"], "reasoning": "Unclear query, route to research for validation", "requires_refinement": true}

Always respond with valid JSON only. No additional text.
"""


def orchestrator_node(state: ResearchState) -> dict:
    """
    LLM-based Orchestrator - intelligent agent routing
    """
    logger.info("=== LLM Orchestrator Node ===")
    
    # Lần đầu tiên chạy: Initialize
    if not state.get("conversation_id"):
        logger.info("Initializing new conversation")
        conversation_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        original_query = state.get("current_query", "")
        
        # Initialize và route
        routing = _route_with_llm(original_query)
        
        return {
            "conversation_id": conversation_id,
            "timestamp": timestamp,
            "original_query": original_query,
            "iteration_count": 0,
            "next_step": routing["primary_agent"]
        }
    
    # Human-in-loop: User đã trả lời, increment iteration
    messages = state.get("messages", [])
    if messages and messages[-1].type == "human":
        logger.info(f"Human-in-loop iteration {state.get('iteration_count', 0) + 1}")
        new_query = messages[-1].content
        
        # Re-route với query mới
        routing = _route_with_llm(new_query)
        
        return {
            "current_query": new_query,
            "iteration_count": state.get("iteration_count", 0) + 1,
            "next_step": routing["primary_agent"]
        }
    
    # Default: Route với current query
    current_query = state.get("current_query", "")
    routing = _route_with_llm(current_query)
    
    logger.info(f"Routing to: {routing['primary_agent']}")
    return {"next_step": routing["primary_agent"]}


def _route_with_llm(query: str) -> dict:
    """
    Use Qwen LLM to determine intelligent routing
    """
    logger.info(f"LLM routing for query: {query}")
    
    # Fallback default
    default_routing = {
        "primary_agent": "reviewer",
        "agent_pipeline": ["reviewer"],
        "reasoning": "Default routing to research workflow",
        "requires_refinement": False
    }
    
    try:
        # Initialize LLM from settings
        llm = ChatOllama(model=settings.model_name, temperature=0)
        
        # Create messages
        messages = [
            SystemMessage(content=ORCHESTRATOR_SYSTEM_PROMPT),
            HumanMessage(content=f"User query: {query}")
        ]
        
        # Call LLM
        response = llm.invoke(messages)
        logger.info(f"LLM routing response: {response.content}")
        
        # Parse JSON
        routing = json.loads(response.content)
        
        # Validate structure
        if not all(key in routing for key in ["primary_agent", "agent_pipeline", "reasoning"]):
            logger.warning("Invalid routing structure from LLM, using default")
            return default_routing
        
        # Map agent names to actual workflow nodes
        agent_mapping = {
            "research": "reviewer",
            "chart": "chart",
            "evaluation": "eval",
            "sentiment": "sentiment"
        }
        
        primary = routing["primary_agent"]
        mapped_agent = agent_mapping.get(primary, "reviewer")
        
        logger.info(f"Routing decision: {primary} → {mapped_agent}")
        
        return {
            "primary_agent": mapped_agent,
            "agent_pipeline": routing.get("agent_pipeline", [mapped_agent]),
            "reasoning": routing.get("reasoning", ""),
            "requires_refinement": routing.get("requires_refinement", False)
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM routing response: {e}")
        return default_routing
    except Exception as e:
        logger.error(f"LLM routing failed: {e}")
        return default_routing
