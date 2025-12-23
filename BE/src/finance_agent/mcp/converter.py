"""Chuyển đổi MCP Tools sang LangChain Tools"""

from typing import List, Any
from langchain_core.tools import Tool
from finance_agent.utils.logger import setup_logger

logger = setup_logger(__name__)


def convert_mcp_to_langchain_tools(mcp_tools: List[dict]) -> List[Tool]:
    """
    Chuyển đổi MCP tools thành LangChain tools
    
    Args:
        mcp_tools: Danh sách tools từ MCP Server
        
    Returns:
        Danh sách LangChain Tools
    """
    logger.info(f"Converting {len(mcp_tools)} MCP tools to LangChain format...")
    
    langchain_tools = []
    
    for mcp_tool in mcp_tools:
        # TODO: Implement conversion logic
        tool = Tool(
            name=mcp_tool.get("name", "unknown"),
            description=mcp_tool.get("description", ""),
            func=lambda x: None  # Placeholder
        )
        langchain_tools.append(tool)
    
    logger.info(f"Converted {len(langchain_tools)} tools successfully")
    
    return langchain_tools
