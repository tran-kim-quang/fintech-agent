"""Các Node (hàm xử lý) trong LangGraph"""

from typing import Dict, Any
from finance_agent.graph.state import AgentState
from finance_agent.utils.logger import setup_logger

logger = setup_logger(__name__)


def process_input_node(state: AgentState) -> Dict[str, Any]:
    """Node xử lý input từ user"""
    logger.info("Processing user input...")
    
    # TODO: Implement input processing logic
    
    return {
        "next_action": "analyze"
    }


def analyze_node(state: AgentState) -> Dict[str, Any]:
    """Node phân tích yêu cầu"""
    logger.info("Analyzing request...")
    
    # TODO: Implement analysis logic
    
    return {
        "next_action": "execute_tools"
    }


def execute_tools_node(state: AgentState) -> Dict[str, Any]:
    """Node thực thi các tools"""
    logger.info("Executing tools...")
    
    # TODO: Implement tool execution logic
    
    return {
        "tool_results": {},
        "next_action": "generate_response"
    }


def generate_response_node(state: AgentState) -> Dict[str, Any]:
    """Node tạo response cho user"""
    logger.info("Generating response...")
    
    # TODO: Implement response generation logic
    
    return {
        "next_action": "end"
    }
