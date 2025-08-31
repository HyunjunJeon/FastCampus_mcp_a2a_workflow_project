"""Task Executor Agent A2A Wrapper.

This module provides an A2A protocol wrapper for the Task Executor Agent,
enabling it to work with the A2A communication protocol.
"""

import asyncio
import os
import re

from datetime import datetime
from typing import Any

import pytz
import structlog
import uvicorn

from a2a.types import AgentCard
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from src.a2a_integration.a2a_lg_server_utils import (
    build_a2a_starlette_application,
    build_request_handler,
    create_agent_card,
    create_agent_skill,
)
from src.a2a_integration.executor import LangGraphAgentExecutor
from src.agents.executor.task_executor_agent_lg import (
    create_executor_agent,
)
from src.agents.prompts import get_prompt
from src.base.a2a_interface import A2AOutput, BaseA2AAgent


logger = structlog.get_logger(__name__)


class TaskExecutorA2AAgent(BaseA2AAgent):
    """A2A wrapper for the Task Executor Agent.

    This class wraps the LangGraph TaskExecutorAgent to provide
    A2A protocol compatibility for general task execution operations.
    """

    def __init__(
        self,
        model: Any | None = None,
        check_pointer: Any | None = None,
        is_debug: bool = False,
    ) -> None:
        """Initialize the Task Executor A2A Agent.

        Args:
            model: LLM model for task analysis
            check_pointer: Checkpoint manager
            is_debug: Debug mode flag
        """
        super().__init__()

        # Store parameters for async initialization
        self.model = model
        self.check_pointer = check_pointer or InMemorySaver()
        self.is_debug = is_debug

        # Agent will be initialized asynchronously
        self.graph = None
        self.agent_type = 'Executor'
        self.NODE_NAMES = {
            'analyze_task': 'analyze_task',
            'prepare_environment': 'prepare_environment',
            'execute_task': 'execute_task',
            'validate_results': 'validate_results',
            'handle_error': 'handle_error',
        }

        logger.info('TaskExecutorA2AAgent initialized')

    async def initialize(self) -> bool:
        """Initialize the executor agent asynchronously."""
        try:
            if self.graph is None:
                self.graph = await create_executor_agent(
                    model=self.model,
                    is_debug=self.is_debug,
                    checkpointer=self.check_pointer,
                )
                logger.info('Executor agent graph created successfully')
            return True
        except Exception as e:
            logger.error(f"Error initializing TaskExecutorA2AAgent: {e}")
            return False

    async def execute_for_a2a(
        self, input_dict: dict[str, Any], config: dict[str, Any] | None = None
    ) -> A2AOutput:
        """Execute the Task Executor Agent with A2A-compatible input and output.

        Args:
            input_dict: Input data containing messages and task details
            config: Optional configuration

        Returns:
            A2AOutput: Standardized output for A2A processing
        """
        try:
            logger.info(
                f'Executing TaskExecutorA2AAgent with input: {input_dict}'
            )

            # Ensure agent is initialized
            await self.initialize()

            # Extract user request from input
            messages = input_dict.get('messages', [])
            user_request = ''

            for msg in messages:
                if msg.get('role') == 'user':
                    user_request = msg.get('content', '')
                    break

            # Extract executor-specific parameters if provided
            code_to_execute = input_dict.get('code_to_execute')
            language = input_dict.get('language', 'python')
            notion_config = input_dict.get('notion_config', {})

            # Sanitize Notion parent IDs: extract and hyphenate UUIDs; do NOT default to workspace
            try:
                def _extract_hyphenated_uuid(value: str) -> str | None:
                    if not isinstance(value, str):
                        return None
                    # Already hyphenated UUID
                    if re.fullmatch(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", value):
                        return value
                    # Find last 32-hex sequence
                    m = re.findall(r"[0-9a-fA-F]{32}", value)
                    if not m:
                        return None
                    raw = m[-1].lower()
                    return f"{raw[0:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:32]}"

                if isinstance(notion_config, dict):
                    parent = notion_config.get('parent')
                    if isinstance(parent, dict):
                        if 'page_id' in parent:
                            parsed = _extract_hyphenated_uuid(parent.get('page_id'))
                            if parsed:
                                notion_config = {**notion_config, 'parent': {**parent, 'page_id': parsed, 'database_id': parent.get('database_id')}}
                        if 'database_id' in parent:
                            parsed = _extract_hyphenated_uuid(parent.get('database_id'))
                            if parsed:
                                notion_config = {**notion_config, 'parent': {**parent, 'database_id': parsed, 'page_id': parent.get('page_id')}}
            except Exception:
                # If sanitization fails, keep original and allow downstream validation to surface clear error
                pass

            # Build an explicit user prompt including parameters so the agent doesn't ask for parent interactivity
            if code_to_execute:
                task_type = 'code'
                parameters_for_prompt = {'code': code_to_execute, 'language': language}
            elif notion_config:
                task_type = 'notion'
                parameters_for_prompt = notion_config
            else:
                task_type = 'api'
                parameters_for_prompt = input_dict

            prompt_text = get_prompt(
                'executor',
                'user',
                task_type=task_type,
                task_description=user_request or 'Execute task via A2A',
                parameters=parameters_for_prompt,
            )

            # Prepare input for LangGraph agent
            lg_input = {
                'messages': [HumanMessage(content=prompt_text)],
                'timeout': 300,
                'max_retries': 3,
                'workflow_phase': 'initializing',
                'should_continue': True,
                'retry_count': 0,
                'current_step_index': 0,
                'execution_plan': [],
                'completed_steps': [],
                'failed_steps': [],
                'execution_results': [],
                'notion_operations': [],
                'working_files': [],
                'created_files': [],
                'modified_files': [],
                'intermediate_results': [],
                'total_execution_time': 0,
                'tool_usage_stats': {},
            }

            # Add configuration (use provided thread_id or conversation_id)
            if not config:
                config = {}
            config['configurable'] = config.get('configurable', {})
            if 'thread_id' not in config['configurable']:
                conv_id = input_dict.get('conversation_id') or input_dict.get('context_id')
                config['configurable']['thread_id'] = (
                    conv_id if conv_id else f'executor-{datetime.now(pytz.UTC).isoformat()}'
                )

            # Execute the LangGraph agent
            result = await self.graph.ainvoke(lg_input, config)

            # Extract final output
            return self.extract_final_output(result)

        except Exception as e:
            logger.error(f'Error executing TaskExecutorA2AAgent: {e}')
            return self.format_error(e, 'Task execution failed')

    def format_stream_event(self, event: dict[str, Any]) -> A2AOutput | None:
        """Convert a streaming event to standardized A2A output.

        Args:
            event: Raw streaming event from LangGraph

        Returns:
            A2AOutput if the event should be forwarded, None otherwise
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
                    node_display_name = self._get_node_display_name(node_name)
                    return self.create_a2a_output(
                        status='working',
                        text_content=f'작업 실행 중: {node_display_name}',
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
                if any(
                    tool in tool_name.lower()
                    for tool in [
                        'sandbox',
                        'notion',
                        'composio',
                        'codeinterpreter',
                    ]
                ):
                    return self.create_a2a_output(
                        status='working',
                        text_content=f'도구 사용: {tool_name}',
                        metadata={
                            'event_type': 'tool_start',
                            'tool_name': tool_name,
                            'timestamp': datetime.now(pytz.UTC).isoformat(),
                        },
                        stream_event=True,
                        final=False,
                    )

            # Handle code execution events
            elif event_type == 'code_execution':
                language = event.get('language', '')
                code_snippet = event.get('code', '')[:100]  # First 100 chars
                return self.create_a2a_output(
                    status='working',
                    text_content=f'코드 실행 중 ({language}): {code_snippet}...',
                    data_content={
                        'language': language,
                        'code_preview': code_snippet,
                    },
                    metadata={
                        'event_type': 'code_execution',
                        'timestamp': datetime.now(pytz.UTC).isoformat(),
                    },
                    stream_event=True,
                    final=False,
                )

            # Handle Notion operation events
            elif event_type == 'notion_operation':
                operation_type = event.get('operation_type', '')
                resource_type = event.get('resource_type', '')
                return self.create_a2a_output(
                    status='working',
                    text_content=f'Notion 작업: {operation_type} {resource_type}',
                    data_content={
                        'operation_type': operation_type,
                        'resource_type': resource_type,
                    },
                    metadata={
                        'event_type': 'notion_operation',
                        'timestamp': datetime.now(pytz.UTC).isoformat(),
                    },
                    stream_event=True,
                    final=False,
                )

            # Check for completion
            if self.is_completion_event(event):
                return self.create_a2a_output(
                    status='completed',
                    text_content='작업이 완료되었습니다.',
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
        """Extract final output from the agent's state.

        Args:
            state: Final state from the LangGraph execution

        Returns:
            A2AOutput: Final standardized output
        """
        try:
            workflow_phase = state.get('workflow_phase', 'unknown')
            error = state.get('error')

            # Handle error state
            if error or workflow_phase == 'failed':
                failed_steps = state.get('failed_steps', [])
                error_details = {
                    'error': error,
                    'failed_steps_count': len(failed_steps),
                    'failed_steps': [
                        {
                            'step_id': step.get('step_id'),
                            'tool_name': step.get('tool_name'),
                            'error_message': step.get('error_message'),
                        }
                        for step in failed_steps[:3]  # Limit to first 3
                    ],
                }

                return self.create_a2a_output(
                    status='failed',
                    text_content=f'작업 실행 실패: {error}',
                    data_content=error_details,
                    metadata={
                        'workflow_phase': workflow_phase,
                        'timestamp': datetime.now(pytz.UTC).isoformat(),
                    },
                    final=True,
                    error_message=error,
                )

            # Extract messages for response
            messages = state.get('messages', [])
            response_text = ''

            for msg in reversed(messages):
                if isinstance(msg, AIMessage):
                    response_text = msg.content
                    break

            # Prepare data content with execution results
            data_content = {}

            # Include final result
            final_result = state.get('final_result')
            if final_result:
                data_content['final_result'] = final_result

            # Include code execution results
            execution_results = state.get('execution_results', [])
            if execution_results:
                data_content['code_outputs'] = [
                    {
                        'language': result.get('language'),
                        'output': result.get('output'),
                        'error': result.get('error'),
                        'execution_time': result.get('execution_time'),
                        'artifacts': result.get('artifacts', []),
                    }
                    for result in execution_results[:5]  # Limit to first 5
                ]

            # Include Notion operations
            notion_operations = state.get('notion_operations', [])
            if notion_operations:
                data_content['notion_operations'] = [
                    {
                        'operation_type': op.get('operation_type'),
                        'resource_type': op.get('resource_type'),
                        'resource_id': op.get('resource_id'),
                        'success': op.get('success'),
                    }
                    for op in notion_operations[:5]  # Limit to first 5
                ]

            # Include file operations
            created_files = state.get('created_files', [])
            modified_files = state.get('modified_files', [])
            if created_files or modified_files:
                data_content['file_operations'] = {
                    'created': created_files[:10],  # Limit to first 10
                    'modified': modified_files[:10],
                }

            # Include execution statistics
            completed_steps = state.get('completed_steps', [])
            if completed_steps:
                successful_steps = [
                    s for s in completed_steps if s.get('success')
                ]
                data_content['execution_stats'] = {
                    'total_steps': len(completed_steps),
                    'successful_steps': len(successful_steps),
                    'failed_steps': len(completed_steps)
                    - len(successful_steps),
                    'total_execution_time': state.get(
                        'total_execution_time', 0
                    ),
                }

            # Include tool usage statistics
            tool_usage_stats = state.get('tool_usage_stats', {})
            if tool_usage_stats:
                data_content['tool_usage'] = tool_usage_stats

            # Determine final status
            task_completed = state.get('task_completed', False)
            status = (
                'completed'
                if task_completed and workflow_phase == 'completed'
                else 'working'
            )

            return self.create_a2a_output(
                status=status,
                text_content=response_text or '작업이 완료되었습니다.',
                data_content=data_content if data_content else None,
                metadata={
                    'workflow_phase': workflow_phase,
                    'task_type': state.get('task_type', 'unknown'),
                    'task_completed': task_completed,
                    'timestamp': datetime.now(pytz.UTC).isoformat(),
                },
                final=True,
            )

        except Exception as e:
            logger.error(f'Error extracting final output: {e}')
            return self.format_error(
                e, 'Failed to extract task execution results'
            )

    def _get_node_display_name(self, node_name: str) -> str:
        """Get display-friendly name for a node.

        Args:
            node_name: Internal node name

        Returns:
            str: Display-friendly name
        """
        display_names = {
            'analyze_task': '작업 분석',
            'prepare_tools': '도구 준비',
            'plan_execution': '실행 계획',
            'execute_step': '단계 실행',
            'validate_step_result': '결과 검증',
            'aggregate_results': '결과 집계',
            'handle_error': '오류 처리',
        }
        return display_names.get(node_name, node_name)

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
            url = f"http://executor-agent:{os.getenv('AGENT_PORT', '8003')}"

        skills = [
            create_agent_skill(
                skill_id="execute-task",
                name="작업 실행",
                description="다양한 작업을 실행하고 결과를 반환합니다.",
                tags=["executor", "task", "automation", "code"],
                examples=[
                    "이 코드를 실행해주세요",
                    "데이터 분석을 수행해주세요",
                    "파일을 생성하고 내용을 작성해주세요"
                ],
            ),
            create_agent_skill(
                skill_id="code-execution",
                name="코드 실행",
                description="Python, JavaScript 등의 코드를 실행하고 결과를 반환합니다.",
                tags=["code", "execution", "python", "javascript"],
                examples=[
                    "이 Python 스크립트를 실행해주세요",
                    "JavaScript 코드를 테스트해주세요"
                ],
            ),
        ]

        logger.info("A2A agent card created")

        return create_agent_card(
            name="TaskExecutorAgent",
            description="다양한 작업을 실행하고 관리하기 위한 Agent입니다.",
            url=url,
            skills=skills,
        )


# Factory function for creating A2A-compatible Task Executor Agent
async def create_task_executor_a2a_agent(
    model: Any | None = None,
    is_debug: bool = False,
    check_pointer: Any | None = None,
) -> TaskExecutorA2AAgent:
    """Create and initialize a Task Executor A2A Agent.

    Args:
        model: LLM model
        is_debug: Debug mode flag
        check_pointer: Checkpoint manager

    Returns:
        TaskExecutorA2AAgent: Initialized A2A agent instance
    """
    return TaskExecutorA2AAgent(
        model=model,
        check_pointer=check_pointer,
        is_debug=is_debug,
    )


def main() -> None:
    """TaskExecutorAgent A2A 서버 실행.

    이 함수는 서버 실행의 진입점으로, 다음 작업을 수행합니다:
    1. 로깅 설정
    2. 비동기 초기화 실행
    3. 환경 설정 로드
    4. A2A 서버 생성 및 실행
    """

    async def async_init() -> TaskExecutorA2AAgent | None:
        """비동기 초기화 헬퍼 함수.

        MCP 서버와의 비동기 연결이 필요하므로 별도의 비동기 함수로 분리.

        Returns:
            TaskExecutorA2AAgent: 초기화된 A2A 래퍼 인스턴스 또는 None
        """
        try:
            # TaskExecutorA2AAgent 인스턴스 생성 (디버그 모드 활성화)
            _a2a_wrapper = TaskExecutorA2AAgent(is_debug=True)

            # 비동기 초기화 실행 및 결과 확인
            if not await _a2a_wrapper.initialize():
                logger.error("❌ TaskExecutorAgentA2A 초기화 실패")
                return None

            logger.info("✅ TaskExecutorAgentA2A 초기화 완료")
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
        port = int(os.getenv("AGENT_PORT", "8003"))
        url = f"http://{host}:{port}"

        agent_card = a2a_agent.get_agent_card(url)

        # LangGraphAgentExecutor로 래핑
        executor = LangGraphAgentExecutor(
            agent_class=TaskExecutorA2AAgent,
            is_debug=True
        )

        # A2A 서버 생성
        handler = build_request_handler(executor)
        server_app = build_a2a_starlette_application(
            agent_card=agent_card,
            handler=handler
        )

        # 서버 시작 정보 로깅
        logger.info(f"✅ TaskExecutorAgent A2A server starting at {url} with CORS enabled")
        logger.info(f"📋 Agent Card URL: {url}/.well-known/agent-card.json")  # A2A 표준 메타데이터 엔드포인트
        logger.info(f"🩺 Health Check: {url}/health")  # 헬스체크 엔드포인트

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
