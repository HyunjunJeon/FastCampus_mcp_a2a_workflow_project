#!/usr/bin/env python3
"""MCP 서버 설정 및 클라이언트 생성 헬퍼.

표준 패턴으로 MCP 도구를 로딩하기 위한 공통 설정과 유틸리티 함수들을 제공합니다.
"""

import os
import traceback

import structlog

from dotenv import load_dotenv
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient


# Load environment variables from .env file
load_dotenv()

logger = structlog.get_logger(__name__)


class MCPServerConfig:
    """MCP 서버 설정 관리 클래스.

    Docker와 로컬 환경에 따라 MCP 서버 설정을 동적으로 관리하며,
    에이전트별로 필요한 서버 그룹을 정의합니다.
    """

    # Docker 환경 감지 - IS_DOCKER 환경변수로 판단
    IS_DOCKER = os.getenv('IS_DOCKER', 'false').lower() == 'true'

    # OpenMemory용 사용자 ID 가져오기
    USER_ID = os.getenv('USER', 'default_user')

    # Notion MCP Bearer 토큰 가져오기 (없으면 기본값 사용)
    NOTION_AUTH_TOKEN = os.getenv('AUTH_TOKEN', 'your-notion-mcp-auth-token-is-here')

    # 실행 환경에 따른 로그 출력
    if IS_DOCKER:
        logger.info(
            'Docker environment detected - using container names for MCP servers'
        )
    else:
        logger.info(
            'Local environment detected - using localhost for MCP servers'
        )

    logger.info(f'Using USER_ID: {USER_ID} for OpenMemory MCP')

    # MCP 서버 설정 - Docker와 로컬 환경에 따라 URL 동적 설정
    STANDARD_MCP_SERVERS = {
        # OpenMemory MCP: 메모리 저장 및 검색 서비스
        'open-memory-mcp': {
            'transport': 'streamable_http',
            'url': f'http://{"openmemory-mcp" if IS_DOCKER else "localhost"}:8031/mcp',
            'headers': {
                'Accept': 'application/json, text/event-stream',
                'Cache-Control': 'no-cache',
            },
        },
        # Playwright MCP: 브라우저 자동화 서비스
        'playwright-mcp': {
            'transport': 'streamable_http',
            # Docker 환경에서는 host.docker.internal 사용 (호스트 접근)
            'url': f'http://{"host.docker.internal" if IS_DOCKER else "localhost"}:8931/mcp',
            'headers': {
                'Accept': 'application/json, text/event-stream',
                'Cache-Control': 'no-cache',
            },
        },
        # Notion MCP: Notion API 통합 서비스
        # 참고: https://github.com/makenotion/notion-mcp-server
        'notion-mcp': {
            'transport': 'streamable_http',
            # Docker와 로컬에서 다른 포트 사용
            'url': f'http://{"notion-mcp" if IS_DOCKER else "localhost"}:{"3000" if IS_DOCKER else "8930"}/mcp',
            'headers': {
                'Authorization': f'Bearer {NOTION_AUTH_TOKEN}',
                'Accept': 'application/json, text/event-stream',
                'Cache-Control': 'no-cache',
            },
        },
        # LangChain Sandbox MCP: WebAssembly 기반 안전한 Python 코드 실행 환경
        'langchain-sandbox': {
            'transport': 'streamable_http',
            'url': f'http://{"langchain-sandbox-mcp" if IS_DOCKER else "localhost"}:8035/mcp',
            'headers': {
                'Accept': 'application/json, text/event-stream',
                'Cache-Control': 'no-cache',
            },
        },
    }

    # 에이전트 타입별 필요한 MCP 서버 그룹 정의
    AGENT_SERVER_GROUPS = {
        # 메모리 관리 에이전트용 서버
        'knowledge': [
            'open-memory-mcp',
        ],
        # 브라우저 자동화 에이전트용 서버
        'browser': [
            'playwright-mcp',
        ],
        # 코드 실행 및 노션 에디터 활용 에이전트용 서버
        'executor': [
            'notion-mcp',  # Notion API 통합 (Bearer 토큰 인증 설정 완료)
            'langchain-sandbox',  # WebAssembly 기반 Python 코드 실행
        ],
    }

    @classmethod
    def get_server_configs(
        cls, server_names: list[str]
    ) -> dict[str, dict[str, str]]:
        """지정된 서버들의 설정을 반환.

        Args:
            server_names: 설정을 가져올 서버 이름 리스트

        Returns:
            서버 이름을 키로 하는 설정 딕셔너리
        """
        configs = {}

        for server_name in server_names:
            if server_name in cls.STANDARD_MCP_SERVERS:
                # 표준 서버 설정에서 가져오기
                configs[server_name] = cls.STANDARD_MCP_SERVERS[server_name]
            else:
                # 알 수 없는 서버 이름인 경우 경고
                logger.warning(f'Unknown MCP server: {server_name}')

        return configs

    @classmethod
    def get_agent_server_configs(
        cls, agent_type: str
    ) -> dict[str, dict[str, str]]:
        """Agent 타입에 따른 서버 설정을 반환.

        Args:
            agent_type: 에이전트 타입 ('knowledge', 'browser', 'executor')

        Returns:
            해당 에이전트에 필요한 서버들의 설정 딕셔너리

        Raises:
            ValueError: 알 수 없는 에이전트 타입인 경우
        """
        if agent_type not in cls.AGENT_SERVER_GROUPS:
            raise ValueError(f'Unknown agent type: {agent_type}')

        # 에이전트 타입에 해당하는 서버 이름들 가져오기
        server_names = cls.AGENT_SERVER_GROUPS[agent_type]
        return cls.get_server_configs(server_names)


