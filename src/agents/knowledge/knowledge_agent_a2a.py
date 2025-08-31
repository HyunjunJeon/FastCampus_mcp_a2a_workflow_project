"""지식(메모리) 에이전트 A2A 래퍼.

이 모듈은 Memory/Knowledge 에이전트를 A2A 통신 프로토콜과 호환되도록 감싸는
래퍼 구현을 제공한다.
"""

import asyncio
import os

from datetime import datetime
from typing import Any

import pytz
import structlog
import uvicorn

from a2a.types import AgentCard
from langchain_core.language_models import BaseChatModel
from langgraph.checkpoint.base import BaseCheckpointSaver

from src.a2a_integration.a2a_lg_server_utils import (
    build_a2a_starlette_application,
    build_request_handler,
    create_agent_card,
    create_agent_skill,
)
from src.a2a_integration.executor import LangGraphAgentExecutor
from src.agents.knowledge.knowledge_agent_lg import create_knowledge_agent
from src.base.a2a_interface import A2AOutput, BaseA2AAgent


logger = structlog.get_logger(__name__)


class KnowledgeA2AAgent(BaseA2AAgent):
    """지식(메모리) 에이전트용 A2A 래퍼.

    LangGraph 기반 메모리 관리 에이전트를 감싸 지식(메모리) 작업을
    A2A 프로토콜과 호환되도록 제공한다.
    """

    def __init__(
        self,
        model: BaseChatModel | None = None,
        check_pointer: BaseCheckpointSaver | None = None,
        is_debug: bool = False,
    ) -> None:
        """Initialize the Memory A2A Agent.

        Args:
            model: LLM model for memory analysis
            check_pointer: Checkpoint manager
            is_debug: Debug mode flag
        """
        super().__init__()

        self.graph = None
        self.agent_type = 'Knowledge'
        logger.info('KnowledgeA2AAgent initialized')

    async def initialize(self) -> bool:
        """지식(메모리) 에이전트를 비동기로 초기화한다."""
        try:
            if self.graph is None:
                self.graph = await create_knowledge_agent()
                logger.info("Knowledge agent graph created successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing KnowledgeA2AAgent: {e}")
            return False

    async def execute_for_a2a(
        self,
        input_dict: dict[str, Any],
        config: dict[str, Any] | None = None,
    ) -> A2AOutput:
        """A2A 호환 입력/출력 규격으로 지식(메모리) 에이전트를 실행한다.

        Args:
            input_dict: 메시지와 메모리 요청이 포함된 입력 데이터
            config: 선택적 실행 구성

        Returns:
            A2AOutput: A2A 처리 표준 출력
        """
        try:
            logger.info(f'Executing KnowledgeA2AAgent with input: {input_dict}')

            # Add configuration (thread_id)
            # 우선순위: 전달된 config.thread_id > input_dict.conversation_id > 생성된 기본값
            config = config or {}
            configurable = config.get('configurable', {})
            provided_thread_id = configurable.get('thread_id')
            conversation_id = input_dict.get('conversation_id')
            if provided_thread_id:
                configurable['thread_id'] = provided_thread_id
            elif conversation_id:
                configurable['thread_id'] = conversation_id
            else:
                configurable['thread_id'] = f"knowledge-{datetime.now(pytz.UTC).isoformat()}"
            config['configurable'] = configurable

            # Execute the LangGraph agent
            result = await self.graph.ainvoke(input_dict, config)

            # Extract final output
            return self.extract_final_output(result)

        except Exception as e:
            logger.error(f'Error executing KnowledgeA2AAgent: {e}')
            return self.format_error(e, 'Memory operation failed')

    def format_stream_event(self, event: dict[str, Any]) -> A2AOutput | None:
        """스트리밍 이벤트를 표준 A2A 출력으로 변환한다.

        Args:
            event: LangGraph 로부터 수신한 원시 스트리밍 이벤트

        Returns:
            전달할 이벤트라면 A2AOutput, 아니면 None
        """
        try:
            event_type = event.get('event', '')

            # Handle LLM streaming
            if event_type == 'on_llm_stream':
                content = self.extract_llm_content(event)
                if content:
                    return self.create_a2a_output(
                        status='working',
                        text_content=content,
                        metadata={
                            'event_type': 'llm_stream',
                            'timestamp': datetime.now(pytz.UTC).isoformat(),
                        },
                        stream_event=True,
                        final=False,
                    )

            # Handle node execution events
            elif event_type == 'on_chain_start':
                node_name = event.get('name', '')
                if node_name in self.NODE_NAMES.values():
                    return self.create_a2a_output(
                        status='working',
                        text_content=f'메모리 작업 중: {node_name}',
                        metadata={
                            'event_type': 'node_start',
                            'node_name': node_name,
                            'timestamp': datetime.now(pytz.UTC).isoformat(),
                        },
                        stream_event=True,
                        final=False,
                    )

            # Handle tool execution events
            elif event_type == 'on_tool_start':
                tool_name = event.get('name', '')
                if 'knowledge' in tool_name.lower():
                    return self.create_a2a_output(
                        status='working',
                        text_content=f'메모리 도구 사용: {tool_name}',
                        metadata={
                            'event_type': 'tool_start',
                            'tool_name': tool_name,
                            'timestamp': datetime.now(pytz.UTC).isoformat(),
                        },
                        stream_event=True,
                        final=False,
                    )

            # Check for completion
            if self.is_completion_event(event):
                return self.create_a2a_output(
                    status='completed',
                    text_content='지식(메모리) 작업이 완료되었습니다.',
                    metadata={
                        'event_type': 'completion',
                        'timestamp': datetime.now(pytz.UTC).isoformat(),
                    },
                    stream_event=True,
                    final=True,
                )

            return None

        except Exception as e:
            logger.error(f'Error formatting stream event: {e}')
            return None

    def extract_final_output(self, state: dict[str, Any]) -> A2AOutput:
        """에이전트 상태에서 최종 출력을 추출한다.

        Args:
            state: LangGraph 실행이 완료된 최종 상태

        Returns:
            A2AOutput: 표준 최종 출력
        """
        try:
            # Prepare data content with memory operation results
            data_content: dict[str, Any] = {}

            # Include saved memories
            active_memories = state.get('active_memories', [])
            if active_memories:
                data_content['saved_memories'] = active_memories

            # Include retrieved memories
            retrieved_memories = state.get('retrieved_memories', [])
            if retrieved_memories:
                data_content['retrieved_memories'] = retrieved_memories

            # Include operation history
            operation_history = state.get('operation_history', [])
            if operation_history:
                data_content['operation_history'] = operation_history

            # Derive deleted memories from operation_history if present
            deleted_memories: list[dict[str, Any]] = []
            for op in operation_history or []:
                if not isinstance(op, dict):
                    continue
                op_type = (
                    op.get('operation')
                    or op.get('action')
                    or op.get('type')
                    or ''
                )
                if isinstance(op_type, str) and op_type.lower() in {'delete', 'deleted', 'remove', 'removed'}:
                    target = op.get('target') or op.get('memory') or op
                    if isinstance(target, dict):
                        deleted_memories.append(target)
            if deleted_memories:
                data_content['deleted_memories'] = deleted_memories

            # Build concise operation summary for UX
            def _items_brief(items: list[dict[str, Any]], key_candidates: list[str]) -> list[str]:
                briefs: list[str] = []
                for it in items[:5]:  # cap in summary
                    value = None
                    for k in key_candidates:
                        if isinstance(it, dict) and k in it and it[k]:
                            value = it[k]
                            break
                    if value is None and isinstance(it, dict) and 'content' in it:
                        content = str(it.get('content') or '')
                        value = content[:80] + ('…' if len(content) > 80 else '')
                    briefs.append(str(value) if value is not None else '(no-title)')
                return briefs

            saved_cnt = len(data_content.get('saved_memories', []))
            deleted_cnt = len(data_content.get('deleted_memories', []))
            retrieved_cnt = len(data_content.get('retrieved_memories', []))

            saved_briefs = _items_brief(data_content.get('saved_memories', []), ['title', 'name', 'id']) if saved_cnt else []
            deleted_briefs = _items_brief(data_content.get('deleted_memories', []), ['title', 'name', 'id']) if deleted_cnt else []
            retrieved_briefs = _items_brief(data_content.get('retrieved_memories', []), ['title', 'name', 'id']) if retrieved_cnt else []

            summary_lines = [
                f"저장 {saved_cnt}건" + (f" — {', '.join(saved_briefs)}" if saved_briefs else ''),
                f"삭제 {deleted_cnt}건" + (f" — {', '.join(deleted_briefs)}" if deleted_briefs else ''),
                f"조회 {retrieved_cnt}건" + (f" — {', '.join(retrieved_briefs)}" if retrieved_briefs else ''),
            ]
            summary_text = '지식 작업 완료:\n' + '\n'.join(summary_lines)

            # Enrich with normalized operations block for clients
            data_content['memory_operations'] = {
                'saved_count': saved_cnt,
                'deleted_count': deleted_cnt,
                'retrieved_count': retrieved_cnt,
            }

            return self.create_a2a_output(
                status='completed',
                text_content=summary_text,
                data_content=data_content if data_content else None,
                metadata={
                    'timestamp': datetime.now(pytz.UTC).isoformat(),
                },
                final=True,
            )

        except Exception as e:
            logger.error(f'Error extracting final output: {e}')
            return self.format_error(
                e, 'Failed to extract memory operation results'
            )

    def get_agent_card(self, url: str) -> AgentCard:
        """A2A AgentCard 생성.

        AgentCard는 에이전트의 메타데이터와 기능을 설명하는 표준화된 문서이다.
        다른 에이전트나 시스템이 이 에이전트의 기능을 이해하고 상호작용할 수 있도록 한다.

        Args:
            url: 에이전트 서버의 기본 URL

        Returns:
            AgentCard: 에이전트 메타데이터 카드
        """
        # Docker 환경에서는 서비스 이름을 사용하여 내부 통신
        if os.getenv("IS_DOCKER", "false").lower() == "true":
            url = f"http://knowledge-agent:{os.getenv('AGENT_PORT', '8002')}"
        _skill = create_agent_skill(
            skill_id="knowledge",
            name="지식(메모리) 관리",
            description="지식(메모리) 관리를 위한 투자전문 Agent 입니다.",
            tags=["knowledge", "memory", "investment"],
            examples=["지식(메모리) 관리를 해주세요"],
        )

        logger.info("A2A agent card created")

        return create_agent_card(
            name="KnowledgeAgent",
            description="지식(메모리) 관리를 위한 Agent 입니다.",
            url=url,
            skills=[_skill],
        )

