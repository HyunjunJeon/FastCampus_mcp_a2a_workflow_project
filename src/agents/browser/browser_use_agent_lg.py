"""LangGraph 기반 브라우저 에이전트.

이 모듈은 create_react_agent를 사용하여 브라우저 자동화 에이전트를 구현하며,
Playwright MCP 도구를 활용해 웹 기반 작업을 수행한다.
"""

import os

from datetime import datetime
from typing import Any
from uuid import uuid4

import pytz
import structlog

from langchain_core.messages import AIMessage, HumanMessage, filter_messages
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent

from src.agents.prompts import get_prompt
from src.base.util import load_env_file
from src.mcp_config_module.health_checker import MCPHealthChecker
from src.mcp_config_module.mcp_config import (
    MCPServerConfig,
    create_mcp_client_and_tools,
)


logger = structlog.get_logger(__name__)

load_env_file()


async def create_browser_agent(
    model: ChatOpenAI | None = None,
    is_debug: bool = False,
    checkpointer: InMemorySaver | None = None,
) -> CompiledStateGraph:
    """create_react_agent를 통한 브라우저 자동화 에이전트.

    Playwright MCP 도구들을 로딩하고 프롬프트를 설정한 후 create_react_agent를 생성합니다.

    Args:
        model: LLM 모델 (기본값: gpt-4o-mini)
        is_debug: 디버그 모드 여부
        checkpointer: 체크포인터 (기본값: MemorySaver)

    Returns:
        create_react_agent로 생성된 LangGraph Agent

    Usage:
        agent = await create_browser_agent()
        result = await agent.ainvoke({"messages": [...]})
    """
    try:
        # MCP 서비스 헬스체크
        is_docker = os.getenv('IS_DOCKER', 'false').lower() == 'true'
        services_ready = await MCPHealthChecker.ensure_services_ready(
            'browser', is_docker=is_docker, timeout=30
        )

        if not services_ready:
            logger.warning('MCP services not ready, using fallback')
            tools = []
        else:
            # MCP 도구 로딩
            try:
                server_configs = MCPServerConfig.get_agent_server_configs('browser')
                _, tools = await create_mcp_client_and_tools(
                    server_configs
                )
                logger.info(f'Loaded {len(tools)} MCP tools for Browser Agent')
            except Exception as e:
                logger.warning(f'MCP server not available: {e}')
                logger.info('Using empty tools list for testing')
                tools = []  # Fallback to empty tools

        # 시스템 프롬프트 설정
        system_prompt = get_prompt('browser', 'system', tool_count=len(tools))

        model = model or ChatOpenAI(
            model='gpt-4.1-mini',
            temperature=0.2,
        )

        checkpointer = checkpointer or InMemorySaver()

        agent = create_react_agent(
            model=model,
            tools=tools,
            prompt=system_prompt,
            checkpointer=checkpointer,
            name='BrowserAgent',
            debug=is_debug,
            version='v1',  # Parallel tool calls = False
        )

        logger.info('Browser Agent created successfully with create_react_agent')
        return agent
    except Exception as e:
        logger.error(f'Failed to create Browser Agent: {e}')
        raise RuntimeError(f'Browser Agent creation failed: {e}') from e


async def browse_web(
    agent: CompiledStateGraph,
    url: str | None = None,
    task: str | None = None,
    action_type: str | None = None,
    context_id: str | None = None,
) -> dict[str, Any]:
    """웹 브라우징 작업 실행 헬퍼 함수.

    create_react_agent로 생성된 agent를 사용하여 웹 작업을 수행합니다.

    Args:
        agent: create_browser_agent()로 생성된 에이전트
        url: 접속할 URL
        task: 수행할 작업 설명
        action_type: 작업 유형 (navigate, click, type, extract 등)
        context_id: 컨텍스트 ID (선택적)

    Returns:
        브라우징 작업 결과 딕셔너리
    """
    try:
        # prompts.py에서 프롬프트 가져오기
        user_prompt = get_prompt(
            'browser', 'user', action_type=action_type, url=url, task=task
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

        # create_react_agent가 수행한 도구 호출 횟수 계산
        tool_calls_made = sum(
            len(msg.tool_calls)
            if hasattr(msg, 'tool_calls') and msg.tool_calls
            else 0
            for msg in ai_messages
        )

        logger.info('create_react_agent 기반 브라우저 작업 완료')
        logger.info(f'작업 유형: {action_type or "general"}')
        logger.info(f'URL: {url or "N/A"}')
        logger.info(f'도구 호출 횟수: {tool_calls_made}')
        logger.info(f'총 메시지 수: {len(messages_list)}')

        # 실행 결과 Dictionary 반환
        return {
            'success': True,
            'result': {
                'data': final_message.content,
                'url': url,
                'action_type': action_type,
                'tool_calls_made': tool_calls_made,
                'total_messages_count': len(messages_list),
                'timestamp': datetime.now(
                    tz=pytz.timezone('Asia/Seoul')
                ).isoformat(),
            },
            'agent_type': 'BrowserLangGraphAgent',
            'workflow_status': 'completed',
            'error': None,
        }

    except Exception as e:
        logger.error(f'create_react_agent 기반 브라우저 작업 실패: {e}')
        return {
            'success': False,
            'result': None,
            'error': str(e),
            'agent_type': 'BrowserLangGraphAgent',
            'agent_implementation': 'create_react_agent',
            'workflow_status': 'failed',
        }
