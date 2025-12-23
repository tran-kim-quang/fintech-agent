"""Entry point cho Finance Agent"""

import asyncio
from finance_agent.config.settings import Settings
from finance_agent.graph.workflow import create_workflow
from finance_agent.utils.logger import setup_logger

logger = setup_logger(__name__)


async def main():
    """Khởi chạy Finance Agent"""
    settings = Settings()
    logger.info("Starting Finance Agent...")
    
    # Tạo workflow
    workflow = create_workflow()
    
    # TODO: Implement main logic
    logger.info("Finance Agent is running...")


if __name__ == "__main__":
    asyncio.run(main())
