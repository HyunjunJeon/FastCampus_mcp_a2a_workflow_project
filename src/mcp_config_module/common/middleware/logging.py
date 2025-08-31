"""FastMCP 로깅 미들웨어.

이 모듈은 FastMCP 서버에서 요청/응답 로깅, 성능 메트릭, 감사 로그를
구조화된 형태로 수집하기 위한 미들웨어를 제공합니다.

설계 의도:
- 구조화된 로깅(structlog) 기본값을 채택하여 운영 환경에서의 검색/집계를 개선합니다.
- 성능 임계치 기반의 느린 호출 감지와 감사 로그를 옵션으로 제공합니다.

사용 예시:
    >>> from src.mcp_config_module.common.middleware.logging import create_debug_logger
    >>> log_mw = create_debug_logger()
    >>> # 서버 미들웨어 체인에 등록하여 사용
"""

import json
import logging
import time

from datetime import datetime
from enum import Enum
from typing import Any

import structlog

from fastmcp.server.middleware import Middleware


# Structured logging 설정
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt='iso'),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(ensure_ascii=False),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


class LogLevel(str, Enum):
    """로그 레벨 정의.

    Python 표준 로깅 레벨과 동일한 문자열 값을 사용합니다.
    """

    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class LoggingMiddleware(Middleware):
    """FastMCP 로깅 미들웨어 구현체.

    기능 요약:
    - 도구 호출/리소스 접근의 요청·응답·에러를 구조화하여 로깅
    - 실행 시간/응답 크기 등 기본 성능 지표 기록 및 느린 호출 경고
    - 감사 로그(Audit Trail) 옵션 제공
    """

    # Performance thresholds
    SLOW_EXECUTION_THRESHOLD = 5.0  # 5 seconds

    def __init__(
        self,
        log_level: LogLevel = LogLevel.INFO,
        log_requests: bool = True,
        log_responses: bool = True,
        log_performance: bool = True,
        log_errors: bool = True,
        **kwargs
    ):
        """로깅 미들웨어 초기화 및 정책 구성.

        Args:
            log_level: 최소 로그 레벨
            log_requests: 요청 로깅 여부
            log_responses: 응답 로깅 여부
            log_performance: 성능 메트릭 로깅 여부
            log_errors: 에러 로깅 여부
            mask_sensitive_fields: 마스킹할 필드명 집합
            max_response_length: 응답 로그 최대 길이
            include_arguments: 요청 인수 로깅 여부
            include_context: 컨텍스트 로깅 여부
            audit_trail: 감사 로그 생성 여부
            structured_logging: 구조화된 로깅 사용 여부
            **kwargs: 추가 로깅 동작을 제어하는 선택적 설정 값들
        """
        super().__init__()

        self.log_level = log_level
        self.log_requests = log_requests
        self.log_responses = log_responses
        self.log_performance = log_performance
        self.log_errors = log_errors

        # kwargs에서 추가 설정값 추출
        self.mask_sensitive_fields = kwargs.get('mask_sensitive_fields', set())
        self.max_response_length = kwargs.get('max_response_length', 1000)
        self.include_arguments = kwargs.get('include_arguments', True)
        self.include_context = kwargs.get('include_context', True)
        self.audit_trail = kwargs.get('audit_trail', False)
        self.structured_logging = kwargs.get('structured_logging', True)

        # 민감한 필드 목록 설정
        default_sensitive_fields = {
            'password',
            'passwd',
            'pwd',
            'secret',
            'token',
            'api_key',
            'apikey',
            'auth',
            'authorization',
            'credential',
            'private_key',
            'access_token',
            'refresh_token',
            'session_id',
        }

        if self.mask_sensitive_fields:
            self.sensitive_fields = default_sensitive_fields.union(
                self.mask_sensitive_fields
            )
        else:
            self.sensitive_fields = default_sensitive_fields

        # 로거 설정
        if self.structured_logging:
            self.logger = structlog.get_logger(__name__)
        else:
            self.logger = logging.getLogger(__name__)

        self.logger.info(
            'Logging middleware initialized',
            log_level=self.log_level.value,
            structured=self.structured_logging,
        )

    def _mask_sensitive_data(self, data: Any) -> Any:
        """민감한 데이터 마스킹.

        딕셔너리/리스트 내의 지정된 필드명을 ``***MASKED***``로 치환합니다.
        중첩 구조는 재귀적으로 처리합니다.
        """
        if isinstance(data, dict):
            masked_data = {}
            for key, value in data.items():
                if key.lower() in self.sensitive_fields:
                    masked_data[key] = '***MASKED***'
                elif isinstance(value, dict | list):
                    masked_data[key] = self._mask_sensitive_data(value)
                else:
                    masked_data[key] = value
            return masked_data
        if isinstance(data, list):
            return [self._mask_sensitive_data(item) for item in data]
        return data

    def _truncate_response(self, response: Any) -> Any:
        """응답 데이터 크기 제한.

        과도한 로그 크기로 인한 성능 저하와 개인정보 노출 위험을 줄이기 위해
        최대 길이를 초과할 경우 프리뷰만 남기고 잘라냅니다.
        """
        if not isinstance(response, str | dict | list):
            return response

        response_str = (
            json.dumps(response, ensure_ascii=False)
            if not isinstance(response, str)
            else response
        )

        if len(response_str) > self.max_response_length:
            if isinstance(response, dict):
                return {
                    'truncated': True,
                    'original_length': len(response_str),
                    'preview': response_str[: self.max_response_length // 2],
                    'message': f'응답이 {self.max_response_length}자를 초과하여 잘렸습니다.',
                }
            return (
                f'{response_str[: self.max_response_length]}... [TRUNCATED]'
            )

        return response

    def _create_log_entry(self, event_type: str, **kwargs) -> dict:
        """표준화된 로그 엔트리 생성.

        공통 타임스탬프/서버 타입 필드를 포함하고, 민감한 데이터를 마스킹합니다.
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'server_type': 'mcp_server',
            **kwargs,
        }

        # 민감한 데이터 마스킹
        return self._mask_sensitive_data(log_entry)

    async def call_tool(
        self, call_next: Any, tool_name: str, arguments: dict[str, Any], **context
    ) -> Any:
        """도구 호출 시 로깅.

        요청/응답/성능/에러/감사 로그를 정책에 따라 수집합니다.
        느린 실행은 경고 레벨로 기록합니다.
        """
        start_time = time.time()
        request_id = context.get('request_id', f'req_{int(start_time * 1000)}')

        # 요청 로깅
        if self.log_requests:
            log_data = self._create_log_entry(
                event_type='tool_request',
                request_id=request_id,
                tool_name=tool_name,
                arguments=self._mask_sensitive_data(arguments)
                if self.include_arguments
                else {'count': len(arguments)},
                context=self._mask_sensitive_data(context)
                if self.include_context
                else {'keys': list(context.keys())},
            )

            self.logger.info('Tool request received', **log_data)

        try:
            # 다음 미들웨어 또는 도구 실행
            result = await call_next(tool_name, arguments, **context)

            # 실행 시간 계산
            execution_time = time.time() - start_time

            # 성공 응답 로깅
            if self.log_responses:
                log_data = self._create_log_entry(
                    event_type='tool_response',
                    request_id=request_id,
                    tool_name=tool_name,
                    status='success',
                    execution_time=execution_time,
                    response=self._truncate_response(result)
                    if result
                    else None,
                )

                self.logger.info('Tool executed successfully', **log_data)

            # 성능 메트릭 로깅
            if self.log_performance:
                perf_data = self._create_log_entry(
                    event_type='performance_metric',
                    request_id=request_id,
                    tool_name=tool_name,
                    execution_time=execution_time,
                    response_size=len(str(result)) if result else 0,
                )

                # 느린 요청 경고
                if execution_time > self.SLOW_EXECUTION_THRESHOLD:
                    self.logger.warning(
                        'Slow tool execution detected', **perf_data
                    )
                else:
                    self.logger.debug('Performance metric', **perf_data)

            # 감사 로그
            if self.audit_trail:
                audit_data = self._create_log_entry(
                    event_type='audit_log',
                    request_id=request_id,
                    tool_name=tool_name,
                    action='tool_executed',
                    status='success',
                    user_id=context.get('user_id', 'anonymous'),
                    timestamp=datetime.now().isoformat(),
                )

                self.logger.info('Audit trail', **audit_data)

            return result

        except Exception as error:
            execution_time = time.time() - start_time

            # 에러 로깅
            if self.log_errors:
                error_data = self._create_log_entry(
                    event_type='tool_error',
                    request_id=request_id,
                    tool_name=tool_name,
                    status='error',
                    execution_time=execution_time,
                    error_type=type(error).__name__,
                    error_message=str(error),
                )

                self.logger.error('Tool execution failed', **error_data)

            # 감사 로그 (에러)
            if self.audit_trail:
                audit_data = self._create_log_entry(
                    event_type='audit_log',
                    request_id=request_id,
                    tool_name=tool_name,
                    action='tool_executed',
                    status='error',
                    error=str(error),
                    user_id=context.get('user_id', 'anonymous'),
                )

                self.logger.error('Audit trail - error', **audit_data)

            # 에러 재발생
            raise

    async def get_resource(
        self, call_next: Any, resource_uri: str, **context
    ) -> Any:
        """리소스 접근 시 로깅.

        리소스 접근 요청과 결과를 구조화하여 기록합니다.
        """
        start_time = time.time()
        request_id = context.get('request_id', f'res_{int(start_time * 1000)}')

        # 요청 로깅
        if self.log_requests:
            log_data = self._create_log_entry(
                event_type='resource_request',
                request_id=request_id,
                resource_uri=resource_uri,
                context=self._mask_sensitive_data(context)
                if self.include_context
                else {'keys': list(context.keys())},
            )

            self.logger.info('Resource request received', **log_data)

        try:
            # 다음 미들웨어 또는 리소스 처리
            result = await call_next(resource_uri, **context)

            execution_time = time.time() - start_time

            # 성공 응답 로깅
            if self.log_responses:
                log_data = self._create_log_entry(
                    event_type='resource_response',
                    request_id=request_id,
                    resource_uri=resource_uri,
                    status='success',
                    execution_time=execution_time,
                    response_size=len(str(result)) if result else 0,
                )

                self.logger.info('Resource accessed successfully', **log_data)

            # 감사 로그
            if self.audit_trail:
                audit_data = self._create_log_entry(
                    event_type='audit_log',
                    request_id=request_id,
                    resource_uri=resource_uri,
                    action='resource_accessed',
                    status='success',
                    user_id=context.get('user_id', 'anonymous'),
                )

                self.logger.info('Audit trail', **audit_data)

            return result

        except Exception as error:
            execution_time = time.time() - start_time

            # 에러 로깅
            if self.log_errors:
                error_data = self._create_log_entry(
                    event_type='resource_error',
                    request_id=request_id,
                    resource_uri=resource_uri,
                    status='error',
                    execution_time=execution_time,
                    error_type=type(error).__name__,
                    error_message=str(error),
                )

                self.logger.error('Resource access failed', **error_data)

            # 에러 재발생
            raise

    def get_log_stats(self) -> dict:
        """로깅 통계 정보.

        현재 설정된 기능 플래그와 민감 필드 개수 등 요약 정보를 제공합니다.
        """
        return {
            'log_level': self.log_level.value,
            'structured_logging': self.structured_logging,
            'features': {
                'requests': self.log_requests,
                'responses': self.log_responses,
                'performance': self.log_performance,
                'errors': self.log_errors,
                'audit_trail': self.audit_trail,
            },
            'sensitive_fields_count': len(self.sensitive_fields),
        }


# 편의 함수들


def create_debug_logger() -> LoggingMiddleware:
    """디버그용 상세 로깅.

    개발 환경에서 요청/응답/성능/에러를 모두 수집합니다.
    """
    return LoggingMiddleware(
        log_level=LogLevel.DEBUG,
        log_requests=True,
        log_responses=True,
        log_performance=True,
        log_errors=True,
        include_arguments=True,
        include_context=True,
        max_response_length=5000,
        structured_logging=True,
    )


def create_production_logger() -> LoggingMiddleware:
    """운영환경용 로깅 (보안 강화).

    응답 본문 로깅을 비활성화하고, 인수/컨텍스트 로깅을 제한합니다.
    감사 로그를 활성화하여 추적성을 확보합니다.
    """
    return LoggingMiddleware(
        log_level=LogLevel.INFO,
        log_requests=True,
        log_responses=False,  # 운영환경에서는 응답 로깅 비활성화
        log_performance=True,
        log_errors=True,
        include_arguments=False,  # 보안상 인수 로깅 비활성화
        include_context=False,
        max_response_length=500,
        audit_trail=True,
        structured_logging=True,
    )


def create_performance_logger() -> LoggingMiddleware:
    """성능 모니터링 전용 로거.

    오버헤드를 최소화하여 성능 지표만 수집합니다.
    """
    return LoggingMiddleware(
        log_level=LogLevel.INFO,
        log_requests=False,
        log_responses=False,
        log_performance=True,
        log_errors=True,
        include_arguments=False,
        include_context=False,
        audit_trail=False,
        structured_logging=True,
    )


def create_audit_logger() -> LoggingMiddleware:
    """감사 로그 전용 로거.

    접근 행위를 장기 보관이 용이한 구조로 기록합니다.
    """
    return LoggingMiddleware(
        log_level=LogLevel.INFO,
        log_requests=True,
        log_responses=False,
        log_performance=False,
        log_errors=True,
        include_arguments=False,
        include_context=True,
        audit_trail=True,
        structured_logging=True,
    )
