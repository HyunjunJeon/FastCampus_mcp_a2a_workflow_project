"""LangGraph A2A Agent Executor V2.

This module provides a clean integration between LangGraph agents with A2A interface
and the A2A protocol, leveraging standardized output formats for both streaming and polling.

한글 설명:
- 본 모듈은 LangGraph 기반 에이전트를 A2A 프로토콜과 자연스럽게 연동하기 위한 실행기(Executor)를 제공합니다.
- 각 에이전트는 표준화된 A2A 인터페이스(`BaseA2AAgent`)를 구현한다고 가정하며, 이 인터페이스를 통해 결과를 규격화된
  메시지 파츠(`TextPart`, `DataPart`)로 변환하여 스트리밍/블로킹 모드 모두에서 일관된 출력 형태를 보장합니다.
- 목표는 에이전트별 커스텀 결과 추출/스트리밍 로직을 최소화하고, 공통 실행 흐름(초기화 → 입력 처리 → 실행 → 아티팩트 생성
  → 상태 업데이트/이벤트 전송)을 단순하고 예측 가능하게 만드는 것입니다.
"""

from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Any, cast
from uuid import uuid4

import pytz
import structlog

from a2a.client.helpers import create_text_message_object
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import InMemoryTaskStore, TaskManager, TaskUpdater
from a2a.types import (
    Artifact,
    DataPart,
    Message,
    Part,
    Task,
    TaskState,
    TaskStatus,
    TextPart,
)
from a2a.utils import (
    new_agent_parts_message,
    new_agent_text_message,
)

from src.a2a_integration.models import LangGraphExecutorConfig
from src.base.a2a_interface import A2AOutput, BaseA2AAgent


logger = structlog.get_logger(__name__)

