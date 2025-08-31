# A2A Integration

## Overview

This module provides the complete implementation of the Agent-to-Agent (A2A) protocol, enabling standardized communication between agents in the multi-agent system. It serves as the communication backbone that allows agents to interact seamlessly.

## Core Components

### Client-Side Integration

- [**`a2a_lg_client_utils.py`**](./a2a_lg_client_utils.py) - A2A client manager
  - `A2AClientManager`: Main client for inter-agent communication
  - `A2AMessageEngine`: Core message processing engine
  - Specialized clients: `A2ATextClient`, `A2ADataClient`, `A2AFileClient`
  - Task caching and deduplication mechanisms

- [**`models.py`**](./models.py) - Configuration models
  - `LangGraphExecutorConfig`: Executor configuration
  - Pydantic models for A2A message structures

### Server-Side Integration

- [**`a2a_lg_server_utils.py`**](./a2a_lg_server_utils.py) - A2A server utilities
  - `to_a2a_starlette_server()`: Convert LangGraph graphs to A2A servers
  - `create_agent_card()`: Generate agent capability descriptions
  - `build_request_handler()`: HTTP request handling
  - `to_a2a_run_uvicorn()`: Server execution utilities

- [**`executor.py`**](./executor.py) - LangGraph executor for A2A
  - `LangGraphAgentExecutor`: Executes LangGraph agents via A2A protocol
  - Streaming and blocking execution modes
  - Task management and status tracking

### Protocol Support

- [**`cors_utils.py`**](./cors_utils.py) - CORS handling utilities
  - `create_cors_enabled_app()`: CORS-enabled Starlette applications
  - Cross-origin request handling for web-based agents

## Key Features

### Communication Patterns

- **Asynchronous Communication**: Full async/await support for all operations
- **Streaming Support**: Real-time event streaming for long-running tasks
- **Protocol Compliance**: Complete A2A specification adherence (JSON-RPC 2.0)
- **Authentication Integration**: Pluggable authentication mechanisms

### Error Handling & Resilience

- **Structured Error Responses**: Consistent error formatting across all agents
- **Retry Logic**: Automatic retry with exponential backoff
- **Connection Management**: Robust connection pooling and health checks
- **Task Deduplication**: Prevents duplicate task execution

### Agent Discovery

- **Agent Cards**: Standardized capability descriptions
- **Service Discovery**: Automatic agent location and capability detection
- **Health Monitoring**: Built-in health check endpoints

## Usage Patterns

### Client Usage
```python
# Initialize A2A client
client_manager = A2AClientManager(
    base_url="http://agent-url:8000",
    streaming=True
)
await client_manager.initialize()

# Send text message
response = await client_manager.text_client.send("Hello, agent!")

# Send structured data
response = await client_manager.data_client.send({"task": "analyze", "data": [...]})
```

### Server Setup
```python
# Convert LangGraph agent to A2A server
server_app = to_a2a_starlette_server(
    graph=my_langgraph_agent,
    agent_card=create_agent_card(
        name="MyAgent",
        description="Task execution agent",
        url="http://localhost:8000",
        skills=[agent_skill]
    )
)

# Run server
to_a2a_run_uvicorn(server_app, host="0.0.0.0", port=8000)
```

### Executor Integration
```python
# Create executor for A2A integration
executor = LangGraphAgentExecutor(
    agent_class=MyAgent,
    config=LangGraphExecutorConfig(enable_streaming=True)
)

# Handle A2A requests
await executor.execute(context, event_queue)
```

## File Structure

```
src/a2a_integration/
├── __init__.py                      # Package exports
├── a2a_lg_client_utils.py          # A2A client implementation
├── a2a_lg_server_utils.py         # A2A server utilities
├── executor.py                     # LangGraph executor
├── models.py                       # Configuration models
├── cors_utils.py                   # CORS handling
├── auth/                           # Authentication module
│   ├── __init__.py
│   ├── credentials.py             # Credential management
│   └── AGENT.md                   # Auth documentation
└── AGENT.md                        # This documentation
```

## Protocol Details

### Message Flow
1. **Discovery**: Agent queries `/.well-known/agent-card.json` for capabilities
2. **Connection**: Client establishes connection with appropriate transport
3. **Authentication**: Optional authentication handshake
4. **Message Exchange**: JSON-RPC 2.0 compliant request/response cycle
5. **Streaming**: Optional real-time event streaming
6. **Completion**: Task completion with final results

### Supported Transports
- **HTTP JSON**: Standard HTTP with JSON payloads
- **JSON-RPC over HTTP**: JSON-RPC 2.0 protocol
- **Streaming HTTP**: Server-sent events for real-time updates
- **gRPC**: High-performance RPC (future support)

## Authentication

The authentication system is modular and pluggable:

- [**`auth/credentials.py`**](./auth/credentials.py) - Credential management
  - `SimpleCredentialService`: In-memory credential storage
  - `EnvCredentialService`: Environment variable-based credentials
  - `CompositeCredentialService`: Multiple credential sources

Supported authentication methods:
- Bearer tokens
- API keys
- OAuth 2.0
- Custom authentication schemes

## Error Handling

Comprehensive error handling with structured responses:

- **Network Errors**: Connection failures, timeouts
- **Protocol Errors**: Invalid message formats, unsupported operations
- **Authentication Errors**: Invalid credentials, expired tokens
- **Business Logic Errors**: Agent-specific validation failures

-----

## Related Documentation

### Sub-Module Documentation

- [**Authentication**](./auth/AGENT.md) - Security and authentication mechanisms

### Navigation

- [**Back to Source Architecture**](../AGENT.md) - Return to source code documentation
- [**Main Architecture**](../../AGENT.md) - Return to main documentation