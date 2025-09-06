"""LangGraph 기반 작업 실행 에이전트.

이 모듈은 create_react_agent를 사용하여 다양한 MCP 도구(예: Notion)를
활용해 일반 자동화 작업을 수행하는 작업 실행 에이전트를 구현한다.
"""

from datetime import datetime
from typing import Any
from uuid import uuid4

import pytz
import structlog

from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, filter_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent

from src.agents.prompts import get_prompt
from src.base.util import load_env_file
from src.mcp_config_module.mcp_config import (
    MCPServerConfig,
    create_mcp_client_and_tools,
)


logger = structlog.get_logger(__name__)

load_env_file()


async def create_executor_agent(
    model=None,
    is_debug: bool = False,
    checkpointer=None,
) -> CompiledStateGraph:
    """create_react_agent를 통한 작업 실행 에이전트.

    Notion MCP 도구들을 로딩하고 프롬프트를 설정한 후 create_react_agent를 생성합니다.

    Args:
        model: LLM 모델 (기본값: gpt-4o-mini)
        is_debug: 디버그 모드 여부
        checkpointer: 체크포인터 (기본값: MemorySaver)

    Returns:
        create_react_agent로 생성된 LangGraph Agent

    Usage:
        agent = await create_executor_agent()
        result = await agent.ainvoke({"messages": [...]})
    """
    try:
        # MCP 도구 로딩
        try:
            server_configs = MCPServerConfig.get_agent_server_configs(
                'executor'
            )
            _, tools = await create_mcp_client_and_tools(server_configs)
            logger.info(f'Loaded {len(tools)} MCP tools for Executor Agent')
        except Exception as e:
            logger.warning(f'MCP server not available: {e}')
            logger.info('Using empty tools list for testing')
            tools = []  # Fallback to empty tools

        # 시스템 프롬프트 설정
        system_prompt = get_prompt('executor', 'system', tool_count=len(tools))

        model = model or init_chat_model(
            model='gpt-4.1-mini',
            temperature=0.1,
            model_provider='openai',
        )

        checkpointer = checkpointer or MemorySaver()

        agent = create_react_agent(
            model=model,
            tools=tools,
            prompt=system_prompt,
            checkpointer=checkpointer,
            name='ExecutorLangGraphAgent',
            debug=is_debug,
        )

        logger.info('Executor Agent created successfully with create_react_agent')
        return agent
    except Exception as e:
        logger.error(f'Failed to create Executor Agent: {e}')
        raise RuntimeError(f'Executor Agent creation failed: {e}') from e


async def execute_task(
    agent: CompiledStateGraph,
    task_description: str,
    task_type: str | None = None,
    parameters: dict | None = None,
    context_id: str | None = None,
) -> dict[str, Any]:
    """작업 실행 헬퍼 함수.

    create_react_agent로 생성된 agent를 사용하여 작업을 실행합니다.

    Args:
        agent: create_executor_agent()로 생성된 에이전트
        task_description: 실행할 작업 설명
        task_type: 작업 유형 (코드 실행, 파일 작업, API 호출 등)
        parameters: 추가 매개변수
        context_id: 컨텍스트 ID (선택적)

    Returns:
        작업 실행 결과 딕셔너리
    """
    try:
        user_prompt = get_prompt(
            'executor',
            'user',
            task_type=task_type,
            task_description=task_description,
            parameters=parameters,
        )

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

        tool_calls_made = sum(
            len(msg.tool_calls)
            if hasattr(msg, 'tool_calls') and msg.tool_calls
            else 0
            for msg in ai_messages
        )

        logger.info(f'[TaskExecutorAgent] 작업 실행 완료: {task_type or "general"}')
        logger.info(f'[TaskExecutorAgent] 도구 호출 횟수: {tool_calls_made}')
        logger.info(f'[TaskExecutorAgent] 총 메시지 수: {len(messages_list)}')

        # 실행 결과 Dictionary 반환
        return {
            'success': True,
            'result': {
                'output': final_message.content,
                'task_description': task_description,
                'task_type': task_type,
                'tool_calls_made': tool_calls_made,
                'total_messages_count': len(messages_list),
                'timestamp': datetime.now(
                    tz=pytz.timezone('Asia/Seoul')
                ).isoformat(),
            },
            'agent_type': 'ExecutorLangGraphAgent',
            'workflow_status': 'completed',
            'error': None,
        }

    except Exception as e:
        logger.error(f'create_react_agent 기반 작업 실행 실패: {e}')
        return {
            'success': False,
            'result': None,
            'error': str(e),
            'agent_type': 'ExecutorLangGraphAgent',
            'agent_implementation': 'create_react_agent',
            'workflow_status': 'failed',
        }
