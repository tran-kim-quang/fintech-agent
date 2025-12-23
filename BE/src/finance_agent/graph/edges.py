"""Logic điều hướng (Conditional edges) trong LangGraph"""

from finance_agent.graph.state import AgentState
from finance_agent.utils.logger import setup_logger

logger = setup_logger(__name__)


def route_next_action(state: AgentState) -> str:
    """Điều hướng dựa trên next_action trong state"""
    next_action = state.get("next_action", "end")
    
    logger.info(f"Routing to: {next_action}")
    
    return next_action


def should_continue(state: AgentState) -> str:
    """Quyết định có tiếp tục workflow không"""
    messages = state.get("messages", [])
    
    # Logic kiểm tra xem có cần tiếp tục không
    if len(messages) > 10:
        return "end"
    
    return "continue"
