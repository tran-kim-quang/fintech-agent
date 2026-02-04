from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

from finance_agent.modules.research.graph.research_workflow import create_research_workflow
from finance_agent.shared.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

# Initialize research workflow
research_graph = create_research_workflow()

class QueryRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None

class QueryResponse(BaseModel):
    conversation_id: str
    status: str
    next_step: str
    final_report: Optional[str] = None
    validation_message: Optional[str] = None

@router.post("/", response_model=QueryResponse)
async def run_research(request: QueryRequest):
    """
    Run the research agent workflow
    """
    logger.info(f"Received research request: {request.query}")
    
    config = {"configurable": {"thread_id": request.conversation_id or str(uuid.uuid4())}}
    
    initial_state = {
        "current_query": request.query,
        "original_query": request.query,
        "iteration_count": 0
    }
    
    try:
        result = research_graph.invoke(initial_state, config=config)
        
        return QueryResponse(
            conversation_id=config["configurable"]["thread_id"],
            status="completed" if result.get("next_step") == "end" else "interrupted",
            next_step=result.get("next_step"),
            final_report=result.get("final_report"),
            validation_message=result.get("validation_message")
        )
    except Exception as e:
        logger.error(f"Research workflow failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
