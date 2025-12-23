"""Định nghĩa AgentState cho LangGraph"""

from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
import operator


class AgentState(TypedDict):
    """State của Agent trong workflow"""
    
    # Messages trong conversation
    messages: Annotated[Sequence[BaseMessage], operator.add]
    
    # Thông tin ngữ cảnh
    user_query: str
    
    # Kết quả từ các tools
    tool_results: dict
    
    # Trạng thái xử lý
    next_action: str
