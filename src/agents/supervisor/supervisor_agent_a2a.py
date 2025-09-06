"""SupervisorAgent A2A 서버 (표준 A2A 인터페이스 사용).
표준화된 A2A 인터페이스를 사용하여 SupervisorAgent를 A2A 프로토콜로 제공합니다.
"""  # noqa: D205

from __future__ import annotations

import json
import logging
import os

from contextlib import suppress
from datetime import datetime
from typing import TYPE_CHECKING, Any, cast

import structlog
import uvicorn

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.tasks import InMemoryTaskStore, TaskUpdater
from a2a.types import (
    AgentCard,
    DataPart,
    Part,
    TaskState,
    TaskStatusUpdateEvent,
    TextPart,
)
from a2a.utils import new_agent_parts_message, new_agent_text_message

from src.a2a_integration.a2a_lg_client_utils import A2AClientManager
from src.a2a_integration.a2a_lg_server_utils import (
    build_a2a_starlette_application,
    build_request_handler,
    create_agent_card,
    create_agent_skill,
)
from src.a2a_integration.cors_utils import create_cors_enabled_app
from src.base.util import load_env_file


if TYPE_CHECKING:
    from a2a.server.events import EventQueue


load_env_file()

logger = structlog.get_logger(__name__)


# (no preview text limit)


