"""FastMCP CORS 미들웨어.

이 모듈은 FastMCP 서버에서 CORS(Cross-Origin Resource Sharing)를 처리하기 위한
경량 미들웨어를 제공합니다. 허용할 Origin, HTTP 메서드, 헤더를 세밀하게 설정하여
브라우저 기반 클라이언트가 교차 출처 요청을 보낼 수 있도록 안전하게 제어합니다.

설계 배경 및 트레이드오프:
- Starlette/FastAPI의 CORS 미들웨어와 유사한 정책을 따르되, FastMCP 미들웨어
  인터페이스에 맞춰 최소 의존성으로 구현했습니다.
- 보안 상의 이유로, 와일드카드("*")를 허용하면 자격 증명(쿠키/인증 헤더)을
  허용하지 않도록 합니다. 본 구현은 특정 Origin에 한해서만
  ``Access-Control-Allow-Credentials`` 헤더를 추가합니다.

사용 예시:
    >>> from src.mcp_config_module.common.middleware.cors import create_cors_middleware
    >>> cors = create_cors_middleware(preset="development")
    >>> # 서버 미들웨어 체인에 등록하여 사용
"""

import logging
import traceback

from fastmcp.server.middleware import Middleware


logger = logging.getLogger(__name__)


class CORSMiddleware(Middleware):
    """CORS 처리를 담당하는 미들웨어.

    본 미들웨어는 다음과 같은 역할을 수행합니다.
    - 사전 점검(Preflight, OPTIONS) 요청에 대한 표준 응답 생성
    - 허용되지 않은 Origin에 대한 차단 및 표준화된 에러 반환
    - 정상 요청/응답에 CORS 관련 헤더 자동 부착

    보안 고려 사항:
    - 운영 환경에서는 가능한 구체적인 도메인만 허용하도록 권장합니다.
    - 민감한 엔드포인트는 별도의 인증/인가 계층과 함께 사용해야 합니다.
    """

    def __init__(
        self,
        allow_origins: list[str],
        allow_methods: list[str],
        allow_headers: list[str],
    ):
        """CORS 미들웨어 초기화.

        Args:
            allow_origins: 허용할 Origin의 화이트리스트.
                "*"가 포함되면 모든 Origin을 허용합니다.
            allow_methods: 허용할 HTTP 메서드 목록. 예: ["GET", "POST", ...]
            allow_headers: 허용할 사용자 지정 헤더 목록. 예: ["Authorization", ...]

        Notes:
            - 와일드카드 Origin("*") 사용 시, 브라우저가 인증 정보를 포함한 요청과
              함께 사용할 수 없으므로, 자격 증명 허용은 특정 Origin에 한해 적용됩니다.
        """
        super().__init__()

        self.allow_origins = allow_origins
        self.allow_methods = allow_methods
        self.allow_headers = allow_headers

        logger.info('CORS middleware initialized')

    def _is_origin_allowed(self, origin: str) -> bool:
        """요청 Origin 허용 여부를 판단합니다.

        Args:
            origin: 요청에서 추출한 Origin 문자열

        Returns:
            주어진 Origin이 허용 목록에 포함되면 ``True``. 와일드카드("*")가 허용
            목록에 포함되어 있으면 무조건 ``True``.

        Rationale:
            - 운영 환경에서는 와일드카드보다 명시적 Origin 제한이 보안상 안전합니다.
        """
        if '*' in self.allow_origins:
            return True

        return origin in self.allow_origins

    def _add_cors_headers(
        self, response_headers: dict, origin: str | None = None
    ) -> dict:
        """응답 헤더에 CORS 관련 표준 헤더를 병합합니다.

        Args:
            response_headers: 기존 응답 헤더 딕셔너리
            origin: 요청 Origin. 특정 Origin일 때만 자격 증명 허용 헤더를 추가합니다.

        Returns:
            CORS 헤더가 병합된 새로운 헤더 딕셔너리

        Notes:
            - ``Access-Control-Allow-Origin``은 요청 Origin이 허용 목록에 있을 때
              해당 Origin으로 설정되고, 그렇지 않으면 와일드카드가 설정됩니다.
            - ``Access-Control-Allow-Credentials``는 보안상 특정 Origin에만 추가합니다.
        """
        cors_headers = response_headers.copy()

        # Access-Control-Allow-Origin 헤더 설정
        if origin and self._is_origin_allowed(origin):
            cors_headers['Access-Control-Allow-Origin'] = origin
        elif '*' in self.allow_origins:
            cors_headers['Access-Control-Allow-Origin'] = '*'

        # Access-Control-Allow-Methods 헤더 설정
        cors_headers['Access-Control-Allow-Methods'] = ', '.join(
            self.allow_methods
        )

        # Access-Control-Allow-Headers 헤더 설정
        cors_headers['Access-Control-Allow-Headers'] = ', '.join(
            self.allow_headers
        )

        # 자격 증명 허용 설정 (보안: 특정 Origin에 한해서만 허용)
        if origin and origin in self.allow_origins:
            cors_headers['Access-Control-Allow-Credentials'] = 'true'

        return cors_headers

    async def process_request(self, request: dict) -> dict:
        """요청 전처리 단계에서 CORS Preflight를 처리합니다.

        Args:
            request: FastMCP 요청 컨텍스트 딕셔너리

        Returns:
            - Preflight(OPTIONS) 요청인 경우, 즉시 성공 응답(dict)을 반환합니다.
            - 그 외에는 요청을 그대로(일부 CORS 메타 추가 후) 반환합니다.

        Behavior:
            - ``Access-Control-Request-Method`` 헤더가 존재하는 OPTIONS 요청을
              Preflight로 간주합니다.
            - 허용되지 않은 Origin은 즉시 오류(response-like dict)로 응답합니다.
        """
        try:
            method = request.get('method', '').upper()
            headers = request.get('headers', {})
            origin = headers.get('origin', headers.get('Origin'))

            logger.debug(
                f'Processing CORS request: method={method}, origin={origin}'
            )

            # OPTIONS 메서드이고 Access-Control-Request-Method 가 있으면 Preflight
            if method == 'OPTIONS' and origin:
                # Access-Control-Request-Method 헤더가 있으면 preflight 요청
                request_method = headers.get(
                    'access-control-request-method'
                ) or headers.get('Access-Control-Request-Method')

                if request_method:
                    logger.info(
                        f'Handling CORS preflight request from {origin}'
                    )

                    # Origin 검증: 허용되지 않으면 보안상 즉시 차단
                    if not self._is_origin_allowed(origin):
                        logger.warning(
                            f'CORS preflight rejected: origin {origin} not allowed'
                        )
                        return {
                            'id': request.get('id'),
                            'error': {
                                'code': -32000,
                                'message': 'CORS: Origin not allowed',
                            },
                        }

                    # Preflight 응답 생성: 본문 없이 헤더만으로 허용 정책 전달 가능
                    response_headers = self._add_cors_headers({}, origin)

                    return {
                        'id': request.get('id'),
                        'result': {
                            'status': 'OK',
                            'message': 'CORS preflight successful',
                        },
                        'headers': response_headers,
                    }

            # 일반 요청의 경우에도 Origin을 검증하여 조기 차단
            if origin and not self._is_origin_allowed(origin):
                logger.warning(
                    f'CORS request rejected: origin {origin} not allowed'
                )
                return {
                    'id': request.get('id'),
                    'error': {
                        'code': -32000,
                        'message': 'CORS: Origin not allowed',
                    },
                }

            # 이후 응답 단계에서 재사용할 수 있도록 CORS 메타데이터 저장
            request['_cors_origin'] = origin

            return request

        except Exception as e:
            logger.error(f'Error processing CORS request: {e}')
            logger.debug(traceback.format_exc())
            return request

    async def process_response(self, request: dict, response: dict) -> dict:
        """응답 후처리 단계에서 CORS 헤더를 부착합니다.

        Args:
            request: 원본 요청 딕셔너리 (``_cors_origin`` 메타가 포함될 수 있음)
            response: 핸들러/도구 실행 결과 응답 딕셔너리

        Returns:
            CORS 표준 헤더가 병합된 응답 딕셔너리
        """
        try:
            origin = request.get('_cors_origin')

            if origin:
                logger.debug(
                    f'Adding CORS headers to response for origin: {origin}'
                )

                # 기존 헤더 가져오기 (있으면 유지하며 병합)
                existing_headers = response.get('headers', {})

                # CORS 헤더 추가
                cors_headers = self._add_cors_headers(existing_headers, origin)
                response['headers'] = cors_headers

            return response

        except Exception as e:
            logger.error(f'Error processing CORS response: {e}')
            logger.debug(traceback.format_exc())
            return response

    def get_middleware_info(self) -> dict:
        """미들웨어 메타정보를 반환합니다.

        Returns:
            미들웨어 이름, 버전, 설명, 구성 값이 포함된 딕셔너리
        """
        return {
            'name': 'CORSMiddleware',
            'version': '1.0.0',
            'description': 'FastMCP CORS Middleware for cross-origin requests',
            'config': {
                'allow_origins': self.allow_origins,
                'allow_methods': self.allow_methods,
                'allow_headers': self.allow_headers,
            },
        }


