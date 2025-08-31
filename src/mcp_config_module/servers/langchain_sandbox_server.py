"""LangChain Sandbox MCP Server implementation.

This server provides secure Python code execution using PyodideSandbox (WebAssembly).
It supports session-based isolation and state persistence across executions.
"""

import asyncio
import json
import logging

from datetime import datetime, timedelta
from typing import Any

import pytz

from langchain_sandbox import PyodideSandbox
from pydantic import BaseModel, Field

from src.mcp_config_module.base_mcp_server import BaseMCPServer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SandboxSession(BaseModel):
    """Sandbox session management."""

    session_id: str
    sandbox: Any  # PyodideSandbox instance
    created_at: datetime
    last_accessed: datetime
    execution_count: int = 0
    total_execution_time: float = 0.0


class ExecutionResult(BaseModel):
    """Python code execution result."""

    success: bool
    output: str | None = None
    error: str | None = None
    execution_time: float
    session_id: str
    variables: dict[str, str] | None = None


class LangChainSandboxMCPServer(BaseMCPServer):
    """MCP Server for LangChain Sandbox code execution.

    This server provides secure Python code execution using PyodideSandbox,
    which runs Python in WebAssembly for isolation.

    WebAssembly 기반 격리 환경에서 안전하게 Python 코드를 실행하며,
    세션별로 상태를 유지하여 연속적인 코드 실행을 지원합니다.
    """

    def __init__(
        self,
        port: int = 8035,
        host: str = '0.0.0.0',
        debug: bool = False,
        **kwargs
    ):
        """Initialize LangChain Sandbox MCP Server.

        Args:
            port: Server port (default: 8035)
            host: Host address (default: "0.0.0.0")
            debug: Debug mode flag
            allow_network: Allow network access in sandbox (httpx only)
            session_timeout_minutes: Session timeout in minutes
            max_sessions: Maximum concurrent sessions
        """
        # kwargs에서 샌드박스 설정 추출
        self.allow_network = kwargs.get('allow_network', True)
        self.session_timeout_minutes = kwargs.get('session_timeout_minutes', 30)
        self.max_sessions = kwargs.get('max_sessions', 10)
        # 활성 세션들을 관리하는 딕셔너리
        self.sessions: dict[str, SandboxSession] = {}

        super().__init__(
            server_name='langchain-sandbox-mcp',
            port=port,
            host=host,
            debug=debug,
            server_instructions=(
                'LangChain Sandbox MCP Server for secure Python code execution. '
                'Uses PyodideSandbox (WebAssembly) for isolation. '
                'Supports session-based state persistence and limited network access.'
            ),
            enable_middlewares=['logging', 'error_handling'],
        )

    def _initialize_clients(self) -> None:
        """Initialize sandbox sessions dictionary."""
        self.sessions = {}
        self._cleanup_task = None
        logger.info('LangChain Sandbox MCP Server initialized')

    def _register_tools(self) -> None:
        """Register MCP tools for sandbox operations."""
        self._register_execute_python_tool()
        self._register_reset_sandbox_tool()

    def _register_execute_python_tool(self) -> None:
        """Register Python execution tool."""

        @self.mcp.tool()
        async def execute_python(
            code: str = Field(..., description='Python code to execute. IMPORTANT: Due to WebAssembly limitations, print() outputs are NOT captured. To return results, assign them to a variable and return that variable as the last expression. Example: result = {"output": "Hello", "value": 42}; result'),
            session_id: str = Field(
                default='default',
                description='Session ID for state persistence across multiple executions',
            ),
        ) -> dict[str, Any]:
            """Execute Python code in a secure WebAssembly sandbox.

            CRITICAL OUTPUT INSTRUCTIONS:
            - print() statements do NOT work due to WebAssembly stdout limitations
            - To return output, use one of these patterns:
              1. Return a value directly: 'result = 2 + 2; result'
              2. Return a dictionary: 'output = {"message": "Hello", "result": 42}; output'
              3. Return a formatted string: 'f"Result: {2+2}"'

            The sandbox maintains state between executions within the same session.
            Variables and imports persist across calls.

            Example usage:
            ```python
            # WRONG - print won't show output:
            print("Hello World")

            # CORRECT - return the value:
            message = "Hello World"
            result = {"output": message, "calculation": 2+2}
            result  # This will be returned
            ```

            Args:
                code: Python code to execute (must return a value to see output)
                session_id: Session identifier for state persistence

            Returns:
                Execution result with the returned value in 'output' field
            """
            try:
                start_time = asyncio.get_event_loop().time()

                # Get or create session
                session = await self._get_or_create_session(session_id)

                # Execute code directly (no print capture as it doesn't work in WebAssembly)
                logger.info(f'Executing code in session {session_id}')

                # Execute the code directly - it should return a value
                result = await session.sandbox.execute(code)

                # Calculate execution time
                execution_time = asyncio.get_event_loop().time() - start_time

                # Update session stats
                session.last_accessed = datetime.now(pytz.UTC)
                session.execution_count += 1
                session.total_execution_time += execution_time

                # Get current variables (simplified - actual implementation would need introspection)
                variables = None
                if self.debug:
                    try:
                        var_code = "import json; json.dumps({k: type(v).__name__ for k, v in globals().items() if not k.startswith('_')})"
                        var_result = await session.sandbox.execute(var_code)
                        # Check if var_result has output attribute
                        if hasattr(var_result, 'output') and var_result.output:
                            variables = json.loads(var_result.output)
                    except Exception as e:
                        logger.warning(f'Failed to get variables: {e}')

                # Format result - handle CodeExecutionResult object properly
                output_text = ''
                error_text = None

                if hasattr(result, 'output'):
                    # The output now contains the captured print statements
                    output_text = result.output or ''
                if hasattr(result, 'error'):
                    error_text = result.error

                return self.create_standard_response(
                    success=True,
                    query=f'execute_python(session={session_id})',
                    data=ExecutionResult(
                        success=True,
                        output=output_text,
                        error=error_text,
                        execution_time=execution_time,
                        session_id=session_id,
                        variables=variables,
                    ).model_dump(),
                )

            except Exception as e:
                logger.error(f'Execution failed: {e}')
                return self.create_error_response(
                    error=str(e),
                    query=f'execute_python(session={session_id})',
                    func_name='execute_python',
                )

    def _register_reset_sandbox_tool(self) -> None:
        """Register sandbox reset tool."""

        @self.mcp.tool()
        async def reset_sandbox(
            session_id: str = Field(
                default='default', description='Session ID to reset'
            ),
        ) -> dict[str, Any]:
            """Reset a sandbox session, clearing all state.

            Args:
                session_id: Session identifier to reset

            Returns:
                Success status
            """
            try:
                if session_id in self.sessions:
                    old_session = self.sessions[session_id]
                    # Create new sandbox
                    new_sandbox = PyodideSandbox(allow_net=self.allow_network)
                    self.sessions[session_id] = SandboxSession(
                        session_id=session_id,
                        sandbox=new_sandbox,
                        created_at=datetime.now(pytz.UTC),
                        last_accessed=datetime.now(pytz.UTC),
                    )
                    logger.info(f'Reset sandbox session {session_id}')

                    return self.create_standard_response(
                        success=True,
                        query=f'reset_sandbox(session={session_id})',
                        data={
                            'message': f'Session {session_id} reset successfully',
                            'previous_execution_count': old_session.execution_count,
                            'previous_total_time': old_session.total_execution_time,
                        },
                    )
                return self.create_standard_response(
                    success=True,
                    query=f'reset_sandbox(session={session_id})',
                    data={
                        'message': f'Session {session_id} not found, nothing to reset',
                    },
                )

            except Exception as e:
                logger.error(f'Failed to reset sandbox: {e}')
                return self.create_error_response(
                    error=str(e),
                    query=f'reset_sandbox(session={session_id})',
                    func_name='reset_sandbox',
                )

        @self.mcp.tool()
        async def get_sandbox_state(
            session_id: str = Field(
                default='default', description='Session ID to query'
            ),
        ) -> dict[str, Any]:
            """Get current state of a sandbox session.

            Args:
                session_id: Session identifier to query

            Returns:
                Session state including variables and statistics
            """
            try:
                if session_id not in self.sessions:
                    return self.create_standard_response(
                        success=True,
                        query=f'get_sandbox_state(session={session_id})',
                        data={
                            'exists': False,
                            'message': f'Session {session_id} does not exist',
                        },
                    )

                session = self.sessions[session_id]

                # Get defined variables
                var_code = """
import json
import types

def get_vars():
    vars_info = {}
    for name, value in globals().items():
        if not name.startswith('_'):
            if isinstance(value, types.ModuleType):
                vars_info[name] = f"module:{value.__name__}"
            elif callable(value):
                vars_info[name] = f"function:{name}"
            else:
                vars_info[name] = f"{type(value).__name__}:{repr(value)[:50]}"
    return json.dumps(vars_info)

get_vars()
"""
                var_result = await session.sandbox.execute(var_code)
                variables = {}
                if var_result.get('output'):
                    try:
                        variables = json.loads(var_result['output'])
                    except json.JSONDecodeError:
                        variables = {'error': 'Failed to parse variables'}

                return self.create_standard_response(
                    success=True,
                    query=f'get_sandbox_state(session={session_id})',
                    data={
                        'exists': True,
                        'session_id': session_id,
                        'created_at': session.created_at.isoformat(),
                        'last_accessed': session.last_accessed.isoformat(),
                        'execution_count': session.execution_count,
                        'total_execution_time': session.total_execution_time,
                        'variables': variables,
                    },
                )

            except Exception as e:
                logger.error(f'Failed to get sandbox state: {e}')
                return self.create_error_response(
                    error=str(e),
                    query=f'get_sandbox_state(session={session_id})',
                    func_name='get_sandbox_state',
                )

        @self.mcp.tool()
        async def list_sessions() -> dict[str, Any]:
            """List all active sandbox sessions.

            Returns:
                List of active sessions with their statistics
            """
            try:
                sessions_info = []
                for session_id, session in self.sessions.items():
                    sessions_info.append(
                        {
                            'session_id': session_id,
                            'created_at': session.created_at.isoformat(),
                            'last_accessed': session.last_accessed.isoformat(),
                            'execution_count': session.execution_count,
                            'total_execution_time': session.total_execution_time,
                        }
                    )

                return self.create_standard_response(
                    success=True,
                    query='list_sessions()',
                    data={
                        'active_sessions': len(sessions_info),
                        'max_sessions': self.max_sessions,
                        'sessions': sessions_info,
                    },
                )

            except Exception as e:
                logger.error(f'Failed to list sessions: {e}')
                return self.create_error_response(
                    error=str(e),
                    query='list_sessions()',
                    func_name='list_sessions',
                )

        logger.info('Tools registered successfully')

    async def _get_or_create_session(self, session_id: str) -> SandboxSession:
        """Get existing session or create new one.

        Args:
            session_id: Session identifier

        Returns:
            SandboxSession instance
        """
        # Clean up old sessions if needed
        await self._cleanup_old_sessions()

        if session_id not in self.sessions:
            # Check max sessions limit
            if len(self.sessions) >= self.max_sessions:
                # Remove oldest session
                oldest_id = min(
                    self.sessions.keys(),
                    key=lambda k: self.sessions[k].last_accessed,
                )
                del self.sessions[oldest_id]
                logger.info(f'Removed oldest session {oldest_id} due to limit')

            # Create new session
            sandbox = PyodideSandbox(allow_net=self.allow_network)
            self.sessions[session_id] = SandboxSession(
                session_id=session_id,
                sandbox=sandbox,
                created_at=datetime.now(pytz.UTC),
                last_accessed=datetime.now(pytz.UTC),
            )
            logger.info(f'Created new sandbox session {session_id}')

        return self.sessions[session_id]

    async def _cleanup_old_sessions(self) -> None:
        """Remove sessions older than timeout."""
        now = datetime.now(pytz.UTC)
        timeout_delta = timedelta(minutes=self.session_timeout_minutes)

        to_remove = []
        for session_id, session in self.sessions.items():
            if now - session.last_accessed > timeout_delta:
                to_remove.append(session_id)

        for session_id in to_remove:
            del self.sessions[session_id]
            logger.info(f'Removed expired session {session_id}')

    async def shutdown(self, timeout: float | None = None) -> None:
        """Shutdown server and cleanup resources."""
        logger.info('Shutting down LangChain Sandbox MCP Server')

        # Clear all sessions
        self.sessions.clear()

        # Call parent shutdown
        await super().shutdown(timeout)


