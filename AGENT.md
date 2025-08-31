# Multi-Agent Assistant Architecture

This document outlines the architecture, conventions, and procedures for the multi-agent assistant project. The system is built on a Supervisor-Worker model, where each agent is a distinct, containerized microservice communicating via the Agent-to-Agent (A2A) protocol.

-----

## **CRITICAL GUIDELINES - MUST READ FIRST**

### USE EXISTING CODE - DO NOT REINVENT

**The codebase in `src/` already contains COMPLETE IMPLEMENTATIONS of:**

-**LangGraph base classes** (`base/base_graph_agent.py`, `base/base_graph_state.py`)
-**A2A Server utilities** (`a2a_integration/a2a_lg_server_utils.py`)
-**A2A Client utilities** (`a2a_integration/a2a_lg_client_utils.py`)
-**Agent implementations** (`agents/supervisor/`, `agents/planner/`)
-**Error handling** (`base/error_handling.py`)
-**Authentication** (`a2a_integration/auth/`)

**MANDATORY RULES:**

1. **ALWAYS use existing implementations** - Do NOT create new base classes or utilities from scratch
2. **EXTEND existing code** - Inherit from `BaseGraphAgent`, use `A2AClientManager`, leverage existing utilities
3. **NEVER reinvent the wheel** - If similar functionality exists, adapt and extend it rather than creating new
4. **BUILD UPON the foundation** - The codebase is production-ready; use it as designed

### DOCUMENTATION-FIRST APPROACH

**ALWAYS consult documentation before implementation:**

- Check `docs/` directory for official documentation and guides
- Follow established patterns from the planning documents
- Reference `planning/plan.md` for architectural decisions
- Use documented APIs and interfaces exactly as specified

**DO NOT:**

-Make assumptions about how things should work
-Create alternative implementations when official ones exist
-Deviate from documented patterns without explicit requirement
-Ignore existing code structure and conventions

### Example: Creating a New Agent

**CORRECT APPROACH:**

```python
# Using existing base classes and utilities
from src.base.base_graph_agent import BaseGraphAgent
from src.a2a_integration.a2a_lg_server_utils import build_a2a_starlette_application

class MyNewAgent(BaseGraphAgent):
    def init_nodes(self, graph):
        # Implement using existing patterns
        pass
    
    def init_edges(self, graph):
        # Follow established conventions
        pass
```

**Remember: The goal is to COMPOSE and CONFIGURE existing components, NOT to create new ones!**

## Documentation Guidelines

### Documentation Writing Rules

**Important: Please follow these rules when writing all documents and code comments:**

1. **No Emoji Usage** - Emojis are prohibited in all text including documents, code comments, and commit messages
2. **Use Clear Text** - Use clear text expressions instead of emojis
   - Bad examples: "✅ Done", "⚠️ Warning", "🚀 Start", "💡 Tip"
   - Good examples: "[Done]", "[Warning]", "DONE", "WARNING", "[Start]", "[Tip]"
3. **Professional Documentation** - Maintain professionalism and readability in technical documentation

## Project Overview

FastCampus Workflow Automation Multi-Agent System - A multi-agent workflow automation system built on LangGraph and the Agent-to-Agent (A2A) protocol. The system follows a Supervisor-Worker model where each agent is a distinct, containerized microservice.

### Core Components

- **Supervisor Agent**: Orchestrates the entire workflow by executing plans from the Planner. Acts as the primary A2A client to coordinate worker agents.
- **Planner Agent**: Decomposes complex user requests into structured, step-by-step JSON plans without executing tasks.
  > The output plan **must** be a JSON object containing a list of steps.
  > Each step must contain: `step_number` (integer), `agent_to_use` (string), and `prompt` (string).
- **Browser Agent**: Executes web-based tasks (searching, clicking, data entry) via containerized Playwright MCP server.
- **Knowledge Agent**: Performs RAG (Retrieval-Augmented Generation) against local knowledge base using FAISS index.
- **Data Collector/Analysis/Trading Agents**: Specialized worker agents for specific domains.

### Architecture Philosophy

The architecture emphasizes **Modularity** and **Specialization**:

- Each agent has a single, well-defined responsibility
- All agents are containerized microservices
- Communication via standardized A2A protocol (JSON-RPC 2.0)
- Independent development, testing, and deployment of components

## Project Setup & Dependencies

The project uses `uv` for high-performance Python package management. All dependencies are defined in `pyproject.toml`.

- **Python Version**: `>=3.12,<3.13`
- **Core Dependencies**: `langgraph==0.6.6`, `langchain-mcp-adapters==0.1.9`, `a2a-sdk[http-server]==0.3.3`, `langchain-openai`, `uvicorn`
- **Development Tools**: `ruff>=0.12.10` for linting and formatting, `pytest>=8.4.1` for testing

