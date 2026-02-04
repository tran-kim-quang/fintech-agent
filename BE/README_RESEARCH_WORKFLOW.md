# Research Workflow - Quick Start Guide

## Overview

The research workflow provides intelligent query processing with:
- ✅ Query validation and refinement (Qwen3 LLM)
- ✅ Automatic query decomposition
- ✅ Parallel Tavily search
- ✅ LLM-powered result synthesis
- ✅ Human-in-the-loop for invalid queries
- ✅ Conversation persistence

## Prerequisites

1. **Ollama** with Qwen model:
   ```bash
   ollama pull qwen2.5:3b
   ```

2. **Tavily API Key** in `.env`:
   ```
   TAVILY_API_KEY=your_key_here
   ```

3. **Python dependencies**:
   ```bash
   pip install langgraph langchain-ollama langchain-core tavily-python
   ```

## Running the CLI

```bash
cd BE/src/finance_agent
python test_research_cli.py
```

## Example Usage

### Example 1: Valid Query
```
Enter your query: Giá vàng hôm nay

Processing...
✓ Query validated
✓ Searching: "Giá vàng Việt Nam ngày 04/02/2026"
✓ Report generated

RESEARCH COMPLETE
================================================================================
# Báo cáo Giá Vàng

## Tóm tắt
...
```

### Example 2: Invalid Query (Human-in-Loop)
```
Enter your query: Làm bánh pizza

Processing...
--------------------------------------------------------------------------------
🤔 Query không liên quan đến tài chính. Vui lòng hỏi về cổ phiếu, crypto, kinh tế, hoặc đầu tư.

Vui lòng cung cấp query liên quan đến:
- Cổ phiếu, chứng khoán
- Tiền điện tử (crypto)
- Tài chính, kinh tế, đầu tư

(Lần hỏi lại: 1)
--------------------------------------------------------------------------------

Enter revised query: Giá Bitcoin

Processing...
✓ Query validated
✓ Searching...
```

### Example 3: Complex Query (Decomposition)
```
Enter your query: So sánh VNM và FPT

Processing...
✓ Query decomposed into 2 sub-queries
✓ Parallel search in progress...
  - "Phân tích cổ phiếu VNM 2026"
  - "Phân tích cổ phiếu FPT 2026"
✓ Synthesizing comparative report...

RESEARCH COMPLETE
================================================================================
# So sánh VNM và FPT
...
```

## Architecture

```
User Query → Orchestrator → Reviewer (Qwen LLM)
                                ↓
                    Valid? ──No→ Ask User → Loop
                      ↓ Yes
                    Search (Tavily, parallel)
                      ↓
                    Aggregator (Qwen LLM)
                      ↓
                    Memory (.txt file)
                      ↓
                    Final Report
```

## File Structure

```
BE/src/finance_agent/
├── graph/
│   ├── research_state.py          # State definitions
│   ├── research_workflow.py       # Graph assembly
│   └── research_nodes/
│       ├── orchestrator.py        # Entry point
│       ├── reviewer.py            # LLM validation
│       ├── search.py              # Tavily search
│       ├── aggregator.py          # LLM synthesis
│       ├── memory.py              # Persistence
│       └── ask_user.py            # Human-in-loop
├── tools/
│   └── research.py                # TavilySearch tool
└── test_research_cli.py           # CLI interface

conversations/                      # Saved conversations
└── [uuid]_[timestamp].txt
```

## Conversation Files

Conversations are saved to `conversations/` directory:

```
================================================================================
FINTECH RESEARCH CONVERSATION
ID: abc-123-def
Timestamp: 2026-02-04T12:00:00
================================================================================

## CONVERSATION HISTORY

[HUMAN]: Giá vàng hôm nay
[AI]: Query đã được refined...

================================================================================
## FINAL RESEARCH REPORT
================================================================================

[Full report content]

================================================================================
## METADATA
================================================================================
Original Query: Giá vàng hôm nay
Iterations: 0
Sub-queries: 1
Search Results: 1
```

## Troubleshooting

### LLM Connection Error
```
Error: Failed to initialize LLM
```
**Fix:** Ensure Ollama is running and qwen2.5:3b is pulled:
```bash
ollama serve
ollama pull qwen2.5:3b
```

### Tavily API Error
```
Error: Tavily API call failed
```
**Fix:** Check your API key in `.env`:
```bash
echo $TAVILY_API_KEY  # Should print your key
```

### Import Errors
```
ModuleNotFoundError: No module named 'langgraph'
```
**Fix:** Install dependencies:
```bash
pip install -r requirements.txt
```

## Next Steps

- [ ] Test with various queries
- [ ] Monitor conversation files
- [ ] Review LLM prompts for accuracy
- [ ] Add Redis caching (future enhancement)
- [ ] Migrate memory to database

## Documentation

Full design documentation: `BE/docs/research_workflow_design.md`