class CustomSupervisorAgentA2A(AgentExecutor):
    """SupervisorAgent A2A 서버 - 표준 A2A 인터페이스 사용한 직접 개발.

    LangGraph 를 사용하지 않음.

    워크플로우 상태를 추적하고, 각 에이전트의 작업 상태 조회 기능 및 최종 결과물을 사용자에게 제공합니다.
    """

    def __init__(self) -> None:
        """SupervisorAgent A2A 서버 초기화."""
        self.agent_urls = {}
        self.task_store = InMemoryTaskStore()
        self.task_managers: dict[str, TaskUpdater] = {}
        # 컨텍스트별 대화 히스토리 저장 (간단한 인메모리)
        self.conversation_histories: dict[str, list[dict[str, Any]]] = {}


    async def _ensure_agent_initialized(self) -> None:
        """SupervisorA2AAgent 초기화 - 다른 A2A 에이전트들의 URL 설정."""
        if not self.agent_urls:
            try:
                # 환경에 따라 다른 A2A 에이전트들의 URL 설정
                is_docker = os.getenv('IS_DOCKER', 'false').lower() == 'true'

                if is_docker:
                    # Docker 환경에서는 컨테이너명 사용
                    self.agent_urls = {
                        'planner': os.getenv(
                            'PLANNER_URL', 'http://planner-agent:8001'
                        ),
                        'knowledge': os.getenv(
                            'KNOWLEDGE_URL', 'http://knowledge-agent:8002'
                        ),
                        'browser': os.getenv(
                            'BROWSER_URL', 'http://browser-agent:8003'
                        ),
                        'executor': os.getenv(
                            'EXECUTOR_URL', 'http://executor-agent:8004'
                        ),
                    }
                else:
                    # 로컬 환경에서는 localhost 사용
                    self.agent_urls = {
                        'planner': os.getenv(
                            'PLANNER_URL', 'http://localhost:8001'
                        ),
                        'knowledge': os.getenv(
                            'KNOWLEDGE_URL', 'http://localhost:8002'
                        ),
                        'browser': os.getenv(
                            'BROWSER_URL', 'http://localhost:8003'
                        ),
                        'executor': os.getenv(
                            'EXECUTOR_URL', 'http://localhost:8004'
                        ),
                    }

                logger.info(
                    f'SupervisorA2AAgent initialized with URLs: {self.agent_urls}'
                )
            except Exception as e:
                logger.error(f'Failed to initialize SupervisorA2AAgent: {e}')
                raise RuntimeError(f'Agent initialization failed: {e}') from e

    async def _call_agent(
        self, agent_type: str, query: str, context_id: str
    ) -> dict[str, Any]:
        """A2A SDK를 사용한 에이전트 호출."""
        agent_url = self.agent_urls.get(agent_type)
        if not agent_url:
            raise ValueError(f'Unknown agent type: {agent_type}')

        # A2A 호출 메시지 구성 + 멀티턴을 위한 conversation/context 정보 포함
        input_data = {
            'messages': [{'role': 'user', 'content': query}],
            'conversation_id': context_id,
            'context_id': context_id,
            'history': self._get_history(context_id),
        }

        try:
            # A2A SDK를 사용
            a2a_client_manager = A2AClientManager(
                base_url=agent_url,
                streaming=False,
                retry_delay=5.0,
            )
            await a2a_client_manager.initialize()

            # 통합 응답을 위해 parts 전송을 사용 (텍스트/데이터 모두 수집)
            unified = await a2a_client_manager.send_parts(
                parts=[Part(root=DataPart(data=input_data))],
                context_id=context_id,
            )

            # 텍스트가 비어있으면 데이터 기반 미리보기 생성 (제한 없이)
            merged_text = unified.merged_text or ''.join(unified.text_parts)
            if not merged_text and unified.merged_data:
                try:
                    merged_text = json.dumps(unified.merged_data, ensure_ascii=False)
                except Exception:
                    merged_text = ''

            # 표준화된 응답 딕셔너리로 변환
            return {
                'text_content': merged_text,
                'data_parts': unified.data_parts,
                'data_content': unified.merged_data,
                'event_count': unified.event_count,
            }

        except Exception as e:
            error_msg = f'Failed to call {agent_type} agent via A2A SDK: {e!s}'
            logger.error(error_msg)
            return {'error': error_msg}

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Execute supervisor workflow using A2A interface.

        Uses the standardized SupervisorA2AAgent which handles all sub-agent
        orchestration internally.
        """
        try:
            logger.info(
                '[SUPERVISOR] 워크플로우 오케스트레이션 시작 - A2A Protocol'
            )

            await self._ensure_agent_initialized()

            input_dict = await self._process_input(context)

            task_id = cast('str', context.task_id)
            context_id = str(getattr(context, 'context_id', task_id))
            # 입력 payload에 명시된 context_id/conversation_id가 있으면 우선 사용
            try:
                payload_cid = input_dict.get('context_id') or input_dict.get('conversation_id')
                if payload_cid:
                    context_id = str(payload_cid)
            except Exception:
                pass

            updater = TaskUpdater(
                event_queue=event_queue,
                task_id=task_id,
                context_id=context_id,
            )

            # payload가 history를 포함하면 저장소 초기화 (클라이언트 제공 히스토리 우선)
            try:
                payload_history = input_dict.get('history')
                if isinstance(payload_history, list):
                    self.conversation_histories[context_id] = [
                        m for m in payload_history if isinstance(m, dict)
                    ]
            except Exception:
                pass

            # 이번 입력 메시지를 히스토리에 추가
            try:
                incoming_messages = input_dict.get('messages', [])
                if isinstance(incoming_messages, list):
                    self._append_history(context_id, incoming_messages)
            except Exception:
                pass

            await updater.start_work()
            result = await self._execute_workflow(
                input_dict,
                updater,
                context_id,
                task_id,
            )

            logger.info(
                f'[SUPERVISOR] 작업 처리 완료 - 상태: {result.get("status", "unknown")}'
            )

            await self._send_a2a_output(result, updater, event_queue, context_id)

            # 최종 결과 텍스트를 assistant 메시지로 히스토리에 추가
            try:
                final_text = result.get('text_content')
                if final_text:
                    self._append_history(
                        context_id,
                        [{'role': 'assistant', 'content': str(final_text)}],
                    )
            except Exception:
                pass

        except Exception as e:
            logger.error(f'SupervisorAgent execution failed: {e}')
            # Send error status
            try:
                await updater.update_status(
                    TaskState.failed,
                    new_agent_text_message(
                        f'작업 중 오류가 발생했습니다: {e!s}',
                        context_id=context_id,
                        task_id=task_id,
                    ),
                    final=True,
                )
            except Exception as update_error:
                logger.error(f'Failed to update error status: {update_error}')
            raise

    async def _process_input(self, context: RequestContext) -> dict:
        """Process input from A2A request context."""
        query = context.get_user_input()

        try:
            data = json.loads(query)
            if isinstance(data, dict) and 'messages' in data:
                return data
        except json.JSONDecodeError:
            pass

        # Fallback to simple message format
        return {'messages': [{'role': 'user', 'content': query}]}

    async def _send_a2a_output(
        self,
        output: dict,
        updater: TaskUpdater,
        event_queue: EventQueue,
        context_id: str,
    ) -> None:
        """Send A2AOutput as A2A message parts."""
        try:
            status = output.get('status', 'working')
            text_content = output.get('text_content')
            data_content = output.get('data_content')
            is_final = output.get('final', False)

            # Build message parts
            parts = []

            # Add text part if present
            if text_content:
                parts.append(TextPart(text=str(text_content)))

            # Add data part if present
            if data_content:
                # 구조화된 응답 데이터 보장
                structured_data = {
                    'data_content': data_content,
                    'metadata': {
                        'timestamp': datetime.now().isoformat(),
                        'agent': 'supervisor',
                        'status': status,
                    },
                }
                parts.append(DataPart(data=dict(structured_data)))

            # Send message if we have parts
            if parts:
                message = new_agent_parts_message(parts)

                # final인 경우 complete, 아니면 일반 메시지
                if is_final:
                    await updater.complete(message)
                else:
                    # 중간 상태 업데이트도 TaskUpdater를 통해 context/task 메타 부여
                    await updater.update_status(TaskState.working, message, final=False)

                logger.info(
                    f'Sent message with {len(parts)} parts (final={is_final})'
                )

                # 히스토리에 assistant 메시지 추가 (텍스트 우선, 없으면 데이터 요약)
                try:
                    history_text = text_content
                    if not history_text and data_content is not None:
                        try:
                            history_text = json.dumps(data_content, ensure_ascii=False)
                        except Exception:
                            history_text = ''
                    if history_text:
                        self._append_history(
                            context_id,
                            [{'role': 'assistant', 'content': str(history_text)}],
                        )
                except Exception:
                    pass

        except Exception as e:
            logger.error(f'Failed to send A2A output: {e}')
            raise

    async def _emit_progress_update(
        self,
        updater: TaskUpdater,
        text: str,
        data: dict[str, Any] | None = None,
    ) -> None:
        """중간 진행 상황 업데이트 메시지를 전송한다 (polling으로 수신 가능)."""
        try:
            parts = [TextPart(text=str(text))]
            if data is not None:
                parts.append(DataPart(data=dict(data)))
            message = new_agent_parts_message(parts)
            await updater.update_status(TaskState.working, message, final=False)
        except Exception as e:
            logger.warning(f'Failed to emit progress update: {e}')

    def _append_history(self, context_id: str, messages: list[dict[str, Any]]) -> None:
        """컨텍스트별 대화 히스토리에 메시지들을 추가한다."""
        if not messages:
            return
        hist = self.conversation_histories.setdefault(context_id, [])
        for msg in messages:
            if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                hist.append({'role': msg.get('role'), 'content': msg.get('content', '')})

    def _get_history(self, context_id: str) -> list[dict[str, Any]]:
        """컨텍스트별 대화 히스토리를 반환한다 (복사본)."""
        return list(self.conversation_histories.get(context_id, []))

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Cancel an ongoing task."""
        logger.info(f'Cancelling task: {context.task_id}')

        if context.current_task:
            updater = TaskUpdater(
                event_queue=event_queue,
                task_id=context.current_task.id,
                context_id=str(context.context_id),
            )
            await updater.cancel()
            await event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    task_id=context.current_task.id,
                    context_id=str(context.context_id),
                    status=TaskState.cancelled,
                    final=True,
                )
            )
            logger.info(f'Task {context.context_id} cancelled')

    def get_agent_card(self, url: str) -> AgentCard:
        """A2A AgentCard 생성."""
        if os.getenv('IS_DOCKER', 'false').lower() == 'true':
            url = f'http://supervisor-agent:{os.getenv("AGENT_PORT", "8000")}'

        _skill = create_agent_skill(
            skill_id='automation_orchestrator',
            name='AI 업무 자동화 워크플로우 오케스트레이션',
            description='사용자 요청을 분석하여 최적 워크플로우를 결정하고 실행합니다',
            tags=['supervisor', 'orchestration', 'workflow', 'automation'],
        )

        return create_agent_card(
            name='SupervisorAgent',
            description='FastCampus - MCP & A2A - AI 업무 자동화 시스템의 오케스트레이터',
            url=url,
            version='1.0.0',
            skills=[_skill],
        )

    def _extract_user_query(self, input_dict: dict[str, Any]) -> str:
        """Extract user query from input dictionary.

        Args:
            input_dict: Input dictionary containing messages

        Returns:
            str: Extracted user query
        """
        messages = input_dict.get('messages', [])

        for msg in messages:
            if msg.get('role') == 'user':
                return msg.get('content', '')

        return ''

    async def _get_workflow_status(self, task_id: str | None) -> dict[str, Any]:
        """Get workflow status for a given task.

        Args:
            task_id: Task ID to check status for

        Returns:
            dict: Status information
        """
        if task_id and task_id in self.task_managers:
            # TaskUpdater만 저장하므로 상세 Task 정보 접근은 생략하고 working 상태만 전달
            return {
                'status': 'working',
                'text_content': f'작업 {task_id} 진행 중입니다',
                'data_content': {
                    'task_id': task_id,
                },
                'final': False,
            }

        # Default status if task not found
        return {
            'status': 'completed',
            'text_content': f'작업 상태 조회: {"작업을 찾을 수 없습니다" if task_id else "진행 중인 작업이 없습니다"}',
            'data_content': None,
            'final': True,
        }

    async def _execute_workflow(
        self,
        input_dict: dict[str, Any],
        updater: TaskUpdater,
        context_id: str,
        task_id: str,
    ) -> dict[str, Any]:
        """Execute the main workflow with sub-agents.

        Args:
            input_dict: Input data
            updater: Task status updater
            context_id: Context ID
            task_id: Task ID

        Returns:
            dict: Execution result
        """
        try:
            user_query = self._extract_user_query(input_dict)
            logger.info('[WORKFLOW] Starting workflow execution')

            # Store updater for this task (상태 조회 시 최소 정보 제공용)
            self.task_managers[task_id] = updater

            # Step 0: Planner 시작 알림
            await self._emit_progress_update(
                updater,
                text='[PLANNER] 계획 수립을 시작합니다',
                data={'agent': 'planner', 'phase': 'start'},
            )

            # Step 1: 항상 Planner를 먼저 호출
            logger.info('[WORKFLOW] Step 1: Calling Planner Agent')
            planner_result = await self._call_agent(
                'planner',
                user_query,
                context_id,
            )

            if 'error' in planner_result:
                return {
                    'status': 'failed',
                    'text_content': f'Planner 실행 실패: {planner_result["error"]}',
                    'data_content': None,
                    'final': True,
                    'error_message': planner_result['error'],
                }

            # Step 2: Planner 결과에서 실행할 에이전트 목록 추출
            logger.info('[WORKFLOW] Step 2: Parsing planner result')
            agents_to_execute = self._parse_planner_result(planner_result)
            logger.info(f'[WORKFLOW] Agents to execute: {agents_to_execute}')

            # Step 3: 추출된 에이전트 목록 중간 업데이트
            await self._emit_progress_update(
                updater,
                text=f'[SUPERVISOR] 실행 예정 에이전트: {", ".join(agents_to_execute) if agents_to_execute else "(없음)"}',
                data={'agents_to_execute': agents_to_execute},
            )

            # Step 3.1: Planner 단계 수 중간 업데이트 (plan이 비어있으면 에이전트 수로 대체)
            try:
                plan_steps_count = 0

                # 1) data_content에서 plan 길이 우선 추출
                dc = planner_result.get('data_content')
                if isinstance(dc, dict):
                    res = dc.get('result') if isinstance(dc.get('result'), dict) else None
                    if res and isinstance(res.get('plan'), list):
                        plan_steps_count = len(res['plan'])

                # 2) data_parts에서도 보조 추출
                if plan_steps_count == 0 and isinstance(planner_result.get('data_parts'), list):
                    for part in planner_result['data_parts']:
                        if isinstance(part, dict):
                            result_obj = part.get('result') if isinstance(part.get('result'), dict) else None
                            if result_obj and isinstance(result_obj.get('plan'), list):
                                plan_steps_count = max(plan_steps_count, len(result_obj['plan']))

                # 3) 그래도 0이면, 실행 예정 에이전트 수로 대체
                if plan_steps_count == 0 and agents_to_execute:
                    plan_steps_count = len(agents_to_execute)

                # Planner 요약 텍스트 추출
                planner_text = planner_result.get('text_content') or ''
                planner_text = f"\n{planner_text}" if planner_text else ''

                await self._emit_progress_update(
                    updater,
                    text=f'[PLANNER] 계획 생성 완료 - 총 {plan_steps_count}단계{planner_text}',
                    data={
                        'agent': 'planner',
                        'summary': {'plan_steps': plan_steps_count},
                        'raw': {
                            'has_text': bool(planner_result.get('text_content')),
                            'data_parts_len': len(planner_result.get('data_parts') or []),
                            'has_data_content': bool(planner_result.get('data_content')),
                        },
                    },
                )
            except Exception:
                await self._emit_progress_update(
                    updater,
                    text='[PLANNER] 계획 생성 완료',
                    data={'agent': 'planner'},
                )

            # Step 4: 추출된 에이전트들을 순차적으로 실행
            # NOTE: 여기를 병렬 처리로 돌릴 순 없을지? 각 에이전트의 최종 결과값만 취합하면 되는데...
            all_results = {'planner': planner_result}
            previous_result = planner_result

            for i, agent_type in enumerate(agents_to_execute, 1):
                logger.info(f'[WORKFLOW] Step 3.{i}: Executing {agent_type} agent')

                # 이전 결과를 포함한 입력 준비
                agent_input = self._prepare_agent_context(
                    user_query,
                    agent_type,
                    previous_result,
                )

                # 에이전트 시작 알림
                with suppress(Exception):
                    await self._emit_progress_update(
                        updater,
                        text=f'[{agent_type.upper()}] 에이전트 실행 시작',
                        data={'agent': agent_type, 'phase': 'start'},
                    )

                # 에이전트 호출
                agent_result = await self._call_agent(
                    agent_type,
                    agent_input,
                    context_id,
                )

                all_results[agent_type] = agent_result
                previous_result = agent_result

                # 에러 체크
                if 'error' in agent_result:
                    # 에러가 발생해도 일단 계속 진행하도록
                    logger.warning(f'[WORKFLOW] {agent_type} agent failed: {agent_result["error"]}')

                # 중간 업데이트 전송 (각 에이전트 실행 완료 후) - 본문 포함
                try:
                    display_body = agent_result.get('text_content') or ''
                    if not display_body:
                        # 텍스트가 없으면 data_content → data_parts의 마지막 파트를 문자열로
                        data_preview_obj = agent_result.get('data_content')
                        if data_preview_obj is None:
                            parts = agent_result.get('data_parts') or []
                            if isinstance(parts, list) and parts:
                                data_preview_obj = parts[-1]
                        if data_preview_obj is not None:
                            try:
                                display_body = json.dumps(data_preview_obj, ensure_ascii=False)
                            except Exception:
                                display_body = ''

                    header = f'[{agent_type.upper()}] 에이전트 실행 완료'
                    text_out = f'{header}\n{display_body}' if display_body else header

                    await self._emit_progress_update(
                        updater,
                        text=text_out,
                        data={
                            'agent': agent_type,
                            'data_parts_len': len(agent_result.get('data_parts') or []),
                            'has_data_content': bool(agent_result.get('data_content')),
                            'error': agent_result.get('error'),
                        },
                    )
                except Exception:
                    pass

            # Step 5: 모든 결과 통합
            logger.info('[WORKFLOW] Step 4: Merging all results')
            return self._merge_results(all_results)

        except Exception as e:
            logger.error(f'Workflow execution failed: {e}')
            return {
                'status': 'failed',
                'text_content': f'워크플로우 실행 중 오류 발생: {e!s}',
                'data_content': None,
                'final': True,
                'error_message': str(e),
            }

    def _parse_planner_result(self, planner_result: dict) -> list[str]:
        """Parse planner result to extract agents to execute.

        Args:
            planner_result: Result from planner agent

        Returns:
            list[str]: List of agent types to execute
        """
        agents_to_call = []

        # data_content에서 우선 추출 (표준 플래너 출력)
        dc = planner_result.get('data_content')
        if isinstance(dc, dict):
            result = dc.get('result') if isinstance(dc.get('result'), dict) else None
            if result:
                # agent_assignments 우선
                assignments = result.get('agent_assignments')
                if isinstance(assignments, dict):
                    agents_to_call.extend(assignments.values())

                # plan 배열에서 에이전트 추출
                plan = result.get('plan')
                if isinstance(plan, list):
                    for step in plan:
                        if isinstance(step, dict):
                            if 'agent' in step:
                                agents_to_call.append(step['agent'])
                            elif 'agent_to_use' in step:
                                agents_to_call.append(step['agent_to_use'])

        # data_parts에서 보조 추출
        if 'data_parts' in planner_result and isinstance(planner_result['data_parts'], list):
            for part in planner_result['data_parts']:
                if isinstance(part, dict):
                    # agent_assignments 확인
                    if 'agent_assignments' in part:
                        assignments = part['agent_assignments']
                        if isinstance(assignments, dict):
                            agents_to_call.extend(assignments.values())

                    # result 내부의 plan 확인
                    if 'result' in part and isinstance(part['result'], dict):
                        result = part['result']

                        # agent_assignments in result
                        if 'agent_assignments' in result:
                            assignments = result['agent_assignments']
                            if isinstance(assignments, dict):
                                agents_to_call.extend(assignments.values())

                        # plan에서 agent 정보 추출
                        if 'plan' in result and isinstance(result['plan'], list):
                            for step in result['plan']:
                                if isinstance(step, dict):
                                    if 'agent' in step:
                                        agents_to_call.append(step['agent'])
                                    elif 'agent_to_use' in step:
                                        agents_to_call.append(step['agent_to_use'])

        # text_content에서 키워드 기반 추출 (fallback)
        if not agents_to_call and 'text_content' in planner_result:
            text = planner_result['text_content'].lower()

            # 키워드 매핑
            keyword_agent_map = [
                (['메모리', 'memory', '기억', '저장된 정보'], 'knowledge'),
                (['브라우저', 'browser', '웹', '검색', 'search'], 'browser'),
                (['실행', 'execute', '코드', 'code', '노션', 'notion'], 'executor'),
            ]

            for keywords, agent_type in keyword_agent_map:
                if any(kw in text for kw in keywords):
                    agents_to_call.append(agent_type)

        # 중복 제거 및 순서 유지
        seen = set()
        unique_agents = []
        for agent in agents_to_call:
            if agent not in seen and agent != 'planner':  # planner는 이미 실행했으므로 제외
                seen.add(agent)
                unique_agents.append(agent)

        # 에이전트가 없으면 기본값으로 knowledge 추가
        if not unique_agents:
            logger.info('[WORKFLOW] No agents found in plan, defaulting to knowledge agent')
            unique_agents = ['knowledge']

        return unique_agents

    def _prepare_agent_context(self, original_query: str, agent_type: str, previous_result: dict) -> str:
        """Prepare input context for each agent.

        Args:
            original_query: Original user query
            agent_type: Type of agent to call
            previous_result: Result from previous agent

        Returns:
            str: Prepared input for the agent
        """
        # 이전 결과에서 텍스트 추출
        prev_text = previous_result.get('text_content', '')

        # 에이전트별 맞춤 컨텍스트 생성
        if agent_type == 'knowledge':
            return f"""
원본 요청: {original_query}

계획:
{prev_text}

위 계획에 따라 필요한 정보를 검색하고 제공해주세요.
"""

        if agent_type == 'browser':
            return f"""
검색 요청: {original_query}

이전 단계 정보:
{prev_text}

위 내용을 참고하여 웹에서 필요한 정보를 검색해주세요.
"""

        if agent_type == 'executor':
            return f"""
실행 요청: {original_query}

컨텍스트:
{prev_text}

위 정보를 바탕으로 요청된 작업을 실행해주세요.
"""

        # 기본값
        return original_query

    def _merge_results(self, all_results: dict[str, dict]) -> dict[str, Any]:
        """Merge all agent results into final response.

        Args:
            all_results: Dictionary of all agent results

        Returns:
            dict: Merged final result
        """
        # 텍스트 내용 병합 (텍스트 없으면 데이터 미리보기로 대체)
        merged_text_parts = []
        for agent_name, result in all_results.items():
            text = result.get('text_content') or ''
            if not text:
                # data_content 우선 미리보기
                data_preview_obj = result.get('data_content')
                if not data_preview_obj:
                    # data_parts가 있으면 마지막 파트 사용
                    parts = result.get('data_parts') or []
                    if isinstance(parts, list) and parts:
                        data_preview_obj = parts[-1]
                if data_preview_obj is not None:
                    try:
                        preview = json.dumps(data_preview_obj, ensure_ascii=False)
                        text = preview
                    except Exception:
                        text = ''

            if text:
                merged_text_parts.append(f"[{agent_name.upper()}]\n{text}")

        # 데이터 내용 수집
        agent_data = {}
        for agent_name, result in all_results.items():
            if 'data_content' in result or 'data_parts' in result:
                agent_data[agent_name] = {
                    'data_content': result.get('data_content'),
                    'data_parts': result.get('data_parts'),
                }

        # 최종 응답 구성
        final_text = '\n\n'.join(merged_text_parts) if merged_text_parts else '워크플로우가 완료되었습니다.'

        return {
            'status': 'completed',
            'text_content': final_text,
            'data_content': {
                'workflow_summary': {
                    'agents_executed': list(all_results.keys()),
                    'total_agents': len(all_results),
                },
                'agent_results': agent_data,
            },
            'final': True,
        }

    def _determine_workflow_type(self, query: str) -> str:
        """Determine the workflow type based on the query.

        Args:
            query: User query

        Returns:
            str: Workflow type
        """
        # Simple keyword-based classification
        if any(
            keyword in query.lower()
            for keyword in ['계획', 'plan', '단계', '분해']
        ):
            return 'planning'
        if any(
            keyword in query.lower() for keyword in ['기억', '저장', '메모']
        ):
            return 'memory'
        if any(
            keyword in query.lower() for keyword in ['웹', '브라우저', '사이트']
        ):
            return 'browser'
        if any(
            keyword in query.lower() for keyword in ['코드', '실행', '문서']
        ):
            return 'executor'
        return 'planning'  # Default


