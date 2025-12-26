"""FastMCP 에러 핸들링 미들웨어.

이 모듈은 FastMCP 서버에 공통 적용할 수 있는 에러 처리 체계를 제공합니다.
핵심 목표는 다음과 같습니다.

- 예외를 일관된 구조의 응답으로 변환하여 클라이언트 UX를 개선합니다.
- 에러의 성격을 카테고리/심각도로 분류해 운영 관측성을 높입니다.
- 민감 정보 마스킹 및 선택적 traceback 포함으로 보안과 개발 편의를 균형 있게 유지합니다.

설계 의도 및 트레이드오프:
- 예외를 즉시 삼키지 않고, 필요 시 재발생시켜 상위 레이어에서 적절히 처리할 수
  있도록 구성했습니다.
- 운영 환경에서는 기본적으로 traceback을 숨기되, 개발 환경에서는 옵션으로 노출할 수
  있게 했습니다.

사용 예시:
    >>> from src.mcp_config_module.common.middleware.error_handling import (
    ...     create_development_error_handler,
    ... )
    >>> error_mw = create_development_error_handler()
    >>> # 서버 미들웨어 체인에 등록하여 사용
"""

import logging
import re
import traceback

from datetime import datetime
from enum import Enum
from typing import Any

from fastmcp.server.middleware import Middleware
from pydantic import BaseModel


logger = logging.getLogger(__name__)


class ErrorSeverity(str, Enum):
    """에러 심각도 분류.

    - LOW: 사용자 입력 오류 등 복구가 쉬운 경미한 오류
    - MEDIUM: 일시적 네트워크 문제 등 재시도 가능성이 있는 오류
    - HIGH: 권한 문제 등 즉각적인 조치가 필요한 오류
    - CRITICAL: 시스템 장애 수준의 치명적 오류
    """

    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'


class ErrorCategory(str, Enum):
    """에러 카테고리 분류.

    클라이언트/서버/외부 의존성 등 에러의 성격을 구분하여 관측과 대응을 용이하게
    합니다. 운영 대시보드/알림 시스템에서 카테고리별 집계를 할 때 유용합니다.
    """

    VALIDATION = 'validation'  # 입력 검증 에러
    AUTHENTICATION = 'authentication'  # 인증 에러
    AUTHORIZATION = 'authorization'  # 권한 에러
    RATE_LIMIT = 'rate_limit'  # 레이트 제한 에러
    EXTERNAL_API = 'external_api'  # 외부 API 에러
    NETWORK = 'network'  # 네트워크 에러
    DATABASE = 'database'  # 데이터베이스 에러
    BUSINESS_LOGIC = 'business_logic'  # 비즈니스 로직 에러
    SYSTEM = 'system'  # 시스템 에러
    UNKNOWN = 'unknown'  # 알 수 없는 에러


class ErrorInfo(BaseModel):
    """에러 정보 모델.

    표준화된 에러 응답 생성을 위해 에러의 메타데이터를 표현합니다.
    ``details``는 원본 예외 메시지 등 부가 정보를 담는 용도로 사용합니다.
    """

    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    user_message: str
    code: str | None = None
    details: dict[str, Any] | None = None
    retry_after: float | None = None


