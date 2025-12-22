# fintech-agent

```
finance-agent/
├── .github/                 # Cấu hình CI/CD (nếu có)
├── .vscode/                 # Cấu hình Editor (nếu dùng VS Code)
├── src/
│   └── finance_agent/       # Package chính của dự án
│       ├── __init__.py
│       ├── main.py          # Điểm khởi chạy (Entry point)
│       ├── config/          # Quản lý biến môi trường và cấu hình
│       │   ├── __init__.py
│       │   └── settings.py  # Dùng Pydantic BaseSettings
│       ├── graph/           # Cấu trúc cốt lõi của LangGraph
│       │   ├── __init__.py
│       │   ├── state.py     # Định nghĩa AgentState (TypedDict)
│       │   ├── nodes.py     # Các hàm xử lý (Nodes)
│       │   ├── edges.py     # Logic điều hướng (Conditional edges)
│       │   └── workflow.py  # Nơi lắp ráp Graph (Compile graph)
│       ├── mcp/             # Xử lý Model Context Protocol
│       │   ├── __init__.py
│       │   ├── client.py    # Client kết nối đến các MCP Server
│       │   └── converter.py # Chuyển đổi MCP Tools sang LangChain Tools
│       ├── tools/           # Các công cụ Local (nếu không dùng qua MCP)
│       │   ├── __init__.py
│       │   └── calculators.py
│       └── utils/           # Các hàm tiện ích chung (logging, formatting)
│           ├── __init__.py
│           └── logger.py
```
