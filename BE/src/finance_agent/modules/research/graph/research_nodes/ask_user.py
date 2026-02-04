"""Ask User Node - Human-in-the-loop clarification"""

from finance_agent.modules.research.graph.research_state import ResearchState
from finance_agent.shared.logger import setup_logger
from langchain_core.messages import AIMessage

logger = setup_logger(__name__)

def ask_user_node(state: ResearchState) -> dict:
    """
    Ask User Node - Interrupt workflow to get clarification from user
    """
    logger.info("=== Ask User Node ===")
    
    validation_message = state.get("validation_message", "Cần thêm thông tin về yêu cầu của bạn.")
    iteration = state.get("iteration_count", 0)
    
    clarification_msg = f"""🤔 {validation_message}

Vui lòng cung cấp query liên quan đến:
- Cổ phiếu, chứng khoán
- Tiền điện tử (crypto)
- Tài chính, kinh tế, đầu tư
- Phân tích công ty, báo cáo tài chính

(Lần hỏi lại: {iteration + 1})
"""
    
    message = AIMessage(content=clarification_msg)
    
    return {
        "messages": [message],
        "next_step": "wait_user"
    }
