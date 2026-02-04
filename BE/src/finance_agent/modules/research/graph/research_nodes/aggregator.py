"""Aggregator Node - LLM synthesis of multiple search results"""

from finance_agent.modules.research.graph.research_state import ResearchState
from finance_agent.shared.logger import setup_logger
from finance_agent.core.config import Settings
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

logger = setup_logger(__name__)
settings = Settings()


# System prompt cho Aggregator
AGGREGATOR_SYSTEM_PROMPT = """You are a Financial Research Report Synthesizer.

Your task: Create a comprehensive, well-structured report based on multiple search results.

Guidelines:
1. **Synthesize information** - Don't just list results, combine insights
2. **Cite sources** - Reference URLs for claims
3. **Structure clearly** - Use markdown headers, bullets
4. **Be objective** - Present facts, mention conflicts if any
5. **Vietnamese preferred** - Unless sources are English-only

Format:
# [Report Title]

## Tóm tắt
[Brief overview answering original query]

## Phân tích Chi tiết
[Key findings from searches, synthesized]

## Nguồn Tham khảo
[List of sources with links]

## Kết luận
[Summary and insights]
"""


def format_sources(sources: list[dict]) -> str:
    """Format sources for context including snippets"""
    if not sources:
        return "No sources available."
    
    formatted = []
    for i, src in enumerate(sources[:5], 1):  # Limit to 5 sources
        title = src.get("title", "Unknown")
        url = src.get("url", "")
        content = src.get("content", "No content available.")
        # Limit content length per source to avoid context overflow
        snippet = content[:500] + "..." if len(content) > 500 else content
        formatted.append(f"{i}. [{title}]({url})\n   Snippet: {snippet}")
    
    return "\n".join(formatted)


def aggregator_node(state: ResearchState) -> dict:
    """
    Aggregator - Synthesize multiple search results
    """
    logger.info("=== Aggregator Node ===")
    
    search_results = state.get("search_results", [])
    original_query = state.get("original_query", "")
    
    if not search_results:
        logger.warning("No search results to aggregate")
        return {
            "final_report": "Không có kết quả tìm kiếm để tổng hợp.",
            "next_step": "memory"
        }
    
    logger.info(f"Aggregating {len(search_results)} search results")
    
    # Prepare context from search results
    context_parts = []
    for idx, result in enumerate(search_results, 1):
        if result.get("status") == "success":
            context_parts.append(f"""
## Search Query {idx}: {result['query']}

**Tavily AI Answer:** {result.get('answer', 'N/A')}

**Detailed Search Results:**
{format_sources(result.get('sources', []))}
""")
        else:
            context_parts.append(f"""
## Search Query {idx}: {result['query']}
**Status:** Failed - {result.get('error', 'Unknown error')}
""")
    
    context = "\n".join(context_parts)
    
    # Initialize LLM from settings
    try:
        llm = ChatOllama(model=settings.model_name, temperature=0.3)
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        # Fallback: Return raw search results
        return {
            "final_report": f"# Kết quả Tìm kiếm\n\n{context}",
            "next_step": "memory"
        }
    
    # Create messages
    messages = [
        SystemMessage(content=AGGREGATOR_SYSTEM_PROMPT),
        HumanMessage(content=f"""Original User Query: {original_query}

Search Results:
{context}

Please create a comprehensive research report in Vietnamese.""")
    ]
    
    # Call LLM
    try:
        response = llm.invoke(messages)
        final_report = response.content
        logger.info("Report generated successfully")
    except Exception as e:
        logger.error(f"LLM synthesis failed: {e}")
        # Fallback: Basic aggregation
        final_report = f"""# Báo cáo Nghiên cứu: {original_query}

## Kết quả Tìm kiếm

{context}

---
*Lưu ý: Không thể tổng hợp tự động. Đây là kết quả thô từ tìm kiếm.*
"""
    
    return {
        "final_report": final_report,
        "next_step": "memory"
    }
