"""
A2A (Agent-to-Agent) Integration Module

Simplified integration between LangGraph agents and A2A protocol.
"""

# Core executor
# Client utilities
from src.a2a_integration.a2a_lg_client_utils import (
    A2AClientManager,
)

# Server utilities
from src.a2a_integration.a2a_lg_server_utils import (
    create_agent_card,
    to_a2a_run_uvicorn,
    to_a2a_starlette_server,
)
from src.a2a_integration.executor import LangGraphAgentExecutor

# Configuration
from src.a2a_integration.models import LangGraphExecutorConfig


__all__ = [
    # Client utilities
    'A2AClientManager',
    # Core
    'LangGraphAgentExecutor',
    'LangGraphAgentExecutor',
    # Configuration
    'LangGraphExecutorConfig',
    # Server utilities
    'create_agent_card',
    'to_a2a_run_uvicorn',
    'to_a2a_starlette_server',
]
