"""Lắp ráp và compile LangGraph workflow"""

from langgraph.graph import StateGraph, END
from finance_agent.graph.state import AgentState
from finance_agent.graph.nodes import (
    process_input_node,
    analyze_node,
    execute_tools_node,
    generate_response_node
)
from finance_agent.graph.edges import route_next_action
from finance_agent.utils.logger import setup_logger

logger = setup_logger(__name__)


def create_workflow():
    """Tạo và compile workflow graph"""
    logger.info("Creating workflow graph...")
    
    # Khởi tạo graph
    workflow = StateGraph(AgentState)
    
    # Thêm nodes
    workflow.add_node("process_input", process_input_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("execute_tools", execute_tools_node)
    workflow.add_node("generate_response", generate_response_node)
    
    # Định nghĩa entry point
    workflow.set_entry_point("process_input")
    
    # Thêm edges
    workflow.add_conditional_edges(
        "process_input",
        route_next_action,
        {
            "analyze": "analyze",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "analyze",
        route_next_action,
        {
            "execute_tools": "execute_tools",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "execute_tools",
        route_next_action,
        {
            "generate_response": "generate_response",
            "end": END
        }
    )
    
    workflow.add_edge("generate_response", END)
    
    # Compile graph
    compiled_workflow = workflow.compile()
    
    logger.info("Workflow graph created successfully")
    
    return compiled_workflow