def main() -> None:
    """Main entry point for the server."""
    import argparse

    import uvicorn

    parser = argparse.ArgumentParser(description='LangChain Sandbox MCP Server')
    parser.add_argument('--port', type=int, default=8035, help='Server port')
    parser.add_argument(
        '--host', type=str, default='0.0.0.0', help='Server host'
    )
    parser.add_argument(
        '--debug', action='store_true', help='Enable debug mode'
    )
    parser.add_argument(
        '--no-network',
        action='store_true',
        help='Disable network access in sandbox',
    )
    parser.add_argument(
        '--session-timeout',
        type=int,
        default=30,
        help='Session timeout in minutes',
    )
    parser.add_argument(
        '--max-sessions',
        type=int,
        default=10,
        help='Maximum concurrent sessions',
    )

    args = parser.parse_args()

    # Create server
    server = LangChainSandboxMCPServer(
        port=args.port,
        host=args.host,
        debug=args.debug,
        allow_network=not args.no_network,
        session_timeout_minutes=args.session_timeout,
        max_sessions=args.max_sessions,
    )

    # Create app
    app = server.create_app()

    # Log startup info
    logger.info(
        f'Starting LangChain Sandbox MCP Server on {args.host}:{args.port}'
    )
    logger.info(f'Debug mode: {args.debug}')
    logger.info(f'Network access: {not args.no_network}')
    logger.info(f'Session timeout: {args.session_timeout} minutes')
    logger.info(f'Max sessions: {args.max_sessions}')
    logger.info(f'Health check: http://{args.host}:{args.port}/health')
    logger.info(f'MCP endpoint: http://{args.host}:{args.port}/mcp')

    # Run server
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        log_level='info' if args.debug else 'warning',
    )


if __name__ == '__main__':
    main()
