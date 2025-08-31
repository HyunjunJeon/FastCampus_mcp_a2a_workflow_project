"""공통 A2A 서버 유틸리티 (LangGraph 전용).

이 모듈은 LangGraph의 `CompiledStateGraph`를 A2A(Agent-to-Agent)
프로토콜 서버로 쉽게 노출하기 위한 조립용 유틸리티를 제공합니다.

핵심 제공 기능은 다음과 같습니다.

1. `DefaultRequestHandler`와 비동기 `httpx` 클라이언트 생성
2. A2A용 Starlette/FastAPI 애플리케이션 빌더 제공
3. 에이전트 메타정보(`AgentCard`, `AgentSkill`) 생성 헬퍼
4. Uvicorn 런처와 상태/스키마 확인용 엔드포인트 추가

설계 의도:
- 애플리케이션 레벨의 부가 설정(타임아웃, 커넥션 풀, 헬스체크)을 안전한
  기본값으로 캡슐화하여 재사용성을 높입니다.
- 프로덕션 전환 시 교체가 필요한 구성(메모리 기반 저장소/푸시 구성)은
  주석으로 명시하여 향후 확장을 용이하게 합니다.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

import httpx
import structlog

from a2a.server.apps import A2AFastAPIApplication, A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import (
    BasePushNotificationSender,
    InMemoryPushNotificationConfigStore,
    InMemoryTaskStore,
)
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from src.a2a_integration.executor import LangGraphAgentExecutor
from src.a2a_integration.models import LangGraphExecutorConfig


if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from a2a.server.agent_execution import AgentExecutor
    from a2a.server.apps.jsonrpc.jsonrpc_app import (
        JSONRPCApplication,
    )
    from langgraph.graph.state import CompiledStateGraph
    from starlette.requests import Request


wrapper_logger = structlog.get_logger(__name__)

# TODO: "image/png", "audio/mpeg", "video/mp4"
# 기본적으로 텍스트/JSON만 허용합니다. 바이너리 MIME 추가는 보안/저장소/전송
# 정책을 정의한 뒤 확장하세요.
SUPPORTED_CONTENT_MIME_TYPES = [
    'text/plain',
    'text/markdown',
    'application/json',
]


def build_request_handler(executor: AgentExecutor) -> DefaultRequestHandler:
    """`DefaultRequestHandler`를 생성합니다.

    왜 이렇게 구현했는가:
    - 장시간 실행되는 LangGraph 작업을 고려하여 `httpx.AsyncClient`의
      읽기/풀 타임아웃을 넉넉히 설정합니다.
    - 현재 푸시 알림과 태스크 저장소는 인메모리 구현으로 제공하여
      개발/단일 프로세스 환경에서 즉시 사용 가능하게 합니다. 프로덕션에선
      외부 MQ/영구 저장소로 교체가 필요합니다.

    Args:
        executor: A2A 서버가 호출할 LangGraph 실행기.

    Returns:
        생성된 `DefaultRequestHandler` 인스턴스.

    Notes:
        - 인메모리 스토어는 프로세스 재시작 시 데이터가 소실됩니다.
        - `httpx` 커넥션 풀/타임아웃은 워크로드에 맞게 조정하십시오.
    """
    httpx_client = httpx.AsyncClient(
        timeout=httpx.Timeout(
            connect=60.0,  # 연결 타임아웃
            read=600.0,  # 읽기 타임아웃 - 10분
            write=60.0,  # 쓰기 타임아웃
            pool=600.0,  # 커넥션 풀 대기 타임아웃 - 10분
        ),
        limits=httpx.Limits(
            max_connections=100,  # 최대 동시 연결 수
            max_keepalive_connections=50,  # Keep-alive 연결 수
            keepalive_expiry=60.0,  # Keep-alive 유지 시간 (초)
        ),
        follow_redirects=True,
        headers={
            'Connection': 'keep-alive',
        },
    )
    # **DO NOT USE PRODUCTION**
    # TODO: [Production] MQ 기반 푸시 알림 구현 필요할 수 있습니다. - 현재 메모리 기반으로 서버 재시작 시 소실
    # TODO: [Scalability] Redis 기반 메시지 큐 구현 필요할 수 있습니다.
    push_config_store = InMemoryPushNotificationConfigStore()
    push_sender = BasePushNotificationSender(
        httpx_client=httpx_client,
        config_store=push_config_store,
    )
    return DefaultRequestHandler(
        agent_executor=executor,
        # TODO: [Production] PostgreSQL/MongoDB 기반 영구 Task 저장소 구현 필요할 수 있습니다.
        # TODO: [Recovery] 서버 재시작 시 진행 중인 Task 복구 로직 필요할 수 있습니다.
        task_store=InMemoryTaskStore(),
        push_config_store=push_config_store,
        push_sender=push_sender,
    )


def build_a2a_starlette_application(
    agent_card: AgentCard, handler: DefaultRequestHandler
) -> A2AStarletteApplication:
    """A2A Starlette 애플리케이션을 생성합니다.

    Args:
        agent_card: 에이전트의 메타정보(이름/버전/스킬 등).
        handler: JSON-RPC 요청을 실제로 처리할 핸들러.

    Returns:
        Starlette 기반 A2A 애플리케이션 래퍼.
    """
    return A2AStarletteApplication(agent_card=agent_card, http_handler=handler)


# NOTE: uv add "a2a-sdk[http-server]" 를 설치해야함
def build_a2a_fastapi_application(
    agent_card: AgentCard, handler: DefaultRequestHandler
) -> A2AFastAPIApplication:
    """A2A FastAPI 애플리케이션을 생성합니다.

    주의:
        FastAPI 변형은 이번 프로젝트에서 기본 경로는 아니며,
        필요 시 교체 용도로만 사용됩니다.

    Args:
        agent_card: 에이전트의 메타정보.
        handler: 요청 처리 핸들러.

    Returns:
        FastAPI 기반 A2A 애플리케이션 래퍼.
    """
    return A2AFastAPIApplication(agent_card=agent_card, http_handler=handler)


def create_agent_skill(
    skill_id: str,
    description: str,
    tags: list[str],
    name: str | None = None,
    input_modes: list[str] | None = None,
    output_modes: list[str] | None = None,
    examples: list[str] | None = None,
) -> AgentSkill:
    """에이전트 스킬을 생성합니다.

    Args:
        skill_id: 스킬 식별자(고유).
        description: 스킬 설명.
        tags: 검색/분류용 태그 목록.
        name: UI/카드 표시에 사용할 표시 이름. 기본은 `skill_id`.
        input_modes: 허용 입력 MIME 목록. 미지정 시 기본값 사용.
        output_modes: 허용 출력 MIME 목록. 미지정 시 기본값 사용.
        examples: 예시 프롬프트/사용법.

    Returns:
        `AgentSkill` 인스턴스.
    """
    if input_modes is None:
        input_modes = SUPPORTED_CONTENT_MIME_TYPES
    if output_modes is None:
        output_modes = SUPPORTED_CONTENT_MIME_TYPES

    return AgentSkill(
        id=skill_id,
        name=name or skill_id,
        description=description,
        input_modes=input_modes,
        output_modes=output_modes,
        tags=tags,
        examples=examples,
    )


def create_agent_card(
    *,
    name: str,
    description: str,
    url: str,
    skills: Iterable[AgentSkill],
    version: str = '1.0.0',
    default_input_modes: list[str] | None = None,
    default_output_modes: list[str] | None = None,
    streaming: bool = True,
    push_notifications: bool = True,
) -> AgentCard:
    """A2A 프로토콜 표준에 맞는 `AgentCard`를 생성합니다.

    왜 이렇게 구현했는가:
    - `AgentCapabilities`를 분리하여 스트리밍/푸시 지원 여부를 명확히 표현하고,
      카드의 다른 필드와 독립적으로 확장할 수 있게 합니다.

    Args:
        name: 에이전트 이름.
        description: 에이전트 설명.
        url: 에이전트가 수신 가능한 외부 접근 URL(배포 환경에 맞게 설정).
        skills: 제공 스킬들의 이터러블.
        version: 에이전트 버전 문자열.
        default_input_modes: 기본 입력 MIME 목록.
        default_output_modes: 기본 출력 MIME 목록.
        streaming: 서버-클라이언트 스트리밍 지원 여부.
        push_notifications: 푸시 알림 지원 여부.

    Returns:
        `AgentCard` 인스턴스.
    """
    capabilities = AgentCapabilities(
        streaming=streaming,
        push_notifications=push_notifications,
    )
    return AgentCard(
        name=name,
        description=description,
        url=url,
        version=version,
        default_input_modes=default_input_modes or SUPPORTED_CONTENT_MIME_TYPES,
        default_output_modes=default_output_modes
        or SUPPORTED_CONTENT_MIME_TYPES,
        capabilities=capabilities,
        skills=list(skills),
    )


def to_a2a_starlette_server(
    *,
    graph: CompiledStateGraph,
    agent_card: AgentCard,
    config: LangGraphExecutorConfig | None = None,
    input_processor: Any | None = None,  # 커스텀 입력 프로세서 추가
) -> A2AStarletteApplication:
    """Starlette 기반 A2A 서버 애플리케이션을 구성합니다.

    왜 이렇게 구현했는가:
    - LangGraph 실행 전략을 외부에서 주입할 수 있도록 `strategy_config`에
      `input_processor` 또는 팩토리 함수를 동적으로 삽입합니다. 이는 다양한
      전처리/검증/변환 전략을 런타임에 교체 가능하게 합니다.

    Args:
        graph: 컴파일된 LangGraph 상태 그래프.
        agent_card: 에이전트 카드 메타정보.
        config: 실행기 구성. 미지정 시 안전한 기본값이 사용됩니다.
        input_processor: 입력 전처리기 또는 그 팩토리(callable).

    Returns:
        `A2AStarletteApplication` 인스턴스.
    """
    # 커스텀 입력 프로세서가 제공되면 config에 추가
    if input_processor:
        if config is None:
            config = LangGraphExecutorConfig()
        if config.strategy_config is None:
            config.strategy_config = {}
        # 팩토리 함수인 경우 호출해서 인스턴스 생성
        if callable(input_processor):
            # 팩토리 함수 자체를 저장 (나중에 graph와 config로 호출)
            config.strategy_config['input_processor_factory'] = input_processor
        else:
            # 이미 인스턴스인 경우 직접 저장
            config.strategy_config['input_processor'] = input_processor

    executor = LangGraphAgentExecutor(
        graph=graph,
        config=config,
    )
    handler = build_request_handler(executor)
    return build_a2a_starlette_application(agent_card, handler)


# NOTE: 이번 프로젝트에서는 사용하지 않습니다.
def to_a2a_fastapi_server(
    *,
    graph: CompiledStateGraph,
    agent_card: AgentCard,
    result_extractor: Callable[[Any], str] | None = None,
    config: LangGraphExecutorConfig | None = None,
    input_processor: Any | None = None,  # 커스텀 입력 프로세서 추가
    agent_type: str | None = None,  # 에이전트 타입 추가
) -> A2AFastAPIApplication:
    """FastAPI 기반 A2A 서버 애플리케이션을 구성합니다.

    Args:
        graph: 컴파일된 LangGraph 상태 그래프.
        agent_card: 에이전트 카드 메타정보.
        result_extractor: LangGraph 실행 결과에서 표시용 문자열을 추출하는 함수.
        config: 실행기 구성.
        input_processor: 입력 전처리기 인스턴스 또는 팩토리.
        agent_type: 실행기/로깅 구분을 위한 선택적 에이전트 타입.

    Returns:
        `A2AFastAPIApplication` 인스턴스.
    """
    # 커스텀 입력 프로세서가 제공되면 config에 추가
    if input_processor:
        if config is None:
            config = LangGraphExecutorConfig()
        if config.strategy_config is None:
            config.strategy_config = {}
        config.strategy_config['input_processor'] = input_processor

    executor = LangGraphAgentExecutor(
        graph=graph,
        result_extractor=result_extractor,
        config=config,
        agent_type=agent_type,
    )
    handler = build_request_handler(executor)
    return build_a2a_fastapi_application(agent_card, handler)


def to_a2a_run_uvicorn(
    *,
    server_app: JSONRPCApplication,
    host: str,
    port: int,
    graph: CompiledStateGraph | None = None,
    agent_card: AgentCard | None = None,
    enable_schema_endpoint: bool = True,
) -> None:
    """Uvicorn으로 A2A 서버를 실행합니다.

    기능:
        - `GET /health`: 간단한 헬스체크 응답을 제공합니다.
        - `GET /schemas` (옵션): LangGraph 입력/출력 스키마를 안전하게
          조회합니다. 런타임에서 메서드 존재 여부를 검사하고 가능한
          여러 변환 경로를 시도한 뒤 직렬화 가능한 형태로 반환합니다.

    Args:
        server_app: JSON-RPC를 지원하는 Starlette/FastAPI 래퍼 앱.
        host: 바인딩 호스트.
        port: 바인딩 포트.
        graph: 스키마 조회를 위한 선택적 LangGraph 인스턴스.
        agent_card: 스키마 응답에 포함할 에이전트 카드.
        enable_schema_endpoint: `/schemas` 노출 여부.

    Notes:
        - WebSocket 및 keep-alive 타임아웃을 늘려 장시간 스트리밍에 대비합니다.
        - 동시 연결 제한(`limit_concurrency`)은 워크로드에 맞게 조정하세요.
    """
    import uvicorn

    from starlette.responses import JSONResponse
    from starlette.routing import Route

    # Add health check endpoint
    # 간단한 상태 점검용 엔드포인트를 추가합니다. 모니터링/로드밸런서 헬스체크에 사용.
    async def health_check(request: Request):
        return JSONResponse(
            {
                'status': 'healthy',
                'request': str(request.values()),
            }
        )
    app = server_app.build()

    app.router.routes.append(
        Route(
            '/health',
            health_check,
            methods=['GET'],
        )
    )

    # LangGraph 스키마 엔드포인트 추가 (enable_schema_endpoint가 True인 경우)
    if enable_schema_endpoint:

        async def get_langgraph_schemas(request: Request):
            """LangGraph Agent의 입력/출력 스키마를 반환합니다.

            예외/호환성 고려:
            - `get_input_jsonschema`/`get_output_jsonschema`가 없을 수 있어
              대체 메서드(`get_input_schema`, `get_output_schema`)를 순차 시도.
            - 스키마 객체가 Pydantic/dict/기타 형태일 수 있어 안전 변환을 적용.
            """
            try:
                # 1. 필수 객체들의 존재 여부 확인
                if graph is None:
                    raise ValueError('Graph is not provided')
                if agent_card is None:
                    raise ValueError('Agent card is not provided')

                # 2. 메서드 존재 여부 확인 후 스키마 조회
                input_schema = None
                output_schema = None

                # LangGraph 메서드 존재 여부 확인
                if hasattr(graph, 'get_input_jsonschema'):
                    try:
                        input_schema = graph.get_input_jsonschema()
                    except Exception as e:
                        print(f'Failed to get input schema: {e}')

                if hasattr(graph, 'get_output_jsonschema'):
                    try:
                        output_schema = graph.get_output_jsonschema()
                    except Exception as e:
                        print(f'Failed to get output schema: {e}')

                # 3. 대안 메서드 시도
                if input_schema is None and hasattr(graph, 'get_input_schema'):
                    try:
                        input_schema = graph.get_input_schema()
                    except Exception as e:
                        print(
                            f'Failed to get input schema with alternative method: {e}'
                        )

                if output_schema is None and hasattr(
                    graph, 'get_output_schema'
                ):
                    try:
                        output_schema = graph.get_output_schema()
                    except Exception as e:
                        print(
                            f'Failed to get output schema with alternative method: {e}'
                        )

                # 4. 안전한 스키마 변환
                def safe_schema_conversion(schema):
                    # 주어진 스키마 객체를 JSON 직렬화 가능한 dict로 최대한 안전하게 변환합니다.
                    if schema is None:
                        return {}

                    # Pydantic 모델 변환
                    if hasattr(schema, 'model_dump'):
                        try:
                            return schema.model_dump()
                        except Exception:
                            pass
                    elif hasattr(schema, 'dict'):
                        try:
                            return schema.dict()
                        except Exception:
                            pass
                    elif hasattr(schema, '__dict__'):
                        try:
                            return schema.__dict__
                        except Exception:
                            pass
                    elif isinstance(schema, dict):
                        return schema
                    else:
                        # JSON 직렬화 가능한지 확인
                        try:
                            import json

                            json.dumps(schema)
                            return schema
                        except (TypeError, ValueError):
                            return {
                                'type': 'unknown',
                                'description': str(type(schema)),
                            }

                converted_input_schema = safe_schema_conversion(input_schema)
                converted_output_schema = safe_schema_conversion(output_schema)

                return JSONResponse(
                    {
                        'input_schema': converted_input_schema,
                        'output_schema': converted_output_schema,
                        'agent_name': getattr(agent_card, 'name', 'unknown'),
                        'timestamp': str(datetime.now()),
                        'source': 'langgraph',
                        'debug_info': {
                            'graph_type': str(type(graph)),
                            'has_input_jsonschema': hasattr(
                                graph, 'get_input_jsonschema'
                            ),
                            'has_output_jsonschema': hasattr(
                                graph, 'get_output_jsonschema'
                            ),
                            'input_schema_type': str(type(input_schema)),
                            'output_schema_type': str(type(output_schema)),
                        },
                    }
                )

            except Exception as e:
                # 상세한 에러 정보 포함
                error_details = {
                    'error_type': type(e).__name__,
                    'error_message': str(e),
                    'graph_available': graph is not None,
                    'agent_card_available': agent_card is not None,
                }

                if graph is not None:
                    error_details['graph_type'] = str(type(graph))
                    error_details['graph_methods'] = [
                        method
                        for method in dir(graph)
                        if method.startswith('get_') and 'schema' in method
                    ]

                return JSONResponse(
                    {
                        'input_schema': {
                            'type': 'object',
                            'properties': {'message': {'type': 'string'}},
                            'required': ['message'],
                        },
                        'output_schema': {
                            'type': 'object',
                            'properties': {
                                'status': {'type': 'string'},
                                'data': {'type': 'object'},
                            },
                        },
                        'error': f'Failed to get schemas: {e!s}',
                        'error_details': error_details,
                        'source': 'fallback',
                    }
                )

        app.router.routes.append(
            Route(
                '/schemas',
                get_langgraph_schemas,
                methods=['GET'],
            )
        )

    # uvicorn 서버 설정 - 타임아웃 증가
    # 장시간 연결 및 스트리밍을 고려한 보수적(넉넉한) 설정값을 사용합니다.
    config = uvicorn.Config(
        app,
        host=host,
        port=port,
        log_level='info',
        access_log=False,
        reload=False,
        timeout_keep_alive=300,  # Keep-alive 타임아웃 300초로 증가
        timeout_notify=300,  # 종료 전 알림 타임아웃 300초
        ws_ping_interval=30,  # WebSocket ping 간격 30초
        ws_ping_timeout=60,  # WebSocket ping 타임아웃 60초
        limit_concurrency=1000,  # 동시 연결 제한 증가
    )
    server = uvicorn.Server(config)
    server.run()
