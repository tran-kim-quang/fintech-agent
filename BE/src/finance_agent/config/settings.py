"""Settings và cấu hình môi trường"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Quản lý biến môi trường và cấu hình"""
    
    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Application Settings
    app_name: str = "Finance Agent"
    debug: bool = False
    log_level: str = "INFO"
    
    # MCP Settings
    mcp_server_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
