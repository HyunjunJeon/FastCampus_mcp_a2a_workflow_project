# MCP Integration Module

## Overview

This module provides comprehensive integration with Model Context Protocol (MCP) servers, enabling seamless tool usage and external service integration for LangGraph agents.

## Core Components

### Configuration & Management

- [**`mcp_config.py`**](./mcp_config.py) - MCP server configuration and management
  - `MCPServerConfig`: Server configuration management class
  - Environment-aware URL resolution (Docker vs local)
  - Agent-specific server groupings
  - Tool loading and client creation

- [**`health_checker.py`**](./health_checker.py) - Service health monitoring
  - `MCPHealthChecker`: MCP service health checking utilities
  - Automatic service startup coordination
  - Docker and local environment support
  - Timeout and retry handling

### Server Infrastructure

- [**`base_mcp_server.py`**](./base_mcp_server.py) - Base MCP server implementation
  - `BaseMCPServer`: Abstract base class for MCP servers
  - Middleware integration system
  - Standard response/error formatting
  - Async lifecycle management

### Middleware System

- [**`common/middleware/`**](./common/middleware/) - MCP middleware components
  - [**`cors.py`**](./common/middleware/cors.py) - CORS handling middleware
  - [**`error_handling.py`**](./common/middleware/error_handling.py) - Error handling and logging
  - [**`logging.py`**](./common/middleware/logging.py) - Request/response logging

### Server Implementations

- [**`servers/langchain_sandbox_server.py`**](./servers/langchain_sandbox_server.py) - Code execution server
  - `LangChainSandboxMCPServer`: WebAssembly-based Python execution
  - Session management and state persistence
  - Secure code execution environment

## Supported MCP Servers

### Core MCP Services

| Service | Purpose | Environment Support |
|---------|---------|-------------------|
| **Playwright MCP** | Browser automation | Docker: `host.docker.internal:8931`<br>Local: `localhost:8931` |
| **Notion MCP** | Document management | Docker: `notion-mcp:3000`<br>Local: `localhost:8930` |
| **LangChain Sandbox** | Code execution | Docker: `langchain-sandbox-mcp:8035`<br>Local: `localhost:8035` |
| **OpenMemory MCP** | Knowledge storage | Docker: `openmemory-mcp:8031`<br>Local: `localhost:8031` |

### Agent-Specific Configurations

#### Browser Agent
```python
servers = MCPServerConfig.get_agent_server_configs('browser')
# Returns: ['playwright-mcp']
```

#### Knowledge Agent
```python
servers = MCPServerConfig.get_agent_server_configs('knowledge')
# Returns: ['open-memory-mcp']
```

#### Executor Agent
```python
servers = MCPServerConfig.get_agent_server_configs('executor')
# Returns: ['langchain-sandbox-mcp', 'notion-mcp']
```

## Key Features

### Environment-Aware Configuration

The module automatically detects and configures for different environments:

```python
# Docker environment detection
IS_DOCKER = os.getenv('IS_DOCKER', 'false').lower() == 'true'

# URL resolution based on environment
if IS_DOCKER:
    url = f'http://service-name:port/mcp'
else:
    url = f'http://localhost:port/mcp'
```

### Tool Integration

Seamless integration with LangGraph agents:

```python
# Load tools for specific agent
tools = await load_tools_for_agent('browser')

# Create agent with MCP tools
agent = create_react_agent(
    model=model,
    tools=tools,
    prompt=system_prompt
)
```

### Health Monitoring

Automatic service health checking and coordination:

```python
# Check service availability
is_healthy = await MCPHealthChecker.check_service(
    'playwright-mcp',
    is_docker=True
)

# Wait for multiple services
services_ready = await MCPHealthChecker.ensure_services_ready(
    'browser',
    is_docker=True,
    timeout=60
)
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `IS_DOCKER` | Docker environment flag | `false` |
| `USER_ID` | User ID for OpenMemory | `default_user` |
| `AUTH_TOKEN` | Notion MCP auth token | - |
| `AGENT_HOST` | Agent server host | `localhost` / `0.0.0.0` |
| `AGENT_PORT` | Agent server port | `8000+` |

### MCP Server Configuration

```python
# Standard MCP server configuration
STANDARD_MCP_SERVERS = {
    'playwright-mcp': {
        'transport': 'streamable_http',
        'url': 'http://localhost:8931/mcp',  # Auto-resolved
        'headers': {
            'Accept': 'application/json, text/event-stream',
            'Cache-Control': 'no-cache',
        },
    },
    # ... other servers
}
```

## Usage Patterns

### Basic Tool Loading

```python
from src.mcp_config_module.mcp_config import load_tools_for_agent

# Load tools for browser agent
tools = await load_tools_for_agent('browser')

# Use tools in LangGraph agent
agent = create_react_agent(model, tools, prompt)
```

### Server Implementation

```python
from src.mcp_config_module.base_mcp_server import BaseMCPServer

class MyMCPServer(BaseMCPServer):
    def _initialize_clients(self):
        # Initialize service clients
        pass

    def _register_tools(self):
        # Register MCP tools
        pass
```

### Middleware Usage

```python
from src.mcp_config_module.common.middleware import (
    CORSMiddleware,
    ErrorHandlingMiddleware,
    LoggingMiddleware
)

# Create middleware stack
middlewares = [
    CORSMiddleware(allow_origins=['*']),
    ErrorHandlingMiddleware(),
    LoggingMiddleware()
]
```

## File Structure

```
src/mcp_config_module/
├── __init__.py                       # Package initialization
├── mcp_config.py                     # MCP server configuration
├── health_checker.py                 # Service health monitoring
├── base_mcp_server.py               # Base MCP server class
├── common/                           # Shared utilities
│   └── middleware/                   # Middleware components
│       ├── cors.py                  # CORS handling
│       ├── error_handling.py        # Error handling
│       └── logging.py               # Request logging
├── servers/                          # MCP server implementations
│   └── langchain_sandbox_server.py # Code execution server
└── AGENT.md                          # This documentation
```

## Error Handling

Comprehensive error handling for MCP operations:

- **Connection Errors**: Automatic retry with exponential backoff
- **Service Unavailable**: Health check-based service detection
- **Timeout Handling**: Configurable timeouts for long-running operations
- **Authentication Errors**: Secure credential management

## Performance Optimization

### Connection Management

- **Connection Pooling**: Efficient HTTP connection reuse
- **Keep-Alive**: Persistent connections for reduced latency
- **Timeout Configuration**: Appropriate timeouts for different operations

### Caching Strategies

- **Tool Metadata Caching**: Reduce repeated tool discovery overhead
- **Response Caching**: Cache frequently accessed data
- **Session Management**: Efficient session handling for stateful operations

## Security Considerations

### Authentication

- **Token Management**: Secure storage and transmission of auth tokens
- **Environment Variables**: Sensitive data stored in environment variables
- **Request Signing**: Optional request signing for additional security

### Network Security

- **HTTPS Enforcement**: TLS encryption for all MCP communications
- **Host Verification**: Certificate validation for secure connections
- **Firewall Configuration**: Proper network isolation in production

-----

## Related Documentation

### Navigation

- [**Back to Source Architecture**](../AGENT.md) - Return to source code documentation
- [**Main Architecture**](../../AGENT.md) - Return to main documentation
