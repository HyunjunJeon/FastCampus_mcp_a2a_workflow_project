"""LangChain Sandbox MCP 서버 구현.

WebAssembly 기반의 PyodideSandbox를 사용하여 격리된 실행 환경에서 Python 코드를
안전하게 실행합니다. 세션 단위로 상태를 유지하여, 연속 실행 간 변수/임포트가
보존되는 노트북 유사 경험을 제공합니다.

특징 및 제약:
- 표준 출력 캡처 제약: WebAssembly 환경에서는 ``print()`` 결과가 출력으로 수집되지
  않습니다. 사용자 코드는 반드시 값을 반환해야 합니다.
- 네트워크 접근은 기본 제한. 필요 시 제한적으로 허용할 수 있습니다.
- 세션은 타임아웃 경과 시 자동 정리되며, 동시 세션 수에는 상한이 있습니다.
"""

import argparse
import asyncio
import json
import logging

from datetime import datetime, timedelta
from typing import Any

import pytz
import uvicorn

from langchain_sandbox import PyodideSandbox
from pydantic import BaseModel, Field

from src.mcp_config_module.base_mcp_server import BaseMCPServer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SandboxSession(BaseModel):
    """샌드박스 세션 상태 모델.

    각 세션은 독립된 샌드박스 인스턴스를 소유하며, 생성/마지막 접근 시각과
    누적 실행 횟수, 총 실행 시간을 추적합니다.
    """

    session_id: str
    sandbox: Any  # PyodideSandbox instance
    created_at: datetime
    last_accessed: datetime
    execution_count: int = 0
    total_execution_time: float = 0.0


class ExecutionResult(BaseModel):
    """Python 코드 실행 결과 모델.

    출력/에러/실행 시간/세션 정보, (디버그 모드시) 변수 스냅샷을 포함합니다.
    """

    success: bool
    output: str | None = None
    error: str | None = None
    execution_time: float
    session_id: str
    variables: dict[str, str] | None = None


class LangChainSandboxMCPServer(BaseMCPServer):
    """LangChain 샌드박스 코드 실행을 위한 MCP 서버.

    PyodideSandbox를 통해 WebAssembly 상에서 Python을 실행하여 호스트 환경과의
    격리를 제공합니다. 세션 단위 상태 지속을 통해 REPL/노트북과 유사한 워크플로를
    지원합니다.
    """

    def __init__(
        self,
        port: int = 8035,
        host: str = '0.0.0.0',
        debug: bool = False,
        **kwargs
    ):
        """LangChain Sandbox MCP 서버 초기화.

        Args:
            port: 서버 포트 (기본: 8035)
            host: 바인드 호스트 주소 (기본: "0.0.0.0")
            debug: 디버그 모드 여부
            allow_network: 샌드박스 내 제한적 네트워크 접근 허용 여부(httpx 기반)
            session_timeout_minutes: 세션 타임아웃(분)
            max_sessions: 동시 유지 가능한 최대 세션 수
            **kwargs: 샌드박스/서버 추가 옵션
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
        """샌드박스 세션 레지스트리 초기화."""
        self.sessions = {}
        self._cleanup_task = None
        logger.info('LangChain Sandbox MCP Server initialized')

    def _register_tools(self) -> None:
        """샌드박스 조작을 위한 MCP 도구 등록.

        - ``execute_python``: Python 코드 실행(반드시 값 반환)
        - ``reset_sandbox``: 세션 상태 초기화
        - ``get_sandbox_state``: 세션 상태 조회
        - ``list_sessions``: 활성 세션 목록/통계
        """
        self._register_execute_python_tool()
        self._register_reset_sandbox_tool()

    def _register_execute_python_tool(self) -> None:
        """Python 코드 실행 도구 등록.

        WebAssembly 제약으로 ``print()``는 결과에 반영되지 않습니다. 반드시 값을
        반환해야 합니다.
        """

        @self.mcp.tool()
        async def execute_python(
            code: str = Field(..., description='Python code to execute. IMPORTANT: Due to WebAssembly limitations, print() outputs are NOT captured. To return results, assign them to a variable and return that variable as the last expression. Example: result = {"output": "Hello", "value": 42}; result'),
            session_id: str = Field(
                default='default',
                description='Session ID for state persistence across multiple executions',
            ),
        ) -> dict[str, Any]:
            """WebAssembly 샌드박스에서 Python 코드를 실행합니다.

            출력 관련 중요 지침:
            - WebAssembly stdout 제약으로 ``print()``는 결과에 포함되지 않습니다.
            - 반드시 값을 반환해야 합니다. 아래 예시를 참고하세요.

            반환 패턴 예시:
            1) 값 직접 반환: 'result = 2 + 2; result'
            2) 딕셔너리 반환: 'output = {"message": "Hello", "result": 42}; output'
            3) 포맷 문자열 반환: 'f"Result: {2+2}"'

            세션 동작:
            - 동일 ``session_id`` 내에서 변수/임포트가 보존됩니다.

            사용 예시:
            ```python
            # 잘못된 예시 - print는 출력되지 않음
            print("Hello World")

            # 올바른 예시 - 값을 반환해야 함
            message = "Hello World"
            result = {"output": message, "calculation": 2+2}
            result  # 이 값이 응답으로 반환됩니다
            ```

            Args:
                code: 실행할 Python 코드(반드시 값을 반환해야 결과 확인 가능)
                session_id: 상태 지속을 위한 세션 식별자

            Returns:
                반환된 값을 'output' 필드에 담아 표준 응답으로 감싼 결과
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
        """샌드박스 리셋/상태 조회 도구 등록."""

        @self.mcp.tool()
        async def reset_sandbox(
            session_id: str = Field(
                default='default', description='Session ID to reset'
            ),
        ) -> dict[str, Any]:
            """샌드박스 세션을 초기화하여 모든 상태를 제거합니다.

            Args:
                session_id: 초기화할 세션 식별자

            Returns:
                성공 여부 및 이전 세션 통계 정보
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
            """샌드박스 세션의 현재 상태를 조회합니다.

            Args:
                session_id: 조회할 세션 식별자

            Returns:
                변수 프리뷰와 세션 통계를 포함한 상태 정보
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
            """활성 샌드박스 세션 목록을 반환합니다.

            Returns:
                각 세션의 기본 통계를 포함한 목록
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
        """세션을 조회하거나 없으면 생성합니다.

        Args:
            session_id: 세션 식별자

        Returns:
            ``SandboxSession`` 인스턴스
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
        """타임아웃을 초과한 세션을 정리합니다."""
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
        """서버 종료 및 리소스 정리."""
        logger.info('Shutting down LangChain Sandbox MCP Server')

        # Clear all sessions
        self.sessions.clear()

        # Call parent shutdown
        await super().shutdown(timeout)


def main() -> None:
    """서버 실행 엔트리 포인트.

    커맨드라인 인자를 파싱하여 서버를 구성하고 실행합니다.
    """
    # argparse/uvicorn은 최상단에서 임포트됨

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
