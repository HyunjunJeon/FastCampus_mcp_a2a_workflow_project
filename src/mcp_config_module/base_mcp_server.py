"""**DO NOT UPDATE THIS FILE. ONLY HUMAN CAN UPDATE THIS FILE.**
MCP 서버들의 공통 베이스 클래스.
이 모듈은 모든 MCP 서버가 상속받아 사용할 수 있는 기본 클래스를 제공합니다.
"""  # noqa: D205

import asyncio
import logging

from abc import ABC, abstractmethod
from typing import Any, Literal, Never

from fastmcp import FastMCP
from fastmcp.server.http import StarletteWithLifespan
from pydantic import BaseModel, ConfigDict, Field
from starlette.requests import Request
from starlette.responses import JSONResponse


class StandardResponse(BaseModel):
    """표준화된 MCP Server 응답 모델.

    Attributes:
        success: 성공 여부.
        query: 원본 쿼리.
        data: 응답 데이터.
    """

    model_config = ConfigDict(
        extra='allow',
        arbitrary_types_allowed=True,
    )  # 추가 필드 허용 및 임의 타입 허용

    success: bool = Field(True, description='성공 여부 (항상 True)')
    query: str = Field(..., description='원본 쿼리')
    data: Any | None = Field(None, description='응답 데이터 (성공 시)')


class ErrorResponse(BaseModel):
    """표준 에러 MCP Server 응답 모델."""

    model_config = ConfigDict(extra='allow', arbitrary_types_allowed=True)

    success: bool = Field(False, description='성공 여부 (항상 False)')
    query: str = Field(..., description='원본 쿼리')
    error: str = Field(..., description='에러 메시지')
    func_name: str | None = Field(None, description='에러가 발생한 함수명')