class ErrorHandlingMiddleware(Middleware):
    """FastMCP 에러 핸들링 미들웨어 구현체.

    기능 요약:
    - 도구 호출 및 리소스 접근 시 발생하는 예외를 분류/로깅/표준응답으로 변환
    - 개발/운영 환경에 따라 traceback 포함 여부와 마스킹 정책 제어
    - 사용자 정의 예외 매핑을 통해 도메인 특화 오류 모델링 지원
    """

    def __init__(
        self,
        include_traceback: bool = False,
        log_errors: bool = True,
        mask_sensitive_data: bool = True,
        custom_error_map: dict[type[Exception], ErrorInfo] | None = None,
        default_user_message: str = '처리 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.',
    ):
        """미들웨어 초기화 및 정책 구성.

        Args:
            include_traceback: 응답에 traceback을 포함할지 여부(개발 환경 권장)
            log_errors: 에러 발생 시 로깅 수행 여부
            mask_sensitive_data: 메시지/traceback에서 민감한 데이터 마스킹 여부
            custom_error_map: 사용자 정의 예외 → ``ErrorInfo`` 매핑 딕셔너리
            default_user_message: 분류되지 않은 예외에 대한 기본 사용자 메시지
        """
        super().__init__()

        self.include_traceback = include_traceback
        self.log_errors = log_errors
        self.mask_sensitive_data = mask_sensitive_data
        self.default_user_message = default_user_message

        # 기본 에러 매핑 설정
        self.error_map = self._create_default_error_map()

        # 사용자 정의 에러 매핑 추가
        if custom_error_map:
            self.error_map.update(custom_error_map)

        logger.info('Error handling middleware initialized')

    def _create_default_error_map(self) -> dict[type[Exception], ErrorInfo]:
        """기본 에러 매핑 생성.

        자주 발생하는 내장 예외에 대해 합리적인 기본 분류를 제공합니다.
        운영 환경에서는 이 매핑을 기반으로 알림 우선순위를 설정할 수 있습니다.
        """
        return {
            ValueError: ErrorInfo(
                category=ErrorCategory.VALIDATION,
                severity=ErrorSeverity.LOW,
                message='Invalid input value',
                user_message='입력값이 올바르지 않습니다.',
            ),
            KeyError: ErrorInfo(
                category=ErrorCategory.VALIDATION,
                severity=ErrorSeverity.LOW,
                message='Required field missing',
                user_message='필수 필드가 누락되었습니다.',
            ),
            ConnectionError: ErrorInfo(
                category=ErrorCategory.NETWORK,
                severity=ErrorSeverity.MEDIUM,
                message='Network connection failed',
                user_message='네트워크 연결에 실패했습니다.',
                retry_after=5.0,
            ),
            TimeoutError: ErrorInfo(
                category=ErrorCategory.NETWORK,
                severity=ErrorSeverity.MEDIUM,
                message='Request timeout',
                user_message='요청 시간이 초과되었습니다.',
                retry_after=10.0,
            ),
            PermissionError: ErrorInfo(
                category=ErrorCategory.AUTHORIZATION,
                severity=ErrorSeverity.HIGH,
                message='Permission denied',
                user_message='접근 권한이 없습니다.',
            ),
            FileNotFoundError: ErrorInfo(
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.MEDIUM,
                message='Required resource not found',
                user_message='요청한 리소스를 찾을 수 없습니다.',
            ),
            MemoryError: ErrorInfo(
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.CRITICAL,
                message='Out of memory',
                user_message='시스템 리소스 부족으로 요청을 처리할 수 없습니다.',
            ),
        }

    def _classify_error(self, error: Exception) -> ErrorInfo:
        """예외 객체를 적절한 ``ErrorInfo``로 변환합니다.

        우선순위:
        1) 정확한 예외 타입 매칭
        2) 부모 클래스 매칭
        3) 기본(UNKNOWN) 매핑
        """
        error_type = type(error)

        # 직접 매칭
        if error_type in self.error_map:
            error_info = self.error_map[error_type].model_copy()
        else:
            # 부모 클래스 매칭
            for exc_type, info in self.error_map.items():
                if issubclass(error_type, exc_type):
                    error_info = info.model_copy()
                    break
            else:
                # 기본 에러 정보
                error_info = ErrorInfo(
                    category=ErrorCategory.UNKNOWN,
                    severity=ErrorSeverity.MEDIUM,
                    message=str(error),
                    user_message=self.default_user_message,
                )

        # 에러 메시지 업데이트
        if str(error) and str(error) != error_info.message:
            error_info.details = {'original_message': str(error)}

        return error_info

    def _mask_sensitive_data(self, data: str) -> str:
        """민감한 데이터 마스킹.

        정규식을 사용하여 패스워드/토큰/API 키 등의 노출을 방지합니다.
        운영 로깅/알림에 그대로 전달되지 않도록 반드시 적용합니다.
        """
        if not self.mask_sensitive_data:
            return data

        # 패스워드, 토큰, API 키 등 마스킹
        patterns = [
            (r'("password"\s*:\s*")[^"]+(")', r'\1***\2'),
            (r'("token"\s*:\s*")[^"]+(")', r'\1***\2'),
            (r'("api_key"\s*:\s*")[^"]+(")', r'\1***\2'),
            (r'("secret"\s*:\s*")[^"]+(")', r'\1***\2'),
            (r'(Authorization:\s*Bearer\s+)[^\s]+', r'\1***'),
            (r'(password=)[^\s&]+', r'\1***'),
        ]

        masked_data = data
        for pattern, replacement in patterns:
            masked_data = re.sub(
                pattern, replacement, masked_data, flags=re.IGNORECASE
            )

        return masked_data

    def _create_error_response(
        self, error: Exception, error_info: ErrorInfo, context: dict[str, Any]
    ) -> dict[str, Any]:
        """표준화된 에러 응답 생성.

        반환 스키마는 클라이언트가 일관되게 처리할 수 있도록 최소 필수 항목을
        포함합니다. 운영 환경에서는 사용자 메시지 중심으로 노출되며, 내부 상세는
        ``error_details``에 담깁니다.
        """
        response = {
            'success': False,
            'error': error_info.user_message,
            'error_details': {
                'category': error_info.category.value,
                'severity': error_info.severity.value,
                'timestamp': datetime.now().isoformat(),
                'type': type(error).__name__,
            },
        }

        # 에러 코드 추가
        if error_info.code:
            response['error_details']['code'] = error_info.code

        # 재시도 정보 추가
        if error_info.retry_after:
            response['retry_after'] = error_info.retry_after

        # 상세 정보 추가
        if error_info.details:
            response['error_details']['details'] = error_info.details

        # 개발 환경에서 traceback 포함
        if self.include_traceback:
            tb = traceback.format_exception(
                type(error), error, error.__traceback__
            )
            response['error_details']['traceback'] = self._mask_sensitive_data(
                ''.join(tb)
            )

        # 컨텍스트 정보 추가 (민감한 정보 제외)
        safe_context = {}
        for key, value in context.items():
            if key not in ['password', 'token', 'api_key', 'secret']:
                safe_context[key] = value

        if safe_context:
            response['error_details']['context'] = safe_context

        return response

    def _log_error(
        self, error: Exception, error_info: ErrorInfo, context: dict[str, Any]
    ) -> None:
        """에러 로깅.

        심각도에 따라 로그 레벨을 동적으로 선택하며, 개발 모드에서는 traceback을
        함께 출력합니다.
        """
        if not self.log_errors:
            return

        log_level = {
            ErrorSeverity.LOW: logging.INFO,
            ErrorSeverity.MEDIUM: logging.WARNING,
            ErrorSeverity.HIGH: logging.ERROR,
            ErrorSeverity.CRITICAL: logging.CRITICAL,
        }.get(error_info.severity, logging.ERROR)

        log_message = (
            f'[{error_info.category.value.upper()}] {error_info.message} | '
            f'Type: {type(error).__name__} | Context: {context}'
        )

        if self.include_traceback:
            logger.log(log_level, log_message, exc_info=True)
        else:
            logger.log(log_level, log_message)

    async def call_tool(
        self,
        call_next: Any,
        tool_name: str,
        arguments: dict[str, Any],
        **context,
    ) -> Any:
        """도구 호출 시 에러 처리.

        예외 발생 시 즉시 분류/로깅 후 표준 응답을 반환합니다. 이는 미들웨어 체인의
        일관된 오류 처리를 보장하여, 개별 도구 구현의 예외 누락으로 인한 누수를
        방지합니다.
        """
        try:
            return await call_next(tool_name, arguments, **context)
        except Exception as error:
            # 에러 분류 및 정보 추출
            error_info = self._classify_error(error)

            # 컨텍스트 정보
            error_context = {
                'tool_name': tool_name,
                'arguments_count': len(arguments),
                **context,
            }

            # 에러 로깅
            self._log_error(error, error_info, error_context)

            # 표준화된 에러 응답 반환
            return self._create_error_response(error, error_info, error_context)

    async def get_resource(
        self, call_next: Any, resource_uri: str, **context
    ) -> Any:
        """리소스 접근 시 에러 처리.

        리소스 접근은 상위 레이어에서 구체적으로 처리해야 할 경우가 많아,
        표준 응답 대신 예외를 재발생시켜 호출자가 흐름을 제어하도록 합니다.
        """
        try:
            return await call_next(resource_uri, **context)
        except Exception as error:
            # 에러 분류 및 정보 추출
            error_info = self._classify_error(error)

            # 컨텍스트 정보
            error_context = {'resource_uri': resource_uri, **context}

            # 에러 로깅
            self._log_error(error, error_info, error_context)

            # 에러 재발생 (리소스 에러는 예외로 처리)
            raise Exception(
                f'[{error_info.category.value}] {error_info.user_message}'
            ) from error

    def add_error_mapping(
        self, exception_type: type[Exception], error_info: ErrorInfo
    ) -> None:
        """사용자 정의 에러 매핑 추가.

        도메인 고유의 예외 타입을 운영 기준에 맞춰 ``ErrorInfo``로 맵핑할 수
        있습니다.
        """
        self.error_map[exception_type] = error_info

    def get_error_stats(self) -> dict[str, Any]:
        """에러 통계 정보 (향후 구현).

        TODO: 중앙화 로깅/메트릭 시스템과 연계하여 누적 집계를 제공합니다.
        """
        return {
            'total_errors': 0,  # 구현 예정
            'by_category': {},  # 구현 예정
            'by_severity': {},  # 구현 예정
        }


# 편의 함수들


def create_development_error_handler() -> ErrorHandlingMiddleware:
    """개발 환경용 에러 핸들러 (traceback 포함).

    개발 중 원인 분석을 빠르게 하기 위해 traceback을 응답/로그에 포함합니다.
    """
    return ErrorHandlingMiddleware(
        include_traceback=True,
        log_errors=True,
        mask_sensitive_data=True,
    )


def create_production_error_handler() -> ErrorHandlingMiddleware:
    """운영 환경용 에러 핸들러 (보안 강화).

    사용자 노출을 최소화하는 메시지를 사용하고, 민감 정보는 마스킹합니다.
    """
    return ErrorHandlingMiddleware(
        include_traceback=False,
        log_errors=True,
        mask_sensitive_data=True,
        default_user_message='일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.',
    )


def create_api_error_handler() -> ErrorHandlingMiddleware:
    """API 서버용 에러 핸들러.

    API 호출 시 자주 발생하는 케이스에 맞춘 에러 매핑을 제공합니다.
    재시도 힌트(``retry_after``)를 통해 클라이언트의 백오프 전략 수립을 돕습니다.
    """
    # API 전용 에러 매핑
    api_error_map = {
        ValueError: ErrorInfo(
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.LOW,
            message='Invalid parameter',
            user_message='요청 파라미터가 올바르지 않습니다.',
            code='INVALID_PARAMETER',
        ),
        ConnectionError: ErrorInfo(
            category=ErrorCategory.EXTERNAL_API,
            severity=ErrorSeverity.MEDIUM,
            message='External API connection failed',
            user_message='외부 서비스 연결에 실패했습니다.',
            code='EXTERNAL_API_ERROR',
            retry_after=30.0,
        ),
    }

    return ErrorHandlingMiddleware(
        include_traceback=False,
        log_errors=True,
        mask_sensitive_data=True,
        custom_error_map=api_error_map,
    )