# 편의를 위한 사전 정의된 CORS 설정
class CORSConfig:
    """CORS 설정에 사용할 사전 정의 프리셋 모음.

    - DEVELOPMENT: 로컬/개발 환경용. 빠른 개발을 위해 모든 Origin 허용.
    - PRODUCTION: 운영 환경 기본값. 반드시 Origin 화이트리스트를 설정해야 안전.
    - API_ONLY: API 서버 특화. 일반적으로 필요한 메서드/헤더만 노출.
    """

    # 개발 환경용 - 모든 origin 허용
    DEVELOPMENT = {
        'allow_origins': ['*'],
        'allow_methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
        'allow_headers': [
            'Content-Type',
            'Authorization',
            'X-Requested-With',
            'Accept',
            'Origin',
            'Access-Control-Request-Method',
            'Access-Control-Request-Headers',
        ],
    }

    # 프로덕션 환경용 - 특정 origin만 허용
    PRODUCTION = {
        'allow_origins': [],  # 사용자가 설정해야 함
        'allow_methods': ['GET', 'POST', 'OPTIONS'],
        'allow_headers': [
            'Content-Type',
            'Authorization',
            'X-Requested-With',
            'Accept',
        ],
    }

    # API 전용 - RESTful API에 적합
    API_ONLY = {
        'allow_origins': [],  # 사용자가 설정해야 함
        'allow_methods': ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
        'allow_headers': [
            'Content-Type',
            'Authorization',
            'X-API-Key',
            'Accept',
        ],
    }