class BaseMCPServer(ABC):
    """MCP 서버의 베이스 클래스.

    모든 MCP 서버가 공통으로 사용하는 기능을 제공하는 추상 베이스 클래스입니다.
    하위 클래스에서는 _initialize_clients()와 _register_tools()를 구현해야 합니다.
    """

    MCP_PATH = '/mcp'  # MCP 엔드포인트 기본 경로

    def __init__(
        self,
        server_name: str,
        port: int,
        host: str = '0.0.0.0',
        debug: bool = False,
        transport: Literal['streamable-http', 'stdio'] = 'streamable-http',
        server_instructions: str = '',
        json_response: bool = False,
        shutdown_timeout: float = 30.0,
        **kwargs
    ):
        """MCP 서버 초기화.

        Args:
            server_name: 서버 이름
            port: 서버 포트
            host: 호스트 주소 (기본값: "0.0.0.0")
            debug: 디버그 모드 (기본값: False)
            transport: MCP 전송 방식 (기본값: "streamable-http")
            server_instructions: 서버 설명 (기본값: "")
            json_response: JSON 응답 검증 여부 (기본값: False)
            shutdown_timeout: Graceful shutdown 타임아웃 (기본값: 30.0초)
            enable_middlewares: 활성화할 미들웨어 리스트 (예: ["logging", "timing", "rate_limiting"])
            middleware_config: 미들웨어별 설정 딕셔너리
        """
        # 서버 기본 설정 저장
        self.server_name = server_name
        self.host = host
        self.port = port
        self.debug = debug
        self.transport = transport
        self.server_instructions = server_instructions
        self.json_response = json_response
        self.shutdown_timeout = shutdown_timeout

        # kwargs에서 추가 설정값 추출
        self.enable_middlewares = kwargs.get('enable_middlewares', [])
        self.middleware_config = kwargs.get('middleware_config', {})

        # FastMCP 인스턴스 생성 - MCP 프로토콜 처리를 위한 핵심 객체
        self.mcp = FastMCP(name=server_name, instructions=server_instructions)

        # 로거 설정 (미들웨어보다 먼저 초기화하여 미들웨어 설정 중 로깅 가능)
        self.logger = logging.getLogger(self.__class__.__name__)

        # 미들웨어 설정 - 요청/응답 처리 파이프라인 구성
        self._setup_middlewares()

        # 백그라운드 태스크 추적을 위한 딕셔너리 초기화
        self._background_tasks: dict[str, asyncio.Task] = {}

        # 하위 클래스에서 구현한 클라이언트 초기화 호출
        self._initialize_clients()

        # 하위 클래스에서 구현한 도구 등록 호출
        self._register_tools()

    @abstractmethod
    def _initialize_clients(self) -> None:
        """클라이언트 인스턴스를 초기화합니다. 하위 클래스에서 구현해야 합니다."""
        raise NotImplementedError('Subclasses must implement this method')

    @abstractmethod
    def _register_tools(self) -> None:
        """MCP 도구들을 등록합니다. 하위 클래스에서 구현해야 합니다."""
        raise NotImplementedError('Subclasses must implement this method')

    def _setup_middlewares(self) -> None:
        """미들웨어를 설정하고 FastMCP에 등록합니다.

        활성화된 미들웨어 목록을 순회하면서 각 미들웨어를 생성하고 등록합니다.
        CORS는 Starlette의 CORSMiddleware를 사용하므로 여기서는 처리하지 않습니다.
        """
        if not self.enable_middlewares:
            return

        # 지원하는 미들웨어와 팩토리 메서드 매핑
        # CORS는 Starlette CORSMiddleware로 별도 처리하므로 제외
        middleware_classes = {
            'error_handling': self._get_error_handling_middleware,
            'logging': self._get_logging_middleware,
        }

        for middleware_name in self.enable_middlewares:
            try:
                # CORS는 Starlette CORSMiddleware로 처리하므로 건너뜀
                if middleware_name == 'cors':
                    self.logger.info(
                        'CORS middleware handled by Starlette CORSMiddleware'
                    )
                    continue

                # 지원하는 미들웨어인 경우 팩토리 메서드 호출
                if middleware_name in middleware_classes:
                    middleware_factory = middleware_classes[middleware_name]
                    middleware = middleware_factory()
                    if middleware:
                        # FastMCP에 미들웨어 추가
                        self.mcp.add_middleware(middleware)
                        self.logger.info(
                            f'Enabled {middleware_name} middleware'
                        )
                else:
                    # 알 수 없는 미들웨어 이름인 경우 경고
                    self.logger.warning(
                        f'Unknown middleware: {middleware_name}'
                    )
            except Exception as e:
                # 미들웨어 설정 실패 시 에러 로깅 (서버는 계속 동작)
                self.logger.error(
                    f'Failed to setup {middleware_name} middleware: {e}'
                )

    def _get_error_handling_middleware(self) -> Any:
        """ErrorHandling 미들웨어 생성.

        에러 처리 미들웨어를 생성하고 설정을 적용합니다.
        디버그 모드에서는 traceback을 포함하도록 설정됩니다.
        """
        try:
            from src.mcp_config_module.common.middleware import (
                ErrorHandlingMiddleware,
            )

            # 에러 핸들링 설정 가져오기
            config = self.middleware_config.get('error_handling', {})
            return ErrorHandlingMiddleware(
                # 디버그 모드일 때 traceback 포함
                include_traceback=config.get('include_traceback', self.debug),
                # 나머지 설정 전달 (include_traceback 제외)
                **{k: v for k, v in config.items() if k != 'include_traceback'},
            )
        except ImportError as e:
            # 미들웨어 모듈을 찾을 수 없는 경우
            self.logger.warning(f'ErrorHandling middleware not available: {e}')
            return None

    def _get_logging_middleware(self) -> Any:
        """Logging 미들웨어 생성.

        로깅 미들웨어를 생성하고 설정을 적용합니다.
        요청은 항상 로깅하고, 응답은 디버그 모드에서만 로깅합니다.
        """
        try:
            from src.mcp_config_module.common.middleware import (
                LoggingMiddleware,
            )

            # 로깅 설정 가져오기
            config = self.middleware_config.get('logging', {})
            return LoggingMiddleware(
                # 요청은 기본적으로 로깅
                log_requests=config.get('log_requests', True),
                # 응답은 디버그 모드에서만 로깅
                log_responses=config.get('log_responses', self.debug),
                # 나머지 설정 전달 (log_requests, log_responses 제외)
                **{
                    k: v
                    for k, v in config.items()
                    if k not in ['log_requests', 'log_responses']
                },
            )
        except ImportError as e:
            # 미들웨어 모듈을 찾을 수 없는 경우
            self.logger.warning(f'Logging middleware not available: {e}')
            return None

    def _get_cors_middleware(self) -> Never:
        """CORS 미들웨어는 이제 Starlette CORSMiddleware로 처리됩니다.

        create_app() 메서드에서 custom_middleware로 적용됩니다.
        """
        self.logger.info(
            'CORS is now handled by Starlette CORSMiddleware in create_app()'
        )
        raise NotImplementedError('CORS middleware is now handled by Starlette CORSMiddleware in create_app()')

    def get_enabled_middlewares(self) -> list[str]:
        """현재 활성화된 미들웨어 목록을 반환합니다.

        Returns:
            활성화된 미들웨어 이름 리스트
        """
        return self.enable_middlewares.copy()

    def is_middleware_enabled(self, middleware_name: str) -> bool:
        """특정 미들웨어가 활성화되어 있는지 확인합니다.

        Args:
            middleware_name: 확인할 미들웨어 이름

        Returns:
            미들웨어 활성화 여부
        """
        return middleware_name in self.enable_middlewares

    def create_standard_response(
        self,
        success: bool,
        query: str,
        data: Any = None,
        **kwargs,
    ) -> dict[str, Any]:
        """표준화된 응답 형식을 생성합니다.

        Args:
            success: 성공 여부
            query: 원본 쿼리
            data: 응답 데이터
            error: 에러 메시지 (실패 시)
            **kwargs: 추가 필드

        Returns:
            표준화된 응답 딕셔너리 (JSON 직렬화 가능)
        """
        response_model = StandardResponse(
            success=success,
            query=query,
            data=data,
            **kwargs,
        )

        return response_model.model_dump(exclude_none=True)

    def create_error_response(
        self,
        error: str,
        query: str | None = None,
        func_name: str | None = None,
        **kwargs,
    ) -> dict[str, Any]:
        """표준화된 에러 처리.

        Args:
            error: 발생한 에러 메시지
            query: 쿼리 문자열
            func_name: 함수 이름
            **kwargs: 추가 응답 데이터
            **context: 에러 컨텍스트 정보

        Returns:
            에러 응답 딕셔너리
        """
        # 에러 응답 데이터 구성
        error_model = ErrorResponse(
            success=False,
            query=str(query),
            error=str(error),
            func_name=func_name,
            **kwargs,
        )

        return error_model.model_dump(exclude_none=True)

    def create_background_task(
        self, coro: Any, name: str | None = None
    ) -> asyncio.Task:
        """백그라운드 태스크를 생성하고 추적합니다.

        Args:
            coro: 실행할 코루틴
            name: 태스크 이름 (디버깅 및 추적용)

        Returns:
            생성된 asyncio.Task 객체
        """
        # 비동기 태스크 생성
        task = asyncio.create_task(coro)

        # 태스크 이름 설정 (제공되지 않으면 태스크 ID 사용)
        task_name = name or f'task_{id(task)}'

        # 태스크 추적 딕셔너리에 추가하여 관리
        self._background_tasks[task_name] = task

        # 태스크 완료 시 자동 정리를 위한 콜백 함수
        def cleanup_callback(t: asyncio.Task) -> None:
            # 완료된 태스크를 추적 딕셔너리에서 제거
            self._background_tasks.pop(task_name, None)
            # 예외로 종료된 경우 에러 로깅
            if t.exception():
                self.logger.error(
                    f'Background task {task_name} failed with exception',
                    exc_info=t.exception(),
                )

        # 태스크 완료 시 콜백 함수 등록
        task.add_done_callback(cleanup_callback)

        self.logger.debug(f'Created background task: {task_name}')
        return task

    async def shutdown(self, timeout: float | None = None) -> None:
        """서버를 안전하게 종료합니다.

        Args:
            timeout: 종료 타임아웃 (초). None이면 초기화 시 설정된 값 사용

        Returns:
            종료 성공 여부
        """
        import sys

        await asyncio.sleep(float(timeout))
        self.logger.info(f'Shutting down {self.server_name}...')
        sys.exit(0)

    def get_active_tasks(self) -> list[str]:
        """현재 실행 중인 백그라운드 태스크 목록을 반환합니다.

        Returns:
            실행 중인 태스크 이름 목록
        """
        return [
            name
            for name, task in self._background_tasks.items()
            if not task.done()
        ]

    async def __aenter__(self) -> "BaseMCPServer":
        """비동기 컨텍스트 매니저 진입."""
        await self.lifecycle.start()
        return self

    async def __aexit__(self, exc_type: type | None, exc_val: Exception | None, exc_tb: Any) -> bool:
        """비동기 컨텍스트 매니저 종료 - 자동 정리."""
        await self.shutdown()
        return False

    def create_app(self) -> StarletteWithLifespan:
        """ASGI 앱을 생성합니다.

        - /health 라우트를 1회만 등록합니다.
        - FastMCP의 http_app을 반환합니다.
        - Starlette CORSMiddleware를 적용합니다.
        """
        # 헬스체크 라우트가 이미 등록되었는지 확인 (중복 등록 방지)
        if not getattr(self, '_health_route_registered', False):

            @self.mcp.custom_route(
                path='/health',
                methods=['GET', 'OPTIONS'],
                include_in_schema=True,
            )
            async def health_check(request: Request) -> JSONResponse:
                """Health check endpoint - CORS is handled by CORSMiddleware."""
                # 표준화된 성공 응답 생성
                response_data = self.create_standard_response(
                    success=True,
                    query='MCP Server Health check',
                    data='OK',
                )
                return JSONResponse(content=response_data)

            # 헬스체크 라우트 등록 완료 플래그 설정
            self._health_route_registered = True
            self.logger.info('Health check endpoint registered at /health')
            self.logger.info(
                f'Simple GET handler registered at {self.MCP_PATH}'
            )

        self.logger.info('Development CORS configured: allow all origins (*)')

        # FastMCP의 streamable_http_app 생성
        # 참고: streamable_http_app은 custom_middleware를 직접 지원하지 않음
        app = self.mcp.streamable_http_app(
            path=self.MCP_PATH,
        )

        # CORS 미들웨어를 Starlette 레벨에서 수동으로 추가
        from starlette.middleware.cors import CORSMiddleware

        # 개발 환경용 CORS 설정 - 모든 origin 허용
        # 프로덕션 환경에서는 보안을 위해 특정 origin만 허용해야 함
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],  # 모든 origin 허용
            allow_methods=['*'],  # 모든 HTTP 메서드 허용
            allow_headers=['*'],  # 모든 헤더 허용
            allow_credentials=False,  # 쿠키 전송 비활성화
            expose_headers=['*'],  # 모든 헤더 노출
            max_age=600,  # preflight 캐시 시간 (초)
        )

        return app


"""
**DO NOT UPDATE THIS FILE. ONLY HUMAN CAN UPDATE THIS FILE.**
"""
