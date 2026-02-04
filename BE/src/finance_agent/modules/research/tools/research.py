"""Research Tools - Tavily Search integration"""

import json
import os
from langchain_core.tools import tool
from tavily import TavilyClient
from finance_agent.core.config import Settings
from finance_agent.shared.logger import setup_logger

logger = setup_logger(__name__)
settings = Settings()

@tool
def research(query: str) -> str:
    """
    Search for financial information using Tavily API.
    Use this tool for stock analysis, market trends, financial news, and company info.
    """
    logger.info(f"Executing Tavily search for: {query}")
    
    api_key = settings.tavily_api_key
    if not api_key:
        logger.error("TAVILY_API_KEY not found in settings")
        return json.dumps({"error": "API key missing", "answer": "", "sources": []})
        
    try:
        client = TavilyClient(api_key=api_key)
        # We use qna search for a summarized answer + sources
        response = client.search(query, search_depth="advanced", max_results=5)
        
        # Format results
        results = {
            "answer": response.get("answer", "No direct answer found."),
            "sources": [
                {
                    "title": r.get("title", "No Title"),
                    "url": r.get("url", ""),
                    "content": r.get("content", "")
                } for r in response.get("results", [])
            ]
        }
        
        return json.dumps(results)
    except Exception as e:
        logger.error(f"Tavily search failed: {e}")
        return json.dumps({"error": str(e), "answer": "", "sources": []})