## Common Development Tasks

### Environment Setup & Dependency Management

```bash
# Install dependencies from uv.lock file (creates/updates lock file automatically)
uv sync

# Install including development dependencies
uv sync --dev

# Add new package
uv add [package-name]

# Add development package
uv add --dev [package-name]
```

### Running Agents

```bash
# Set Python path (required)
export PYTHONPATH="${PWD}/src"

# Run Supervisor Agent
uv run python -m agents.supervisor

# Run Planner Agent  
uv run python -m agents.planner

# Run specific agent as A2A server
uv run python src/agents/supervisor/supervisor_agent_a2a.py
```

### Code Quality Management

```bash
# Linting with Ruff
uv run ruff check src/

# Auto-formatting with Ruff
uv run ruff format src/

# Auto-fix lint errors
uv run ruff check src/ --fix
```

### Testing

```bash
# Run pytest (install if needed: uv add --dev pytest)
uv run pytest

# Run specific test file
uv run pytest tests/test_[module].py

# Run tests with coverage
uv run pytest --cov=src tests/
```

## Architecture & Structure

### Core Module Structure

```text
src/
├── base/                      # Base abstract classes and common utilities
│   ├── base_graph_agent.py   # LangGraph agent abstract base class
│   ├── base_graph_state.py   # State management base class
│   ├── a2a_interface.py      # A2A protocol interface
│   └── error_handling.py     # Unified error handling
│
├── a2a_integration/           # A2A protocol integration utilities
│   ├── a2a_lg_client_utils.py # A2A client manager
│   ├── a2a_lg_server_utils.py # A2A server builder utilities
│   ├── models.py              # A2A data models
│   └── auth/                  # Authentication related
│
├── agents/                    # Agent implementations
│   ├── supervisor/            # Supervisor agent
│   │   └── supervisor_agent_a2a.py
│   ├── planner/              # Planner agent
│   │   ├── planner_agent_a2a.py
│   │   └── planner_agent_lg.py
│   └── prompts.py            # Agent prompt templates
│
└── mcp/                      # MCP (Model Context Protocol) integration
```

### Agent Architecture Patterns

1. **BaseGraphAgent Inheritance Pattern**
   - All LangGraph agents inherit from `BaseGraphAgent`
   - Must implement `init_nodes()` and `init_edges()` methods
   - State defined using TypedDict

2. **A2A Server Pattern**
   - Implement `AgentExecutor` interface
   - Execute agent logic in `execute()` method
   - Define agent spec with `get_agent_card()` method
   - Wrap with Starlette application for HTTP endpoints

3. **Workflow Orchestration Pattern**
   - Supervisor determines workflow pattern (DATA_ONLY, DATA_ANALYSIS, FULL_WORKFLOW)
   - State tracking via TaskManager
   - Call sub-agents using A2AClientManager

### Inter-Agent Communication

```python
# Agent invocation via A2A client
a2a_client_manager = A2AClientManager(
    base_url="http://agent-url:8000",
    streaming=False
)
client = await a2a_client_manager.initialize()
result = await client.send_data({"messages": [{"role": "user", "content": "query"}]})
```

### MCP Server Integration

```python
# MCP tools initialization pattern
from langchain_mcp_adapters.client import MultiServerMCPClient

mcp_servers = [
    {"name": "playwright", "url": "http://playwright-mcp:8931/mcp"}
]
# BaseGraphAgent automatically initializes and integrates MCP tools
```

### Agent Discovery

Each agent must expose an `AgentCard` at `/.well-known/agent-card.json` to declare its capabilities and endpoints for A2A protocol discovery.

## Key Development Patterns

### 1. Agent State Management

- Explicit state schema definition using TypedDict
- State update methods specified with Annotated types
- Message history management with add_messages reducer

### 2. Error Handling

- Use `AgentExecutionError` custom exception
- Structured error handling with context information
- Track errors by updating Task state to failed

### 3. Asynchronous Initialization

- lazy_init pattern for async operations like MCP server connections
- Async factory pattern implementation with `create()` class method

### 4. Environment-specific Configuration

- Distinguish Docker/local environments with IS_DOCKER environment variable
- Dynamic agent URL configuration per environment

## Testing Strategy

### Unit Testing

- Test individual node functions of each agent
- Isolate external dependencies using mocks

### Integration Testing

- Test A2A communication between agents
- Verify complete workflow execution

### End-to-End Testing

- Run entire system with Docker Compose
- Test based on real-world scenarios

## Docker & Services

All agents and supporting services run as Docker containers, orchestrated by Docker Compose.

### Service Architecture

