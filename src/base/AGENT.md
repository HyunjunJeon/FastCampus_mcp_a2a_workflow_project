# Base Classes and Utilities

## Overview

This module provides the foundational abstract base classes and common utilities that all agents in the system inherit from and utilize. It establishes the core architecture patterns and ensures consistency across all agent implementations.

## Core Components

### Abstract Base Classes

- [**`BaseGraphAgent`**](./base_graph_agent.py) - LangGraph agent abstract base class
  - Defines the standard agent interface with `init_nodes()` and `init_edges()` methods
  - Implements graph construction logic and compilation
  - Handles MCP tool integration and initialization
  - Provides async initialization patterns

- [**`BaseGraphState`**](./base_graph_state.py) - State management base classes
  - `BaseGraphInputState`: Input state with MessagesState
  - `BaseGraphState`: Complete state management with message handling
  - TypedDict-based state schemas for type safety

### Protocol Integration

- [**`a2a_interface.py`**](./a2a_interface.py) - A2A protocol interface definitions
  - `A2AOutput`: Standardized output format for A2A integration
  - `BaseA2AAgent`: Abstract base class for A2A-compatible agents
  - Stream event handling and output formatting utilities

### Configuration & Utilities

- [**`configuration.py`**](./configuration.py) - Configuration management
  - Pydantic-based configuration classes
  - MCP server configuration
  - Environment variable integration

- [**`util.py`**](./util.py) - Common utility functions
  - Environment file loading utilities
  - Message extraction helpers
  - API key management functions

### Error Handling

- [**`error_handling.py`**](./error_handling.py) - Unified error management system
  - Custom exception classes (`AgentExecutionError`, `AgentValidationError`, etc.)
  - Structured error responses with context preservation
  - Error formatting and logging utilities
  - Async-compatible error handling decorators

## Design Principles

### Inheritance Pattern

All agents must follow this pattern:
1. Inherit from `BaseGraphAgent` for LangGraph integration
2. Implement `BaseA2AAgent` for A2A protocol compatibility
3. Define state schemas using TypedDict from `BaseGraphState`
4. Use structured error handling from `error_handling.py`

### Key Architecture Patterns

#### Agent Lifecycle
```python
class MyAgent(BaseGraphAgent, BaseA2AAgent):
    async def initialize(self) -> None:
        # Async initialization
        pass

    def init_nodes(self, graph: StateGraph) -> None:
        # Define graph nodes
        pass

    def init_edges(self, graph: StateGraph) -> None:
        # Define graph edges
        pass
```

#### A2A Integration
```python
async def execute_for_a2a(self, input_dict, config=None) -> A2AOutput:
    # Process input and return standardized output
    return self.create_a2a_output(
        status="completed",
        text_content="Result",
        data_content={"key": "value"}
    )
```

## File Structure

```
src/base/
├── __init__.py                 # Package initialization
├── base_graph_agent.py         # Abstract LangGraph agent base class
├── base_graph_state.py         # State management base classes
├── a2a_interface.py           # A2A protocol interface definitions
├── configuration.py           # Configuration management
├── error_handling.py          # Error handling utilities
├── util.py                    # Common utility functions
└── AGENT.md                   # This documentation
```

## Usage Examples

### Creating a New Agent
```python
from src.base.base_graph_agent import BaseGraphAgent
from src.base.a2a_interface import BaseA2AAgent

class MyCustomAgent(BaseGraphAgent, BaseA2AAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent_type = "MyCustom"

    def init_nodes(self, graph):
        # Implement node definitions
        pass

    def init_edges(self, graph):
        # Implement edge definitions
        pass
```

### Error Handling
```python
from src.base.error_handling import handle_agent_errors

@handle_agent_errors()
async def risky_operation(self):
    # Operation that might fail
    pass
```

-----

## Related Documentation

### Navigation

- [**Back to Source Architecture**](../AGENT.md) - Return to source code documentation
- [**Main Architecture**](../../AGENT.md) - Return to main documentation