class LangGraphAgentExecutor(AgentExecutor):
    """Simplified A2A Agent Executor for LangGraph agents with A2A interface.

    This executor leverages the standardized A2A interface implemented by each
    LangGraph agent, eliminating the need for custom result extractors and
    complex streaming logic.

    한글 설명:
    - 각 LangGraph 에이전트가 제공하는 표준 A2A 인터페이스를 활용하여 실행 결과를 A2A 메시지로 변환합니다.
    - 별도의 에이전트별 커스텀 파서 없이도 공통 규격(`A2AOutput`)을 통해 텍스트/데이터 파츠를 생성하고,
      스트리밍/블로킹 모드를 모두 지원합니다.
    - 설계 의도: 에이전트 교체/확장 시 실행기의 변경을 최소화하고, 상태 업데이트/이벤트 전송을 일관되게 처리합니다.
    """

    def __init__(
        self,
        agent_class: type[BaseA2AAgent],
        config: LangGraphExecutorConfig | None = None,
        **agent_kwargs: Any,
    ):
        """Initialize the LangGraph A2A Executor.

        Args:
            agent_class: The A2A-enabled agent class to instantiate
            config: Configuration for the executor
            **agent_kwargs: Additional arguments to pass to the agent constructor

        한글 설명:
        - `agent_class`는 `BaseA2AAgent`를 구현한 에이전트의 타입입니다. 실제 인스턴스는
          지연 초기화(`_ensure_agent_initialized`) 시점에 생성됩니다.
        - `config`는 스트리밍 활성화 여부 등 실행 동작을 제어합니다.
        - `task_store`/`task_manager`/`TaskUpdater`/`EventQueue`는 A2A 프로토콜의 작업(Task)
          라이프사이클(생성 → 진행 → 완료/실패)과 이벤트 전송을 담당합니다.
        - 설계 선택: 실행기 내부에서 작업 저장소는 메모리 기반(`InMemoryTaskStore`)을 기본으로 사용합니다.
          외부 주입을 고려한다면 생성자 인자로 교체 가능하도록 확장할 수 있습니다.
        """
        self.agent_class = agent_class
        self.agent_kwargs = agent_kwargs
        self.config = config or LangGraphExecutorConfig()
        self.agent: BaseA2AAgent | None = None
        self.task_store = InMemoryTaskStore()
        self.task_manager: TaskManager | None = None
        self.updater: TaskUpdater | None = None
        self.event_queue: EventQueue | None = None

        logger.info(
            f'LangGraphAgentExecutorV2 initialized for {agent_class.__name__}'
        )

    async def _ensure_agent_initialized(self) -> None:
        """Ensure the agent is initialized.

        한글 설명:
        - 에이전트 인스턴스가 아직 생성되지 않았으면 생성 후, 초기화 메서드(`initialize`)가 존재할 경우
          비동기로 초기화를 수행합니다.
        - 실패 시 런타임 오류로 래핑하여 상위 호출자에서 일관되게 처리할 수 있게 합니다.
        - 왜 필요한가: 실행 전에 모델/그래프/리소스 초기화가 선행되어야 안정적인 처리와
          예측 가능한 상태 전이가 가능합니다.
        """
        if not self.agent:
            try:
                # Create agent instance
                # NOTE: 지연 초기화로 불필요한 자원 사용을 피하고, 구성 변경을 용이하게 합니다.
                self.agent = self.agent_class(**self.agent_kwargs)

                # Initialize if it has an initialize method
                if hasattr(self.agent, 'initialize'):
                    # 일부 에이전트는 외부 서비스 연결, 모델 로딩 등 비용이 큰 작업을 수행할 수 있습니다.
                    await self.agent.initialize()
                    logger.info(f'Agent {self.agent.agent_type} initialized')

            except Exception as e:
                logger.error(f'Failed to initialize agent: {e}')
                raise RuntimeError(f'Agent initialization failed: {e}') from e

    async def execute(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        """Execute the A2A request using the standardized agent interface.

        Args:
            context: A2A request context
            event_queue: Event queue for sending messages

        한글 설명(흐름 개요):
        1) 에이전트 초기화 보장 → 2) 입력 정규화(JSON 페이로드 또는 사용자 메시지) →
        3) 작업(Task) 생성/복구 및 상태 추적자(`TaskUpdater`) 구성 →
        4) 실행 모드 결정(블로킹/스트리밍) → 5) 실행 및 결과를 A2A 아티팩트로 래핑하여 이벤트 전송 →
        6) 완료 상태로 마무리. 오류 발생 시 실패 상태로 업데이트하고 에러 메시지 전송.
        설계 의도: 상태 전이(제출 → 작업 중 → 완료/실패)를 중앙화하여 API 소비자가
        일관된 생명주기를 관찰하도록 합니다.
        """
        try:
            logger.info(
                f'Starting A2A agent execution for {self.agent_class.__name__}'
            )

            # Ensure agent is initialized
            await self._ensure_agent_initialized()

            # Process input
            # NOTE: A2A 메시지의 `DataPart`를 우선 사용하여 구조화된 호출을 지원하고,
            #       없으면 사용자 텍스트 쿼리를 기본 메시지로 변환합니다.
            input_dict = await self._process_input(context)
            logger.info(f'Processed input: {type(input_dict)}')

            # Setup task updater
            task_id = cast('str', context.task_id)
            context_id = getattr(context, 'context_id', task_id)
            user_message = create_text_message_object(
                content=input_dict.get('messages', [{}])[0].get('content', '')
            )

            task = context.current_task
            logger.info(f'[Execute] Task: {task}')
            if not task:
                # 기존 컨텍스트에 작업이 없으면 새 작업을 생성하여 제출 상태로 브로드캐스트합니다.
                task = Task(
                    id=task_id,
                    context_id=context_id,
                    status=TaskStatus(
                        message=user_message,
                        state=TaskState.submitted,
                        timestamp=datetime.now(
                            tz=pytz.timezone('Asia/Seoul')
                        ).isoformat(),
                    ),
                )
                await event_queue.enqueue_event(task)
                logger.info(f'New task created and enqueued: {task_id}')
            else:
                logger.info(f'Using existing task from context: {task_id}')

            self.task_manager = TaskManager(
                task_id=task_id,
                context_id=context_id,
                task_store=self.task_store,
                initial_message=user_message,
            )
            self.updater = TaskUpdater(
                event_queue=event_queue, task_id=task_id, context_id=context_id
            )
            self.event_queue = event_queue

            is_blocking = self._is_blocking_mode(context)
            logger.info(
                f'Execution mode - blocking: {is_blocking}, '
                f'streaming enabled: {self.config.enable_streaming}'
            )

            # 작업 상태를 "working"으로 일관되게 전환합니다.
            await self.updater.update_status(TaskState.working)
            if is_blocking or not self.config.enable_streaming:
                # 블로킹 모드: 최종 결과만 전송합니다.
                output = await self._execute_blocking(input_dict, context_id)
                logger.info(f'Blocking execution output: {output}')
            else:
                # 스트리밍 모드: 이벤트 단위로 중간 결과를 전송합니다.
                output = await self._execute_streaming(input_dict, context_id)
                logger.info(f'Streaming execution output: {output}')

            # 실행 결과를 아티팩트로 래핑하여 최종 Task 이벤트에 포함합니다.
            artifact = Artifact(
                artifact_id=str(uuid4()),
                parts=output.parts,
            )
            task = Task(
                id=task_id,
                context_id=context_id,
                artifacts=[artifact],
                status=TaskStatus(
                    state=TaskState.completed,
                    timestamp=datetime.now(
                        tz=pytz.timezone('Asia/Seoul')
                    ).isoformat(),
                ),
            )
            await self.event_queue.enqueue_event(task)
            await self.updater.complete()

        except Exception as e:
            logger.error(f'Critical error in executor: {e}')
            try:
                # 실패 시에도 소비자가 상태를 인지할 수 있도록 실패(TaskState.failed)로 업데이트합니다.
                updater = TaskUpdater(
                    event_queue=event_queue,
                    task_id=cast('str', context.task_id),
                    context_id=str(
                        getattr(context, 'context_id', context.task_id)
                    ),
                )
                await updater.update_status(
                    TaskState.failed,
                    new_agent_text_message(
                        f'작업 중 오류가 발생했습니다: {e!s}'
                    ),
                    final=True,
                )
            except Exception as update_error:
                logger.error(f'Failed to update error status: {update_error}')
            raise

    async def _execute_blocking(
        self,
        input_dict: dict[str, Any],
        context_id: str,
    ) -> Message:
        """Execute in blocking mode (no streaming).

        한글 설명:
        - 스트리밍 없이 에이전트를 한 번 호출하여 최종 결과만 반환합니다.
        - LangGraph 스레드 분리를 위해 `configurable.thread_id`에 `context_id`를 지정합니다.
        - 반환값은 `A2AOutput` 규격의 딕셔너리여야 하며, 이후 `_send_a2a_output`으로 메시지 파츠로 변환됩니다.
        - 주의: 상태 전이는 이 메서드 내부에서 변경하지 않습니다(상태 일관성 확보).
        """
        logger.info('Using blocking execution mode')

        try:
            # Execute the agent using standardized interface
            # 표준 인터페이스: `execute_for_a2a(input_dict, config)`는 A2AOutput(dict)을 반환해야 합니다.
            config = {'configurable': {'thread_id': context_id}}
            result = await self.agent.execute_for_a2a(input_dict, config)

            logger.info(
                f'Agent execution completed, result type: {type(result)}'
            )
            logger.info(
                f'Result keys: {list(result.keys()) if isinstance(result, dict) else "Not a dict"}'
            )
            logger.info(
                f'Agent execution completed, status: {result.get("status")}'
            )
            logger.info(f'Result final flag: {result.get("final", "Not set")}')
            logger.info('===========' * 10)
            logger.info(f'Result: {result}')
            logger.info('===========' * 10)

            # Send the result based on A2AOutput format
            # NOTE: 이 안에서 상태 변경 금지.
            # TODO: [State Management] 상태 변경 처리 전략 및 트랜잭션 보장 방안 필요
            # - 이유: 상태 업데이트와 메시지 전송을 분리하여 경쟁 상태를 줄이고, 재시도/보상 트랜잭션을 용이하게 하기 위함.
            last_message = await self._send_a2a_output(result)
            logger.info(f'Last message: {last_message}')

            return last_message

        except Exception as e:
            logger.error(f'Blocking execution failed: {e}')
            raise

    async def _execute_streaming(
        self,
        input_dict: dict[str, Any],
        context_id: str,
    ) -> AsyncGenerator[Message, None]:
        """Execute with streaming support.

        한글 설명:
        - 에이전트의 `graph.astream_events`를 구독하여 이벤트 단위로 결과를 생성합니다.
        - 각 이벤트는 에이전트의 `format_stream_event`에 의해 `A2AOutput`으로 정규화되며,
          `_send_a2a_output`을 통해 A2A 메시지로 전송됩니다.
        - 완료 신호는 (1) 에이전트가 `final=True`로 명시하거나, (2) 이벤트 패턴을 통해 감지합니다.
        - 스트리밍 종료 후에도 미완료라면 그래프 스냅샷에서 최종 결과를 추출하여 전송합니다.
        """
        logger.info('Using streaming execution mode')

        try:
            # For streaming, we need to hook into the agent's graph events
            # This requires the agent to have a graph attribute
            if not hasattr(self.agent, 'graph'):
                # 스트리밍 미지원 에이전트는 블로킹 모드로 폴백합니다.
                logger.warning(
                    "Agent doesn't support streaming, falling back to blocking"
                )
                await self._execute_blocking(input_dict, context_id)
                return

            # Track completion
            is_completed = False
            event_count = 0

            # Stream events from the graph
            async for event in self.agent.graph.astream_events(
                input_dict, config={'configurable': {'thread_id': context_id}}
            ):
                event_count += 1

                # Let the agent format the streaming event
                # 이벤트를 에이전트 전용 포맷터로 정규화(A2AOutput)합니다.
                formatted_output = self.agent.format_stream_event(event)

                if formatted_output:
                    _message = await self._send_a2a_output(formatted_output)
                    yield _message

                    # Check if this is a completion event
                    # 에이전트가 명시적으로 완료를 알린 경우 즉시 종료합니다.
                    if formatted_output.get('final', False):
                        is_completed = True
                        logger.info('Completion detected from agent')
                        break

                # Check for completion patterns in raw event
                # 에이전트가 명시하지 않아도, 이벤트 타입/노드명으로 완료를 추론할 수 있습니다.
                if not is_completed and self._is_completion_event(event):
                    is_completed = True
                    logger.info('Completion detected from event pattern')
                    break

            # If not completed yet, get final state
            if not is_completed:
                logger.info('Streaming ended, extracting final state')

                # Get the final state from the graph
                # 마지막 스냅샷에서 최종 결과를 재구성하여 누락된 종료 메시지를 보완합니다.
                state_snapshot = await self.agent.graph.aget_state(
                    config={'configurable': {'thread_id': context_id}}
                )

                if state_snapshot and state_snapshot.values:
                    # Extract final output using agent's method
                    final_output = self.agent.extract_final_output(
                        state_snapshot.values
                    )

                    # Send final output
                    # 스트리밍 종료 메시지로 최종 결과를 전송합니다.
                    _message = await self._send_a2a_output(final_output)
                    yield _message

            logger.info(f'Streaming complete - Events: {event_count}')

        except Exception as e:
            logger.error(f'Streaming execution failed: {e}')
            raise

    async def _send_a2a_output(
        self,
        output: A2AOutput,
    ) -> Message:
        """Send A2AOutput as appropriate A2A message parts.

        Args:
            output: Standardized A2A output from agent

        한글 설명:
        - `A2AOutput` 딕셔너리의 내용(텍스트/데이터/상태/에이전트 타입)을 읽어 A2A `Message`의
          파츠 리스트로 변환합니다.
        - 최소 1개 파츠를 보장하기 위해 텍스트/데이터가 없을 때는 폴백 텍스트를 생성합니다.
        - 상태 필드는 상위의 상태 전이와 분리되어 있으며, 순수 출력 포맷에만 관여합니다.
        """
        try:
            # A2AOutput 내용 전체 로깅
            logger.info(f'Full A2AOutput received: {output}')

            status = output.get('status', 'working')
            text_content = output.get('text_content')
            data_content = output.get('data_content')
            agent_type = output.get('agent_type', 'Unknown')

            parts = []

            if text_content:
                parts.append(Part(root=TextPart(text=text_content)))

            if data_content:
                parts.append(Part(root=DataPart(data=data_content)))

            # Ensure we always send something - create fallback content if parts is empty
            # 폴백: 텍스트/데이터가 전혀 없을 경우, 사용자가 최소한의 진행 상황을 인지하도록
            #       에이전트 타입과 상태 정보를 합성하여 전송합니다.
            if not parts:
                # Create fallback text with agent and status information
                agent_type = output.get('agent_type', 'Agent')
                fallback_text = f'{agent_type} - {status}'

                # Include error message if available
                error_msg = output.get('error_message')
                if error_msg:
                    fallback_text += f': {error_msg}'

                parts.append(Part(root=TextPart(text=fallback_text)))
                logger.warning(
                    f'No content provided, sending fallback text: {fallback_text}'
                )

            return new_agent_parts_message(parts)

        except Exception as e:
            logger.error(f'Failed to send A2A output: {e}')

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        """Cancel an ongoing task.

        Args:
            context: Request context
            event_queue: Event queue

        한글 설명:
        - 진행 중인 작업이 존재하는 경우 `TaskUpdater.cancel()`을 호출하여 취소 상태를 전파합니다.
        - 설계 의도: 취소 또한 정상적인 상태 전이의 일부로 취급하여, 구독자가 예측 가능한 시맨틱을 갖도록 합니다.
        """
        logger.info(f'Cancelling task: {context.task_id}')

        if context.current_task:
            updater = TaskUpdater(
                event_queue=event_queue,
                task_id=context.current_task.id,
                context_id=str(context.context_id),
            )
            await updater.cancel()
            logger.info(f'Task {context.task_id} cancelled')

    # Helper methods

    async def _process_input(self, context: RequestContext) -> dict[str, Any]:
        """Process input from request context.

        한글 설명:
        - A2A 요청 컨텍스트에서 입력을 정규화합니다. 우선순위는 다음과 같습니다.
          1) 메시지 파츠 내 `DataPart`의 구조화된 페이로드
          2) 사용자 텍스트 질의(`context.get_user_input`)를 메시지 포맷으로 래핑
          3) 둘 다 없으면 빈 메시지 배열
        - 이유: 구조화된 입력은 에이전트가 더 풍부한 컨텍스트로 동작할 수 있게 하며, 텍스트 입력은 기본 UX를 보장합니다.
        """
        query = context.get_user_input()

        # Try to get structured data from DataPart
        # 메시지에 첨부된 `DataPart`에서 마지막 항목을 우선 페이로드로 사용합니다.
        payload = {}
        if context.message and getattr(context.message, 'parts', None):
            try:
                from a2a.utils import get_data_parts

                data_parts = get_data_parts(context.message.parts)
                if data_parts:
                    last_part = data_parts[-1]
                    if isinstance(last_part, dict):
                        payload = last_part
            except Exception as e:
                logger.debug(f'No DataPart found: {e}')

        # Return appropriate format
        # 반환 우선순위: DataPart 페이로드 > 텍스트 메시지 > 빈 메시지
        if payload:
            return payload
        if query:
            return {'messages': [{'role': 'user', 'content': query}]}
        return {'messages': []}

    def _is_blocking_mode(self, context: RequestContext) -> bool:
        """Check if blocking mode is requested.

        한글 설명:
        - 컨텍스트 요청 설정에 `blocking=True`가 지정된 경우 블로킹 모드로 판단합니다.
        - 설계 의도: 호출자(클라이언트)가 명시적으로 동기/비동기 전략을 제어할 수 있게 합니다.
        """
        if hasattr(context, 'request') and context.request and (
            hasattr(context.request, 'configuration')
            and context.request.configuration
        ):
            return getattr(context.request.configuration, 'blocking', False)
        return False

    def _is_completion_event(self, event: dict[str, Any]) -> bool:
        """Check if an event indicates completion.

        한글 설명:
        - 이벤트의 타입/노드명을 기반으로 완료를 추론합니다. 명시적 완료 신호가 누락된 경우의 보완 장치입니다.
        - 현재 휴리스틱: `event == on_chain_end` 이고 `name ∈ {__end__, aggregate, complete}`
        """
        event_type = event.get('event', '')

        if event_type == 'on_chain_end':
            node_name = event.get('name', '')
            if node_name in ['__end__', 'aggregate', 'complete']:
                return True

        return False

    def _map_status_to_task_state(self, status: str) -> TaskState:
        """Map A2AOutput status to TaskState.

        한글 설명:
        - `A2AOutput.status` 문자열을 A2A의 `TaskState` 열거형으로 매핑합니다.
        - 기본값은 `working`이며 미지의 상태에 대해 보수적으로 동작합니다.
        """
        mapping = {
            'working': TaskState.working,
            'completed': TaskState.completed,
            'failed': TaskState.failed,
            'input_required': TaskState.input_required,
        }
        mapped_state = mapping.get(status, TaskState.working)
        logger.info(
            f"Status mapping - input: '{status}' -> output: {mapped_state}"
        )
        return mapped_state
