"""LangGraph 기반 플래너 에이전트.

이 모듈은 create_react_agent를 사용하여 복잡한 사용자 요청을
구조화되고 실행 가능한 작업으로 분해하는 계획 수립 에이전트를 구현한다.
"""

from datetime import datetime
from typing import Any
from uuid import uuid4

import pytz
import structlog

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, filter_messages
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent

from src.agents.prompts import get_prompt
from src.base.util import load_env_file


logger = structlog.get_logger(__name__)

load_env_file()


async def create_planner_agent(
    model: BaseChatModel | None = None,
    is_debug: bool = False,
    checkpointer: BaseCheckpointSaver | None = None,
) -> CompiledStateGraph:
    """create_react_agent를 통한 계획 수립 에이전트.

    Planner는 도구 없이 순수 프롬프트 기반으로 작업을 분해하고 계획을 수립합니다.

    Args:
        model: LLM 모델 (기본값: gpt-4o-mini)
        is_debug: 디버그 모드 여부
        checkpointer: 체크포인터 (기본값: MemorySaver)

    Returns:
        create_react_agent로 생성된 LangGraph Agent

    Usage:
        agent = await create_planner_agent()
        result = await agent.ainvoke({"messages": [...]})
    """
    try:
        # Planner는 도구 없이 프롬프트만으로 작업
        tools = []

        # 시스템 프롬프트 설정
        system_prompt = get_prompt('planner', 'system', tool_count=0)

        # o3-mini 추론형 모델 사용 (Planner는 복잡한 계획 수립 필요)
        if model is None:

            try:
                # Try o3-mini without temperature (not supported)
                model = ChatOpenAI(
                    model='o3-mini',  # OpenAI 추론형 모델
                )
            except Exception:
                # Fallback to gpt-4.1 for compatibility
                model = ChatOpenAI(
                    model='gpt-4.1',
                    temperature=0,
                )

        checkpointer = checkpointer or InMemorySaver()

        agent = create_react_agent(
            model=model,
            tools=tools,
            prompt=system_prompt,
            checkpointer=checkpointer,
            name='PlannerLangGraphAgent',
            debug=is_debug,
        )

        logger.info(
            '✅ Planner Agent created successfully with create_react_agent'
        )
        return agent
    except Exception as e:
        logger.error(f'Failed to create Planner Agent: {e}')
        raise RuntimeError(f'Planner Agent creation failed: {e}') from e


async def create_task_plan(
    agent: CompiledStateGraph,
    user_request: str,
    context_id: str | None = None,
) -> dict[str, Any]:
    """작업 계획 수립 실행 헬퍼 함수.

    create_react_agent로 생성된 agent를 사용하여 작업 계획을 수립합니다.

    Args:
        agent: create_planner_agent()로 생성된 에이전트
        user_request: 사용자 요청
        context_id: 컨텍스트 ID (선택적)

    Returns:
        작업 계획 딕셔너리
    """
    try:
        # prompts.py에서 프롬프트 가져오기
        user_prompt = get_prompt('planner', 'user', user_request=user_request)

        messages = [HumanMessage(content=user_prompt)]

        result = await agent.ainvoke(
            {'messages': messages},
            config={'configurable': {'thread_id': context_id or str(uuid4())}},
        )

        # Debug: print result structure
        logger.info(f'Debug - result type: {type(result)}')

        # create_react_agent 실행 결과에서 최종 AI 메시지 추출
        if 'messages' not in result:
            logger.error("❌ result에 'messages' 키가 없습니다.")
            messages_list = []
        else:
            messages_list = result['messages']

        ai_messages = filter_messages(
            messages_list,
            include_types=[AIMessage],
        )

        if not ai_messages:
            logger.error('No AI messages found in the result')
            raise ValueError('No AI response generated')

        final_message: AIMessage = ai_messages[-1]

        logger.info('🎯 create_react_agent 기반 계획 수립 완료')
        logger.info(f'   → 총 메시지 수: {len(messages_list)}')

        # 실행 결과 Dictionary 반환
        return {
            'success': True,
            'result': {
                'plan': final_message.content,
                'user_request': user_request,
                'total_messages_count': len(messages_list),
                'timestamp': datetime.now(
                    tz=pytz.timezone('Asia/Seoul')
                ).isoformat(),
            },
            'agent_type': 'PlannerLangGraphAgent',
            'workflow_status': 'completed',
            'error': None,
        }

    except Exception as e:
        logger.error(f'❌ create_react_agent 기반 계획 수립 실패: {e}')
        return {
            'success': False,
            'result': None,
            'error': str(e),
            'agent_type': 'PlannerLangGraphAgent',
            'agent_implementation': 'create_react_agent',
            'workflow_status': 'failed',
        }