def main() -> None:
    """SupervisorAgent A2A 서버 실행."""
    # 로깅 설정
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    supervisor_executor = CustomSupervisorAgentA2A()

    try:
        is_docker = os.getenv('IS_DOCKER', 'false').lower() == 'true'
        host = os.getenv(
            'AGENT_HOST', 'localhost' if not is_docker else '0.0.0.0'
        )
        port = int(os.getenv('AGENT_PORT', '8000'))
        url = f'http://{host}:{port}'

        handler = build_request_handler(supervisor_executor)
        server_app = build_a2a_starlette_application(
            agent_card=supervisor_executor.get_agent_card(url),
            handler=handler,
        )

        # NOTE: Supervisor 는 외부에서 요청을 받아야하기 때문에 CORS 설정이 필요함.
        app = create_cors_enabled_app(server_app)

        logger.info(
            f'SupervisorAgent A2A server starting at {url} with CORS enabled'
        )

        config = uvicorn.Config(
            app,
            host=host,
            port=port,
            log_level='info',
            access_log=False,
            reload=False,
            timeout_keep_alive=1000,
            timeout_notify=1000,
            ws_ping_interval=30,
            ws_ping_timeout=60,
            limit_max_requests=None,
            timeout_graceful_shutdown=10,
            loop="uvloop"
        )
        server = uvicorn.Server(config)
        server.run()

    except Exception as e:
        logger.error(f'Server start failed: {e}', exc_info=True)
        raise
