"""Logging configuration"""

import logging
import sys
from typing import Optional


def setup_logger(
    name: str,
    level: Optional[str] = None,
    log_format: Optional[str] = None
) -> logging.Logger:
    """
    Thiết lập logger với cấu hình
    
    Args:
        name: Tên của logger (thường là __name__)
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Format của log message
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Nếu logger đã có handlers, return ngay
    if logger.handlers:
        return logger
    
    # Set level
    log_level = getattr(logging, level or "INFO")
    logger.setLevel(log_level)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Create formatter
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    formatter = logging.Formatter(log_format)
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger
