"""FastMCP 미들웨어 컬렉션.

본 패키지는 MCP 서버에서 공통적으로 사용할 수 있는 미들웨어 구현을 제공합니다.
주요 구성 요소는 다음과 같습니다.

- ``CORSMiddleware``: CORS 정책 적용(Preflight 처리, 허용 Origin/메서드/헤더)
- ``ErrorHandlingMiddleware``: 예외 분류/로깅/표준 응답 변환
- ``LoggingMiddleware``: 구조화된 요청/응답/성능/감사 로깅

간단한 사용 예시:
    >>> from src.mcp_config_module.common.middleware import (
    ...     CORSMiddleware,
    ...     ErrorHandlingMiddleware,
    ...     LoggingMiddleware,
    ... )
    >>> cors = CORSMiddleware(allow_origins=["*"], allow_methods=["GET"], allow_headers=["*"])
    >>> errors = ErrorHandlingMiddleware(include_traceback=True)
    >>> logs = LoggingMiddleware()
    >>> # 서버 미들웨어 체인에 등록하여 사용
"""

from src.mcp_config_module.common.middleware.cors import CORSMiddleware
from src.mcp_config_module.common.middleware.error_handling import (
    ErrorHandlingMiddleware,
)
from src.mcp_config_module.common.middleware.logging import LoggingMiddleware


__all__ = [
    'CORSMiddleware',
    'ErrorHandlingMiddleware',
    'LoggingMiddleware',
]
