"""Main entry point for Finance Agent API"""

from fastapi import FastAPI
from finance_agent.shared.logger import setup_logger
from finance_agent.core.config import Settings
from finance_agent.api.v1.research import router as research_router_v1

logger = setup_logger(__name__)
settings = Settings()

app = FastAPI(
    title=settings.app_name,
    description="Fintech Research Agent API",
    version="1.0.0"
)

# Root endpoint
@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.app_name} API", "status": "online"}

# Include routers
app.include_router(research_router_v1, prefix="/api/v1/research", tags=["Research"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
