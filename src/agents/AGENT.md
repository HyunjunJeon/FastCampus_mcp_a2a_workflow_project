# Agent Implementations

## Overview

This directory contains the concrete implementations of all agents in the multi-agent workflow automation system. Each agent follows a standardized architecture pattern and implements both LangGraph and A2A protocol interfaces.

## Agent Architecture

### Core Design Principles

- **Inheritance-based**: All agents inherit from `BaseGraphAgent`
- **Dual Interface**: Implements both LangGraph and A2A protocol interfaces
- **State Management**: Uses TypedDict-based state schemas
- **Modular Design**: Clear separation of LangGraph logic and A2A communication

### Implementation Pattern

Each agent follows a consistent structure:

1. **LangGraph Implementation** (`*_agent_lg.py`): Core agent logic using LangGraph
2. **A2A Wrapper** (`*_agent_a2a.py`): A2A protocol compatibility layer
3. **Entry Point** (`__main__.py`): Server startup and configuration
4. **Documentation** (`AGENT.md`): Agent-specific documentation

## Available Agents

### Core Orchestration Agents

- [**Supervisor Agent**](./supervisor/) - Workflow orchestrator and coordinator
  - Coordinates multiple worker agents
  - Manages complex multi-step workflows
  - Handles inter-agent communication

- [**Planner Agent**](./planner/) - Task planning and decomposition
  - Converts user requests into structured execution plans
  - Creates JSON-formatted step-by-step plans
  - Optimizes workflow execution order

### Specialized Worker Agents

- [**Browser Agent**](./browser/) - Web automation and data extraction
  - Web page navigation and interaction
  - Data scraping and form filling
  - Screenshot capture and analysis

- [**Executor Agent**](./executor/) - General task execution
  - Code execution in sandboxed environment
  - File operations and data processing
  - API calls and external integrations

- [**Knowledge Agent**](./knowledge/) - Information retrieval and RAG
  - Document indexing and search
  - Knowledge base management
  - Contextual information retrieval

### Utility Modules

- [**`prompts.py`**](./prompts.py) - Agent prompt templates and utilities
  - System prompts for different agent types
  - User prompt formatting functions
  - Prompt management and versioning

- [**`model.py`**](./model.py) - Shared model configurations
  - Common LLM configurations
  - Model initialization utilities

- [**`sample.py`**](./sample.py) - Sample agent implementations
  - Reference implementations
  - Testing and development examples

## File Structure

```
src/agents/
├── __init__.py                    # Package initialization
├── AGENT.md                       # This documentation
├── prompts.py                     # Agent prompt templates
├── model.py                       # Shared model configurations
├── sample.py                      # Sample implementations
├── supervisor/                    # Supervisor agent
│   ├── __init__.py
│   ├── __main__.py               # Server entry point
│   ├── supervisor_agent_lg.py    # LangGraph implementation
│   ├── supervisor_agent_a2a.py   # A2A wrapper
│   └── AGENT.md                  # Agent documentation
├── planner/                       # Planner agent
│   ├── __init__.py
│   ├── __main__.py
│   ├── planner_agent_lg.py
│   ├── planner_agent_a2a.py
│   └── AGENT.md
├── browser/                       # Browser agent
│   ├── __init__.py
│   ├── __main__.py
│   ├── browser_use_agent_lg.py
│   ├── browser_use_agent_a2a.py
│   └── AGENT.md
├── executor/                      # Executor agent
│   ├── __init__.py
│   ├── __main__.py
│   ├── task_executor_agent_lg.py
│   ├── task_executor_agent_a2a.py
│   └── AGENT.md
└── knowledge/                     # Knowledge agent
    ├── __init__.py
    ├── __main__.py
    ├── knowledge_agent_lg.py
    ├── knowledge_agent_a2a.py
    └── AGENT.md
```

## Agent Development Pattern

### 1. Create LangGraph Implementation

```python
# agent_lg.py - Core LangGraph logic
from src.base.base_graph_agent import BaseGraphAgent

class MyAgent(BaseGraphAgent):
    def init_nodes(self, graph: StateGraph) -> None:
        # Define graph nodes
        pass

    def init_edges(self, graph: StateGraph) -> None:
        # Define graph edges
        pass
```

### 2. Create A2A Wrapper

```python
# agent_a2a.py - A2A protocol wrapper
from src.base.a2a_interface import BaseA2AAgent

class MyAgentA2A(BaseA2AAgent, MyAgent):
    async def execute_for_a2a(self, input_dict, config=None):
        # A2A-compatible execution
        pass
```

### 3. Add Server Entry Point

```python
# __main__.py - Server startup
def main():
    # Server configuration and startup
    pass
```

## Common Agent Features

### State Management

All agents use TypedDict-based state schemas:

```python
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    workflow_phase: str
    current_step: int
    results: list[dict]
    errors: list[str]
```

### Error Handling

Consistent error handling patterns:

```python
try:
    # Agent logic
    pass
except Exception as e:
    return self.format_error(e, "Operation failed")
```

### Configuration

Environment-based configuration:

```python
# Environment variables
AGENT_HOST=localhost
AGENT_PORT=8000
OPENAI_API_KEY=sk-...
IS_DOCKER=false
```

## Agent Communication

### Inter-Agent Communication

Agents communicate via A2A protocol:

```python
# Supervisor calling worker agent
client_manager = A2AClientManager(
    base_url="http://worker-agent:8000"
)
await client_manager.initialize()
result = await client_manager.send_data(task_data)
```

### Workflow Coordination

Supervisor agent coordinates complex workflows:

```python
# Multi-step workflow execution
workflow = [
    {"agent": "planner", "task": "analyze request"},
    {"agent": "browser", "task": "gather data"},
    {"agent": "executor", "task": "process results"}
]
```

## Testing and Development

### Running Individual Agents

```bash
# Set Python path
export PYTHONPATH="${PWD}/src"

# Run specific agent
uv run python -m agents.supervisor
uv run python -m agents.browser
uv run python -m agents.executor
```

### Development Workflow

1. **Implement LangGraph logic** in `*_agent_lg.py`
2. **Add A2A wrapper** in `*_agent_a2a.py`
3. **Test standalone** with LangGraph
4. **Test A2A integration** with protocol
5. **Add documentation** in `AGENT.md`

## Performance Considerations

### Resource Management

- **Memory**: Efficient state management and cleanup
- **Concurrency**: Async/await patterns for I/O operations
- **Caching**: Result caching for repeated operations
- **Timeout**: Configurable timeouts for long-running tasks

### Scalability

- **Horizontal Scaling**: Container-based deployment
- **Load Balancing**: Multiple agent instances
- **State Persistence**: External state storage for recovery
- **Monitoring**: Performance metrics and health checks

-----

## Related Documentation

### Agent-Specific Documentation

- [**Supervisor Agent**](./supervisor/AGENT.md) - Workflow orchestrator implementation
- [**Planner Agent**](./planner/AGENT.md) - Task planning and decomposition
- [**Browser Agent**](./browser/AGENT.md) - Web automation and interaction
- [**Executor Agent**](./executor/AGENT.md) - General task execution
- [**Knowledge Agent**](./knowledge/AGENT.md) - Information retrieval and RAG

### Navigation

- [**Back to Source Architecture**](../AGENT.md) - Return to source code documentation
- [**Main Architecture**](../../AGENT.md) - Return to main documentation