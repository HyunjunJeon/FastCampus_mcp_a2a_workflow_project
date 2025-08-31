# Source Code Architecture

## Overview

This directory contains the core implementation of the multi-agent workflow automation system based on LangGraph and A2A protocol. The system follows a modular architecture with clear separation of concerns.

## Module Structure

The source code is organized into distinct modules, each serving specific architectural purposes in the multi-agent system.

### Core Modules

- [**`base/`**](./base/AGENT.md) - Abstract base classes and common utilities for all agents
- [**`a2a_integration/`**](./a2a_integration/AGENT.md) - Agent-to-Agent protocol implementation and utilities
- [**`agents/`**](./agents/AGENT.md) - Concrete agent implementations (Supervisor, Planner, Browser, etc.)
- [**`mcp_config_module/`**](./mcp_config_module/AGENT.md) - Model Context Protocol integration for tool usage

## Design Philosophy

- **Inheritance-based Architecture**: All agents inherit from `BaseGraphAgent`
- **Protocol-driven Communication**: Standardized A2A protocol for inter-agent messaging
- **Modular Design**: Clear separation of concerns between different system components
- **Containerized Microservices**: Each agent runs as an independent containerized service

## Key Components

### Base Infrastructure

- `BaseGraphAgent`: Abstract base class for all LangGraph agents
- `BaseGraphState`: State management utilities
- `A2AOutput`: Standardized output format for A2A integration
- Error handling and configuration management

### A2A Protocol Integration

- `A2AClientManager`: Client for inter-agent communication
- `A2AStarletteApplication`: HTTP server for A2A endpoints
- Authentication and CORS handling
- Request/response processing

### Agent Implementations

- **Supervisor Agent**: Orchestrates workflow execution
- **Planner Agent**: Creates structured execution plans
- **Browser Agent**: Web automation and data extraction
- **Knowledge Agent**: RAG-based information retrieval
- **Executor Agent**: General task execution

### MCP Integration

- Playwright MCP for browser automation
- Notion MCP for document management
- LangChain Sandbox MCP for code execution
- OpenMemory MCP for knowledge management

## Quick Start

### Environment Setup

```bash
# Set Python path
export PYTHONPATH="${PWD}/src"

# Install dependencies
uv sync

# Run specific agent
uv run python -m agents.supervisor
```

### Agent Development

1. Extend `BaseGraphAgent` for new agents
2. Implement A2A interface methods
3. Use `A2AClientManager` for inter-agent communication
4. Configure MCP tools as needed

-----

## Related Documentation

### Module Documentation

- [**Base Classes & Utilities**](./base/AGENT.md) - Core abstract classes and shared utilities
- [**A2A Integration**](./a2a_integration/AGENT.md) - A2A protocol client/server implementations
- [**Agent Implementations**](./agents/AGENT.md) - Concrete agent implementations
- [**MCP Integration**](./mcp_config_module/AGENT.md) - Model Context Protocol tool integration

### Navigation

- [**Back to Main Architecture**](../AGENT.md) - Return to main documentation
- [**Project Root**](../README.md) - Project overview and setup