async def create_mcp_client_and_tools(
    server_configs: dict[str, dict[str, str]],
) -> tuple[MultiServerMCPClient, list[BaseTool]]:
    """MCP 클라이언트 생성 및 도구 로딩.

    여러 MCP 서버에 연결하고 각 서버가 제공하는 도구들을 로드합니다.
    OpenMemory 도구들은 자동으로 어댑터가 적용됩니다.

    Args:
        server_configs: MCP 서버 설정 딕셔너리

    Returns:
        tuple: (mcp_client, tools) - 클라이언트와 로딩된 도구들

    Example:
        server_configs = MCPServerConfig.get_agent_server_configs("data_collector")
        client, tools = await create_mcp_client_and_tools(server_configs)
    """
    try:
        if not server_configs:
            raise ValueError('No server configs provided')

        logger.info(
            f'Creating MCP client for servers: {list(server_configs.keys())}'
        )

        # 여러 서버를 관리하는 MultiServerMCPClient 생성
        # langchain-mcp-adapters 라이브러리 사용
        mcp_client = MultiServerMCPClient(server_configs)

        # 각 서버로부터 도구 로딩
        # TaskGroup을 사용하여 병렬로 도구를 로드하므로 BaseExceptionGroup 처리 필요
        try:
            tools = await mcp_client.get_tools()
        except BaseExceptionGroup as eg:
            # TaskGroup에서 발생한 모든 예외를 개별적으로 로깅
            logger.error(f'TaskGroup errors: {len(eg.exceptions)} exceptions')
            for i, exc in enumerate(eg.exceptions):
                logger.error(
                    f'  Exception {i + 1}: {type(exc).__name__}: {exc}'
                )
            raise

        logger.info(
            f'Successfully loaded {len(tools)} tools from {len(server_configs)} servers'
        )

        return mcp_client, tools

    except Exception as e:
        logger.error(f'Failed to create MCP client and load tools: {e}')
        # 디버깅을 위한 전체 스택 트레이스 출력
        logger.error(f'Traceback: {traceback.format_exc()}')
        raise


async def load_tools_for_agent(agent_type: str) -> list[BaseTool]:
    """Agent 타입에 맞는 MCP 도구들을 로딩.

    Args:
        agent_type: Agent 타입 ("data_collector", "analysis", "trading")

    Returns:
        list: 로딩된 도구들

    Example:
        tools = await load_tools_for_agent("data_collector")
    """
    try:
        server_configs = MCPServerConfig.get_agent_server_configs(agent_type)
        _, tools = await create_mcp_client_and_tools(server_configs)
        return tools

    except Exception as e:
        logger.error(f'Failed to load tools for agent {agent_type}: {e}')
        raise