def create_cors_middleware(
    allow_origins: list[str] | None = None,
    allow_methods: list[str] | None = None,
    allow_headers: list[str] | None = None,
    preset: str | None = None,
) -> CORSMiddleware:
    """CORS 미들웨어 생성을 돕는 헬퍼 함수.

    Args:
        allow_origins: 허용할 Origin 목록(옵션). 제공 시 프리셋 값을 덮어씁니다.
        allow_methods: 허용할 HTTP 메서드 목록(옵션).
        allow_headers: 허용할 HTTP 헤더 목록(옵션).
        preset: 사전 정의된 설정 프리셋 이름. "development", "production",
            "api_only" 중 하나를 권장합니다.

    Returns:
        구성된 ``CORSMiddleware`` 인스턴스

    Examples:
        >>> create_cors_middleware(preset="production")
        >>> create_cors_middleware(allow_origins=["https://example.com"])
    """
    config = {}

    # 사전 정의된 설정 적용 (알 수 없는 프리셋은 무시하고 경고)
    if preset:
        preset_config = getattr(CORSConfig, preset.upper(), None)
        if preset_config:
            config.update(preset_config)
        else:
            logger.warning(f'Unknown CORS preset: {preset}')

    # 사용자 설정으로 덮어쓰기: 명시값이 우선
    if allow_origins is not None:
        config['allow_origins'] = allow_origins
    if allow_methods is not None:
        config['allow_methods'] = allow_methods
    if allow_headers is not None:
        config['allow_headers'] = allow_headers

    # 기본값 설정 (최소 안전/호환 값)
    config.setdefault('allow_origins', ['*'])
    config.setdefault('allow_methods', ['GET', 'POST', 'OPTIONS'])
    config.setdefault('allow_headers', ['Content-Type', 'Authorization'])

    return CORSMiddleware(
        allow_origins=config['allow_origins'],
        allow_methods=config['allow_methods'],
        allow_headers=config['allow_headers'],
    )
