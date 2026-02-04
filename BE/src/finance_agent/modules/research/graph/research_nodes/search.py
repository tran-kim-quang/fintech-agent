"""Search Node - LLM-driven tool execution with LangChain tool binding"""

from finance_agent.modules.research.graph.research_state import ResearchState, SearchResult
from finance_agent.shared.logger import setup_logger
from finance_agent.core.config import Settings
from finance_agent.modules.research.tools.research import research  # LangChain @tool
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import json

logger = setup_logger(__name__)
settings = Settings()


# System prompt for Search Agent
SEARCH_AGENT_PROMPT = """You are a financial research agent with access to a research tool.

Your job: Execute searches for ALL provided queries and collect comprehensive results.

**Available Tool:**
- research(query: str) -> str: Search for financial information using Tavily API

**Instructions:**
1. You will receive a list of refined queries
2. Execute the research tool for EACH query
3. Collect all results
4. Return results in structured format

**Important:**
- Execute ALL queries, don't skip any
- If a search fails, note the error but continue with other queries
- Be thorough and systematic

Always call the research tool for each query provided.
"""


def search_node(state: ResearchState) -> dict:
    """
    Search Node - LLM-driven tool execution
    """
    logger.info("=== Search Node (Tool Binding) ===")
    
    refined_queries = state.get("refined_queries", [])
    
    if not refined_queries:
        logger.warning("No refined queries to search")
        return {
            "search_results": [],
            "next_step": "aggregate"
        }
    
    logger.info(f"Executing searches for {len(refined_queries)} queries using LLM + tools")
    
    # Initialize LLM with tool binding
    try:
        llm = ChatOllama(model=settings.model_name, temperature=0)
        llm_with_tools = llm.bind_tools([research])
        
        # Create task message for LLM
        task_message = f"""Execute research for the following queries:

Queries to search:
{chr(10).join(f'{i+1}. {q}' for i, q in enumerate(refined_queries))}

Please call the research tool for each query and collect all results.
"""
        
        messages = [
            SystemMessage(content=SEARCH_AGENT_PROMPT),
            HumanMessage(content=task_message)
        ]
        
        # Invoke LLM - it will decide to call tools
        response = llm_with_tools.invoke(messages)
        
        logger.info(f"LLM response type: {type(response)}")
        logger.info(f"Tool calls: {response.tool_calls if hasattr(response, 'tool_calls') else 'None'}")
        
        # Execute tool calls if LLM decided to use tools
        search_results = []
        
        if hasattr(response, 'tool_calls') and response.tool_calls:
            logger.info(f"LLM requested {len(response.tool_calls)} tool calls")
            
            for tool_call in response.tool_calls:
                query = ""
                try:
                    # Extract query from tool call
                    query = tool_call.get('args', {}).get('query', '')
                    logger.info(f"Executing tool call for: {query}")
                    
                    # Execute research tool
                    result_json = research.invoke({"query": query})
                    result = json.loads(result_json)
                    
                    search_results.append({
                        "query": query,
                        "answer": result.get("answer", ""),
                        "sources": result.get("sources", []),
                        "status": "success",
                        "error": ""
                    })
                    
                except Exception as e:
                    logger.error(f"Tool execution failed for '{query}': {e}")
                    search_results.append({
                        "query": query,
                        "answer": "",
                        "sources": [],
                        "status": "failed",
                        "error": str(e)
                    })
        else:
            # Fallback: LLM didn't call tools, execute manually
            logger.warning("LLM didn't call tools, executing manually as fallback")
            search_results = _manual_search_fallback(refined_queries)
        
        # Log summary
        successful = sum(1 for r in search_results if r["status"] == "success")
        logger.info(f"Search complete: {successful}/{len(search_results)} successful")
        
        return {
            "search_results": search_results,
            "next_step": "aggregate"
        }
        
    except Exception as e:
        logger.error(f"Search node failed: {e}")
        # Fallback to manual execution
        logger.info("Falling back to manual search execution")
        search_results = _manual_search_fallback(refined_queries)
        
        return {
            "search_results": search_results,
            "next_step": "aggregate"
        }


def _manual_search_fallback(queries: list[str]) -> list[SearchResult]:
    """
    Fallback: Manual search execution if LLM tool binding fails
    """
    from concurrent.futures import ThreadPoolExecutor
    
    logger.info("Executing manual fallback search")
    
    def search_single(query: str) -> SearchResult:
        try:
            result_json = research.invoke({"query": query})
            result = json.loads(result_json)
            return {
                "query": query,
                "answer": result.get("answer", ""),
                "sources": result.get("sources", []),
                "status": "success",
                "error": ""
            }
        except Exception as e:
            logger.error(f"Manual search failed for '{query}': {e}")
            return {
                "query": query,
                "answer": "",
                "sources": [],
                "status": "failed",
                "error": str(e)
            }
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(search_single, queries))
    
    return results