- **Service Network**: All services communicate over a shared bridge network named `a2a-network`
- **Container Naming**: Services resolve each other by container name (e.g., `http://planner-agent:8000`)
- **Playwright MCP**: Browser automation runs as a dedicated service with `ipc: host` for stability
- **Agent Dockerfiles**: Each agent has its own Dockerfile
  > The `Dockerfile.knowledge_agent` copies local knowledge source and pre-built vector index into the container

### Docker Configuration

```yaml
# docker-compose.yml example structure
services:
  supervisor-agent:
    build: .
    environment:
      - IS_DOCKER=true
      - PYTHONPATH=/app/src
    ports:
      - "8000:8000"
    networks:
      - a2a-network

  playwright-mcp:
    image: mcr.microsoft.com/playwright/mcp:latest
    container_name: playwright-mcp-server
    command: ["--port", "8931"]
    ports:
      - "8931:8931"
    ipc: host  # Recommended to prevent Chromium memory crashes
    networks:
      - a2a-network

networks:
  a2a-network:
    driver: bridge
```

### Building and Running

```bash
# Build and run the entire multi-agent system
docker-compose -f docker-compose-full.yml up --build

# Run in detached mode
docker-compose -f docker-compose-full.yml up -d --build

# View logs
docker-compose logs -f [service-name]

# Stop all services
docker-compose down
```

## Important Conventions

### 1. Logging

- Structured logging using `structlog`
- Agent-specific logger namespaces
- Log levels: INFO for normal operations, ERROR for failures

### 2. Type Hinting

- Type hints required for all functions/methods
- Complex dictionary structures defined with TypedDict
- Use Union types for flexible inputs

### 3. Constant Management

- Node names managed as class attribute NODE_NAMES
- Minimize magic string usage
- Define workflow patterns as constants

### 4. Asynchronous Programming

- Use async/await pattern for all I/O operations
- Consider concurrency in design
- Proper exception handling in async contexts

## Environment Variables

### Required Variables

- `PYTHONPATH`: Path to src directory (required: `${PWD}/src`)
- `OPENAI_API_KEY`: OpenAI API key for LLM usage
- `IS_DOCKER`: Docker environment flag ("true"/"false")
- `AGENT_HOST`: Agent server host (default: "localhost" or "0.0.0.0" in Docker)
- `AGENT_PORT`: Agent server port (default: "8000")

### A2A Agent URLs (for Supervisor)

- `DATA_COLLECTOR_URL`: Data collector agent URL
- `ANALYSIS_URL`: Analysis agent URL  
- `TRADING_URL`: Trading agent URL
- `PLANNER_URL`: Planner agent URL (if used)
- `BROWSER_URL`: Browser agent URL (if used)
- `KNOWLEDGE_URL`: Knowledge agent URL (if used)

## Debugging & Monitoring

### 1. LangGraph Debugging

```python
# Enable graph execution logging with debug mode
agent = BaseGraphAgent(is_debug=True)

# Visualize graph structure
graph = agent.build_graph()
print(graph.get_graph().draw_mermaid())
```

### 2. A2A Communication Debugging

- Use `a2a-inspector` tool for message flow visualization
- Check agent capabilities at `/.well-known/agent-card.json` endpoint
- Monitor JSON-RPC requests/responses

### 3. State Tracking

- Utilize TaskManager's metadata field
- Track progress with `workflow_phase`, `current_step`
- Monitor task states: submitted → working → completed/failed

### 4. Performance Monitoring

```bash
# Monitor container resources
docker stats

# Check container logs
docker logs -f [container-name]

# Inspect running processes
docker exec [container-name] ps aux
```

## Troubleshooting Guide

### Common Issues

1. **MCP Connection Failures**
   - Ensure MCP server is running: `docker ps | grep mcp`
   - Check network connectivity: `docker network inspect a2a-network`
   - Verify URL configuration in mcp_servers list

2. **Agent Communication Errors**
   - Verify A2A endpoints are accessible
   - Check CORS configuration if browser-based
   - Ensure proper JSON-RPC message format

3. **Memory/Performance Issues**
   - Use `ipc: host` for browser automation containers
   - Set appropriate resource limits in docker-compose
   - Monitor with `docker stats`

4. **Task State Issues**
   - Check TaskManager initialization
   - Verify metadata updates in workflow execution
   - Ensure proper error handling updates task state

-----

## Related Documentation

### Project Structure Documentation

- [**Source Code Architecture**](./src/AGENT.md) - Core implementation and agent components and so on.
- [**Technical Documentation**](./docs/AGENT.md) - Technical documentation and API specifications
- [**Service - Deploy Docker Configuration**](./docker/AGENT.md) - Containerization and deployment settings
- [**Service - A2A Inspector Tool**](./a2a-inspector/AGENT.md) - Agent-to-Agent communication debugging tool
