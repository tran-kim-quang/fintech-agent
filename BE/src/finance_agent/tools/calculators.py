"""Các công cụ tính toán local"""

from langchain_core.tools import tool
from finance_agent.utils.logger import setup_logger

logger = setup_logger(__name__)


@tool
def calculator_tool(expression: str) -> str:
    """
    Tính toán các biểu thức toán học đơn giản
    
    Args:
        expression: Biểu thức toán học cần tính (vd: "2 + 2")
        
    Returns:
        Kết quả tính toán
    """
    logger.info(f"Calculating: {expression}")
    
    try:
        # Chỉ cho phép các phép toán an toàn
        allowed_chars = set("0123456789+-*/().")
        if not all(c in allowed_chars or c.isspace() for c in expression):
            return "Error: Invalid characters in expression"
        
        result = eval(expression)
        logger.info(f"Result: {result}")
        return str(result)
    
    except Exception as e:
        error_msg = f"Error calculating expression: {str(e)}"
        logger.error(error_msg)
        return error_msg


@tool
def compound_interest_calculator(
    principal: float,
    rate: float,
    time: float,
    n: int = 12
) -> str:
    """
    Tính lãi kép
    
    Args:
        principal: Số tiền gốc
        rate: Lãi suất hàng năm (%)
        time: Số năm
        n: Số kỳ lãi trong một năm (mặc định 12 - tính theo tháng)
        
    Returns:
        Số tiền cuối cùng sau khi tính lãi kép
    """
    logger.info(f"Calculating compound interest for principal={principal}, rate={rate}%, time={time} years")
    
    try:
        # A = P(1 + r/n)^(nt)
        rate_decimal = rate / 100
        amount = principal * (1 + rate_decimal / n) ** (n * time)
        interest = amount - principal
        
        result = f"Số tiền cuối: {amount:.2f}\nLãi: {interest:.2f}"
        logger.info(result)
        return result
    
    except Exception as e:
        error_msg = f"Error calculating compound interest: {str(e)}"
        logger.error(error_msg)
        return error_msg
