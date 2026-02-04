"""Memory Node - Persist conversation to disk"""

from finance_agent.modules.research.graph.research_state import ResearchState
from finance_agent.shared.logger import setup_logger
import os
from datetime import datetime

logger = setup_logger(__name__)

def memory_node(state: ResearchState) -> dict:
    """
    Memory Node - Save conversation history and final report to a text file
    """
    logger.info("=== Memory Node ===")
    
    conversation_id = state.get("conversation_id", "unknown")
    timestamp = state.get("timestamp", datetime.now().isoformat()).replace(":", "-")
    storage_dir = "storage"
    
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)
        
    file_path = os.path.join(storage_dir, f"{conversation_id}_{timestamp}.txt")
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("="*80 + "\n")
            f.write("FINTECH RESEARCH CONVERSATION\n")
            f.write(f"ID: {conversation_id}\n")
            f.write(f"Timestamp: {state.get('timestamp')}\n")
            f.write("="*80 + "\n\n")
            
            f.write("## CONVERSATION HISTORY\n\n")
            for msg in state.get("messages", []):
                role = "HUMAN" if msg.type == "human" else "AI"
                f.write(f"[{role}]: {msg.content}\n")
            f.write("\n" + "="*80 + "\n")
            f.write("## FINAL RESEARCH REPORT\n")
            f.write("="*80 + "\n\n")
            f.write(state.get("final_report", "No report generated."))
            f.write("\n\n" + "="*80 + "\n")
            f.write("## METADATA\n")
            f.write("="*80 + "\n")
            f.write(f"Original Query: {state.get('original_query')}\n")
            f.write(f"Iterations: {state.get('iteration_count')}\n")
            f.write(f"Sub-queries: {len(state.get('refined_queries', []))}\n")
            f.write(f"Search Results: {len(state.get('search_results', []))}\n")
            
        logger.info(f"Saving conversation to {file_path}")
        logger.info("Conversation saved successfully")
        
        return {
            "memory_saved": True,
            "memory_path": file_path,
            "next_step": "end"
        }
    except Exception as e:
        logger.error(f"Failed to save conversation: {e}")
        return {
            "memory_saved": False,
            "next_step": "end"
        }
