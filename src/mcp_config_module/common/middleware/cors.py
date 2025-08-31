"""FastMCP CORS Middleware.

This middleware provides CORS (Cross-Origin Resource Sharing) support for FastMCP servers,
allowing you to specify which origins, methods, and headers are permitted in cross-origin requests.
"""

import logging
import traceback

from fastmcp.server.middleware import Middleware


logger = logging.getLogger(__name__)


class CORSMiddleware(Middleware):
    """FastMCP CORS Middleware."""

    def __init__(
        self,
        allow_origins: list[str],
        allow_methods: list[str],
        allow_headers: list[str],
    ):
        """CORS middleware 초기화.

        Args:
            allow_origins: 허용할 원본 목록
            allow_methods: 허용할 HTTP 메서드 목록
            allow_headers: 허용할 HTTP 헤더 목록
        """
        super().__init__()

        self.allow_origins = allow_origins
        self.allow_methods = allow_methods
        self.allow_headers = allow_headers

        logger.info('CORS middleware initialized')

    def _is_origin_allowed(self, origin: str) -> bool:
        """요청 origin이 허용되는지 확인.

        Args:
            origin: 요청 origin

        Returns:
            허용 여부
        """
        if '*' in self.allow_origins:
            return True

        return origin in self.allow_origins

    def _add_cors_headers(
        self, response_headers: dict, origin: str | None = None
    ) -> dict:
        """CORS 헤더를 응답에 추가.

        Args:
            response_headers: 기존 응답 헤더
            origin: 요청 origin

        Returns:
            CORS 헤더가 추가된 응답 헤더
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

        # 자격 증명 허용 설정 (origin이 특정되어 있을 때만)
        if origin and origin in self.allow_origins:
            cors_headers['Access-Control-Allow-Credentials'] = 'true'

        return cors_headers

    async def process_request(self, request: dict) -> dict:
        """요청 전처리 - CORS preflight 요청 처리.

        Args:
            request: 요청 데이터

        Returns:
            처리된 요청 데이터 또는 preflight 응답
        """
        try:
            method = request.get('method', '').upper()
            headers = request.get('headers', {})
            origin = headers.get('origin', headers.get('Origin'))

            logger.debug(
                f'Processing CORS request: method={method}, origin={origin}'
            )

            # OPTIONS 메서드이고 preflight 요청인 경우
            if method == 'OPTIONS' and origin:
                # Access-Control-Request-Method 헤더가 있으면 preflight 요청
                request_method = headers.get(
                    'access-control-request-method'
                ) or headers.get('Access-Control-Request-Method')

                if request_method:
                    logger.info(
                        f'Handling CORS preflight request from {origin}'
                    )

                    # Origin 검증
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

                    # Preflight 응답 생성
                    response_headers = self._add_cors_headers({}, origin)

                    return {
                        'id': request.get('id'),
                        'result': {
                            'status': 'OK',
                            'message': 'CORS preflight successful',
                        },
                        'headers': response_headers,
                    }

            # 일반 요청의 경우 origin 검증
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

            # CORS 정보를 요청에 추가
            request['_cors_origin'] = origin

            return request

        except Exception as e:
            logger.error(f'Error processing CORS request: {e}')
            logger.debug(traceback.format_exc())
            return request

    async def process_response(self, request: dict, response: dict) -> dict:
        """응답 후처리 - CORS 헤더 추가.

        Args:
            request: 원본 요청 데이터
            response: 응답 데이터

        Returns:
            CORS 헤더가 추가된 응답 데이터
        """
        try:
            origin = request.get('_cors_origin')

            if origin:
                logger.debug(
                    f'Adding CORS headers to response for origin: {origin}'
                )

                # 기존 헤더 가져오기
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
        """미들웨어 정보 반환.

        Returns:
            미들웨어 정보
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
    """CORS 설정을 위한 사전 정의된 구성."""

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
    """CORS 미들웨어 생성 헬퍼 함수.

    Args:
        allow_origins: 허용할 origin 목록
        allow_methods: 허용할 HTTP 메서드 목록
        allow_headers: 허용할 HTTP 헤더 목록
        preset: 사전 정의된 설정 ("development", "production", "api_only")

    Returns:
        구성된 CORS 미들웨어 인스턴스
    """
    config = {}

    # 사전 정의된 설정 적용
    if preset:
        preset_config = getattr(CORSConfig, preset.upper(), None)
        if preset_config:
            config.update(preset_config)
        else:
            logger.warning(f'Unknown CORS preset: {preset}')

    # 사용자 설정으로 덮어쓰기
    if allow_origins is not None:
        config['allow_origins'] = allow_origins
    if allow_methods is not None:
        config['allow_methods'] = allow_methods
    if allow_headers is not None:
        config['allow_headers'] = allow_headers

    # 기본값 설정
    config.setdefault('allow_origins', ['*'])
    config.setdefault('allow_methods', ['GET', 'POST', 'OPTIONS'])
    config.setdefault('allow_headers', ['Content-Type', 'Authorization'])

    return CORSMiddleware(
        allow_origins=config['allow_origins'],
        allow_methods=config['allow_methods'],
        allow_headers=config['allow_headers'],
    )
