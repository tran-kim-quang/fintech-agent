"""Research Workflow - LangGraph assembly"""

from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from finance_agent.modules.research.graph.research_state import ResearchState
from finance_agent.modules.research.graph.research_nodes.orchestrator import orchestrator_node
from finance_agent.modules.research.graph.research_nodes.reviewer import reviewer_node
from finance_agent.modules.research.graph.research_nodes.search import search_node
from finance_agent.modules.research.graph.research_nodes.aggregator import aggregator_node
from finance_agent.modules.research.graph.research_nodes.memory import memory_node
from finance_agent.modules.research.graph.research_nodes.ask_user import ask_user_node
from finance_agent.shared.logger import setup_logger

logger = setup_logger(__name__)

def route_from_orchestrator(state: ResearchState) -> str:
    """Route from orchestrator based on next_step"""
    return state.get("next_step", "reviewer")

def route_from_reviewer(state: ResearchState) -> str:
    """Route from reviewer based on validation"""
    if state.get("is_valid"):
        return "search"
    else:
        return "ask_user"

def create_research_workflow():
    """Create and compile the research workflow graph"""
    logger.info("Creating research workflow graph...")
    
    # Initialize graph
    workflow = StateGraph(ResearchState)
    
    # Add nodes
    workflow.add_node("orchestrator", orchestrator_node)
    workflow.add_node("reviewer", reviewer_node)
    workflow.add_node("search", search_node)
    workflow.add_node("aggregator", aggregator_node)
    workflow.add_node("memory", memory_node)
    workflow.add_node("ask_user", ask_user_node)
    
    # Add edges
    workflow.add_edge(START, "orchestrator")
    
    workflow.add_conditional_edges(
        "orchestrator",
        route_from_orchestrator,
        {
            "reviewer": "reviewer",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "reviewer",
        route_from_reviewer,
        {
            "search": "search",
            "ask_user": "ask_user"
        }
    )
    
    workflow.add_edge("ask_user", "orchestrator")
    workflow.add_edge("search", "aggregator")
    workflow.add_edge("aggregator", "memory")
    workflow.add_edge("memory", END)
    
    # Add checkpointer and interrupt
    memory = MemorySaver()
    
    # Compile
    app = workflow.compile(
        checkpointer=memory,
        interrupt_before=["ask_user"]
    )
    
    logger.info("Research workflow created successfully")
    return app
