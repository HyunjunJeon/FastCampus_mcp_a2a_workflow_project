"""A2A 통합이 적용된 플래너 에이전트.

이 모듈은 표준화된 A2A 인터페이스를 구현하여 작업 계획 수립과 배분을
수행하는 플래너 에이전트를 제공한다.
"""

import asyncio
import os

from datetime import datetime
from typing import Any
from uuid import uuid4

import pytz
import structlog
import uvicorn

from a2a.types import AgentCard
from langchain_core.language_models import BaseChatModel
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from src.a2a_integration.a2a_lg_server_utils import (
    build_a2a_starlette_application,
    build_request_handler,
    create_agent_card,
    create_agent_skill,
)
from src.a2a_integration.executor import LangGraphAgentExecutor
from src.agents.planner.planner_agent_lg import (
    create_planner_agent,
)
from src.base.a2a_interface import A2AOutput, A2AStreamBuffer, BaseA2AAgent
from src.base.base_graph_agent import BaseGraphAgent


logger = structlog.get_logger(__name__)


class PlannerA2AAgent(BaseA2AAgent, BaseGraphAgent):
    """A2A 통합 플래너 에이전트.

    이 에이전트는 다음을 수행한다:
    - 사용자 요청을 구조화된 PRD로 파싱
    - 의존성을 포함한 실행 계획 생성
    - 적절한 에이전트로 작업 분배
    - 작업 실행 진행 상황 모니터링

    최종적으로 Supervisor 에이전트에 구조화된 작업 계획을 제공한다.
    """

    def __init__(
        self,
        model: BaseChatModel | None = None,
        is_debug: bool = False,
        check_pointer: InMemorySaver | None = None,
    ) -> None:
        """Initialize Planner A2A Agent.

        Args:
            model: LLM model (default: gpt-4o-mini)
            is_debug: Debug mode flag
            check_pointer: Checkpoint manager (default: MemorySaver)
        """
        BaseA2AAgent.__init__(self)

        # Initialize the model and checkpointer for later use
        self.model = model
        self.check_pointer = check_pointer
        self.is_debug = is_debug
        self.agent = None  # Will be initialized async in _ensure_agent

        self.stream_buffer = A2AStreamBuffer(max_size=100)

        self.current_plan = []
        self.plan_metadata = {}
        self.workflow_phase = 'idle'

    async def initialize(self) -> bool:
        """Initialize the planner agent asynchronously."""
        try:
            await self._ensure_agent()
            return True
        except Exception as e:
            logger.error(f"Error initializing PlannerA2AAgent: {e}")
            return False

    async def _ensure_agent(self) -> None:
        """Ensure agent is initialized."""
        if self.agent is None:
            self.agent = await create_planner_agent(
                model=self.model,
                is_debug=self.is_debug,
                checkpointer=self.check_pointer,
            )

    async def execute_for_a2a(
        self, input_dict: dict[str, Any], config: dict[str, Any] | None = None
    ) -> A2AOutput:
        """Execute the agent with A2A-compatible input and output.

        Args:
            input_dict: Input data containing messages or planning request
            config: Optional configuration (thread_id, etc.)

        Returns:
            A2AOutput: Standardized output for A2A processing
        """
        try:
            # Ensure agent is initialized
            await self._ensure_agent()
            if self.agent is None:
                raise RuntimeError('Planner agent is not initialized')

            self.current_plan = []
            self.plan_metadata = {}
            self.workflow_phase = 'parsing'

            # Ensure config thread_id (use provided, or conversation_id fallback)
            if not config:
                config = {}
            config['configurable'] = config.get('configurable', {})
            if 'thread_id' not in config['configurable']:
                conv_id = input_dict.get('conversation_id') or input_dict.get('context_id')
                config['configurable']['thread_id'] = conv_id if conv_id else str(uuid4())

            result = await self.agent.ainvoke(
                input_dict,
                config=config,
            )

            logger.info(f'[PlannerA2AAgent] result: {result}')

            # Extract final output
            return self.extract_final_output(result)

        except Exception as e:
            return self.format_error(e, context='execute_for_a2a')

    def format_stream_event(self, event: dict[str, Any]) -> A2AOutput | None:
        """Convert a streaming event to standardized A2A output.

        Args:
            event: Raw streaming event from LangGraph

        Returns:
            A2AOutput if the event should be forwarded, None otherwise
        """
        event_type = event.get('event', '')

        # Handle LLM streaming
        if event_type == 'on_llm_stream':
            content = self.extract_llm_content(event)
            if content:
                # Track planning progress mentioned in content
                self._track_planning_progress(content)

                if self.stream_buffer.add(content):
                    # Buffer is full, flush it
                    return self.create_a2a_output(
                        status='working',
                        text_content=self.stream_buffer.flush(),
                        stream_event=True,
                        metadata={
                            'event_type': 'llm_stream',
                            'planning_progress': self._get_planning_progress(),
                        },
                    )

        # Handle tool execution events
        elif event_type == 'on_tool_start':
            tool_name = event.get('name', 'unknown')
            task_type = self._identify_task_type(tool_name)

            return self.create_a2a_output(
                status='working',
                text_content=f'📝 계획 작업 진행 중: {task_type}',
                stream_event=True,
                metadata={
                    'event_type': 'tool_start',
                    'tool_name': tool_name,
                    'task_type': task_type,
                },
            )

        # Handle tool completion with planning results
        elif event_type == 'on_tool_end':
            tool_output = event.get('data', {}).get('output', {})
            tool_name = event.get('name', 'unknown')
            task_type = self._identify_task_type(tool_name)

            if tool_output and isinstance(tool_output, dict):
                # Update plan if parsing or expanding tasks
                if (
                    'parse' in tool_name.lower()
                    or 'expand' in tool_name.lower()
                ):
                    if 'tasks' in tool_output:
                        self.current_plan.extend(tool_output['tasks'])
                    elif 'subtasks' in tool_output:
                        self.current_plan.extend(tool_output['subtasks'])

                return self.create_a2a_output(
                    status='working',
                    data_content={
                        'plan_update': {
                            'task_type': task_type,
                            'result': tool_output,
                        },
                        'current_progress': self._get_planning_progress(),
                    },
                    stream_event=True,
                    metadata={'event_type': 'plan_update'},
                )

        # Handle completion events
        elif self.is_completion_event(event):
            # Flush any remaining buffer content
            if self.stream_buffer.has_content():
                return self.create_a2a_output(
                    status='working',
                    text_content=self.stream_buffer.flush(),
                    stream_event=True,
                    metadata={'event_type': 'buffer_flush'},
                )

        return None

    def extract_final_output(self, state: dict[str, Any]) -> A2AOutput:
        """Extract final output from the agent's state.

        Args:
            state: Final state from the LangGraph execution

        Returns:
            A2AOutput: Final standardized output
        """
        try:
            # Extract messages from state
            messages = state.get('messages', [])

            # Get the last AI message as planning summary
            planning_summary = ''
            for msg in reversed(messages):
                if (
                    hasattr(msg, 'content')
                    and msg.__class__.__name__ == 'AIMessage'
                ):
                    planning_summary = msg.content
                    break

            # Extract plan from state
            plan = state.get('plan', [])
            metadata = state.get('metadata', {})
            agent_assignments = state.get('agent_assignments', {})
            workflow_phase = state.get('workflow_phase', 'completed')

            # Prepare structured data
            data_content = {
                'success': True,
                'result': {
                    'plan': plan,
                    'metadata': metadata,
                    'agent_assignments': agent_assignments,
                    'workflow_phase': workflow_phase,
                    'summary': planning_summary,
                    'timestamp': datetime.now(pytz.UTC).isoformat(),
                },
                'agent_type': 'PlannerA2AAgent',
                'workflow_status': workflow_phase,
            }

            # Create final output
            return self.create_a2a_output(
                status='completed',
                text_content=planning_summary or '계획이 완료되었습니다.',
                data_content=data_content,
                final=True,
                metadata={
                    'execution_complete': True,
                    'total_tasks': len(plan),
                    'workflow_phase': workflow_phase,
                },
            )

        except Exception as e:
            logger.error(f'Error extracting final output: {e}')
            return self.format_error(e, context='extract_final_output')

    # Helper methods for planning

    def _track_planning_progress(self, content: str) -> None:
        """Track planning progress from content."""
        content_lower = content.lower()

        phase_keywords = {
            'parsing': ['파싱', '분석', '요구사항', 'prd'],
            'planning': ['계획', '작업', '태스크', '단계'],
            'distributing': ['분배', '할당', '배포'],
            'monitoring': ['모니터링', '추적', '진행'],
        }

        for phase, keywords in phase_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                self.workflow_phase = phase

    def _identify_task_type(self, tool_name: str) -> str:
        """Identify which task type a tool represents."""
        tool_lower = tool_name.lower()

        # 작업 타입 매핑
        task_mappings = {
            'parse': 'PRD 파싱',
            'prd': 'PRD 파싱',
            'expand': '작업 확장',
            'complexity': '복잡도 분석',
            'analyze': '복잡도 분석',
            'create': '작업 생성',
            'update': '상태 업데이트',
            'get': '작업 조회',
            'search': '작업 조회',
        }

        # 매핑에서 일치하는 키를 찾아 반환
        for keyword, task_type in task_mappings.items():
            if keyword in tool_lower:
                return task_type

        return '일반 작업'

    def _get_planning_progress(self) -> dict[str, Any]:
        """Get current planning progress."""
        return {
            'tasks_created': len(self.current_plan),
            'workflow_phase': self.workflow_phase,
            'metadata': self.plan_metadata,
        }

    def get_agent_card(self, url: str) -> AgentCard:
        """A2A AgentCard 생성.

        AgentCard는 에이전트의 메타데이터와 기능을 설명하는 표준화된 문서입니다.
        다른 에이전트나 시스템이 이 에이전트의 기능을 이해하고 상호작용할 수 있도록 합니다.

        Args:
            url: 에이전트 서버의 기본 URL

        Returns:
            AgentCard: 에이전트 메타데이터 카드
        """
        # Docker 환경에서는 서비스 이름을 사용하여 내부 통신
        if os.getenv("IS_DOCKER", "false").lower() == "true":
            url = f"http://planner-agent:{os.getenv('AGENT_PORT', '8001')}"

        skills = [
            create_agent_skill(
                skill_id="create-plan",
                name="계획 생성",
                description="복잡한 작업을 실행 가능한 단계로 분해하고 계획을 생성합니다.",
                tags=["planning", "tasks", "dependencies", "orchestration"],
                examples=[
                    "데이터 분석 워크플로우 계획을 생성해주세요",
                    "트레이딩 전략 구현 계획을 수립해주세요"
                ],
            ),
            create_agent_skill(
                skill_id="expand-task",
                name="작업 확장",
                description="복잡한 작업을 실행 가능한 하위 작업으로 확장합니다.",
                tags=["planning", "expansion", "decomposition"],
                examples=[
                    "'시장 데이터 분석'을 하위 작업으로 확장해주세요",
                    "'트레이딩 전략 구현'을 단계별로 나눠주세요"
                ],
            ),
        ]

        logger.info("A2A agent card created")

        return create_agent_card(
            name="PlannerAgent",
            description="작업 계획 수립 및 오케스트레이션을 위한 Agent입니다.",
            url=url,
            skills=skills,
        )