def main() -> None:
    """KnowledgeAgent A2A 서버 실행.

    이 함수는 서버 실행의 진입점으로, 다음 작업을 수행합니다:
    1. 로깅 설정
    2. 비동기 초기화 실행
    3. 환경 설정 로드
    4. A2A 서버 생성 및 실행
    """

    async def async_init() -> "KnowledgeA2AAgent":
        """비동기 초기화 헬퍼 함수.

        MCP 서버와의 비동기 연결이 필요하므로 별도의 비동기 함수로 분리.

        Returns:
            KnowledgeA2AAgent: 초기화된 A2A 래퍼 인스턴스 또는 None
        """
        try:
            # KnowledgeA2AAgent 인스턴스 생성 (디버그 모드 활성화)
            _a2a_wrapper = KnowledgeA2AAgent(is_debug=True)

            # 비동기 초기화 실행 및 결과 확인
            if not await _a2a_wrapper.initialize():
                logger.error("❌ KnowledgeAgentA2A 초기화 실패")
                return None

            logger.info("✅ KnowledgeAgentA2A 초기화 완료")
            return _a2a_wrapper

        except Exception as e:
            # 초기화 중 발생한 예외 처리
            logger.error(f"초기화 중 오류 발생: {e}", exc_info=True)
            return None

    a2a_agent = asyncio.run(async_init())

    # 초기화 실패 시 조기 종료
    if a2a_agent is None:
        return

    try:
        # 환경 변수에서 서버 설정 로드
        # Docker 환경 여부 확인 - Docker에서는 모든 인터페이스에서 수신
        is_docker = os.getenv("IS_DOCKER", "false").lower() == "true"

        # 호스트 설정: Docker는 0.0.0.0, 로컬은 localhost
        host = os.getenv("AGENT_HOST", "localhost" if not is_docker else "0.0.0.0")
        port = int(os.getenv("AGENT_PORT", "8002"))
        url = f"http://{host}:{port}"

        agent_card = a2a_agent.get_agent_card(url)

        # LangGraphAgentExecutor로 래핑
        executor = LangGraphAgentExecutor(
            agent_class=KnowledgeA2AAgent,
            is_debug=True
        )

        # A2A 서버 생성
        handler = build_request_handler(executor)
        server_app = build_a2a_starlette_application(
            agent_card=agent_card,
            handler=handler
        )

        # 서버 시작 정보 로깅
        logger.info(f"KnowledgeAgent A2A 서버 시작: {url} (CORS 사용)")
        logger.info(f"Agent Card URL: {url}/.well-known/agent-card.json")  # A2A 표준 메타데이터 엔드포인트
        logger.info(f"Health Check: {url}/health")  # 헬스체크 엔드포인트

        # uvicorn 서버 직접 실행
        config = uvicorn.Config(
            server_app.build(),
            host=host,
            port=port,
            log_level="info",
            access_log=False,
            reload=False,
            timeout_keep_alive=1000,
            timeout_notify=1000,
            ws_ping_interval=30,
            ws_ping_timeout=60,
            limit_max_requests=None,
            timeout_graceful_shutdown=10,
        )
        server = uvicorn.Server(config)
        server.run()

    except Exception as e:
        # 서버 시작 실패 시 에러 로깅 및 예외 재발생
        logger.error(f"서버 시작 중 오류 발생: {e}", exc_info=True)
        raise
