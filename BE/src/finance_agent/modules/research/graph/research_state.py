from typing import Annotated, Sequence, TypedDict, List, Dict, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
import operator

class SearchResult(TypedDict):
    """Tavily search result format"""
    query: str
    answer: str
    sources: List[Dict[str, str]]
    status: str
    error: str

class ResearchState(TypedDict):
    """LangGraph state for research workflow"""
    
    # === Messages (LangGraph standard) ===
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    # === Query Tracking ===
    original_query: str          # User's initial query
    current_query: str           # Current iteration query
    iteration_count: int         # Human-in-loop counter
    
    # === Reviewer Outputs ===
    is_valid: bool               # Query validation result
    validation_message: str      # Feedback for user
    refined_queries: Annotated[List[str], operator.add]  # Sub-queries
    
    # === Search Results ===
    search_results: Annotated[List[SearchResult], operator.add]  # Tavily responses
    
    # === Final Output ===
    final_report: str            # Aggregated report
    
    # === Metadata ===
    conversation_id: str         # UUID
    timestamp: str               # ISO timestamp
    
    # === Flow Control ===
    next_step: str               # Routing: "reviewer", "search", etc.