# Factory function for backward compatibility
async def create_planner_a2a_agent(
    model: BaseChatModel | None = None, is_debug: bool = False, checkpointer: BaseCheckpointSaver | None = None
) -> PlannerA2AAgent:
    """Create and initialize a Planner A2A Agent.

    Args:
        model: LLM model (default: gpt-4o-mini)
        is_debug: Debug mode flag
        checkpointer: Checkpoint manager

    Returns:
        PlannerA2AAgent: Initialized agent instance
    """
    agent = PlannerA2AAgent(model, is_debug, checkpointer)
    await agent.initialize()
    return agent


def main() -> None:
    """PlannerAgent A2A 서버 실행.

    이 함수는 서버 실행의 진입점으로, 다음 작업을 수행합니다:
    1. 로깅 설정
    2. 비동기 초기화 실행
    3. 환경 설정 로드
    4. A2A 서버 생성 및 실행
    """

    async def async_init() -> "PlannerA2AAgent":
        """비동기 초기화 헬퍼 함수.

        MCP 서버와의 비동기 연결이 필요하므로 별도의 비동기 함수로 분리.

        Returns:
            PlannerA2AAgent: 초기화된 A2A 래퍼 인스턴스 또는 None
        """
        try:
            # PlannerA2AAgent 인스턴스 생성 (디버그 모드 활성화)
            _a2a_wrapper = PlannerA2AAgent(is_debug=True)

            # 비동기 초기화 실행 및 결과 확인
            if not await _a2a_wrapper.initialize():
                logger.error("❌ PlannerAgentA2A 초기화 실패")
                return None

            logger.info("✅ PlannerAgentA2A 초기화 완료")
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
        port = int(os.getenv("AGENT_PORT", "8001"))
        url = f"http://{host}:{port}"

        agent_card = a2a_agent.get_agent_card(url)

        # LangGraphAgentExecutor로 래핑
        executor = LangGraphAgentExecutor(
            agent_class=PlannerA2AAgent,
            is_debug=True
        )

        # A2A 서버 생성
        handler = build_request_handler(executor)
        server_app = build_a2a_starlette_application(
            agent_card=agent_card,
            handler=handler
        )

        # Health 체크 엔드포인트 추가 (Starlette 애플리케이션에 직접 주입)
        app = server_app.build()

        async def health_check(request: Request) -> JSONResponse:  # type: ignore[unused-argument]
            return JSONResponse({
                'status': 'healthy',
                'agent': 'PlannerAgent',
                'timestamp': datetime.now(pytz.UTC).isoformat(),
            })

        app.router.routes.append(
            Route('/health', health_check, methods=['GET'])
        )

        # 서버 시작 정보 로깅
        logger.info(f"✅ PlannerAgent A2A server starting at {url} with CORS enabled")
        logger.info(f"📋 Agent Card URL: {url}/.well-known/agent-card.json")  # A2A 표준 메타데이터 엔드포인트
        logger.info(f"🩺 Health Check: {url}/health")  # 헬스체크 엔드포인트

        # uvicorn 서버 직접 실행
        config = uvicorn.Config(
            app,
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
