"""Browser Agent A2A Wrapper.

This module provides an A2A protocol wrapper for the Browser Agent,
enabling it to work with the A2A communication protocol.
"""

import asyncio
import os

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
from src.agents.browser.browser_use_agent_lg import (
    create_browser_agent,
)
from src.base.a2a_interface import A2AOutput, BaseA2AAgent


logger = structlog.get_logger(__name__)


class BrowserUseA2AAgent(BaseA2AAgent):
    """A2A wrapper for the Browser Agent.

    This class wraps the LangGraph BrowserUseAgent to provide
    A2A protocol compatibility for browser automation operations.
    """

    def __init__(
        self,
        model=None,
        check_pointer=None,
        is_debug: bool = False,
    ) -> None:
        """Initialize the Browser A2A Agent.

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
        self.agent_type = "Browser"
        self.NODE_NAMES = {
            "analyze_task": "analyze_task",
            "plan_actions": "plan_actions",
            "navigate_to_page": "navigate_to_page",
            "interact_with_page": "interact_with_page",
            "extract_data": "extract_data",
            "validate_results": "validate_results",
            "handle_error": "handle_error",
        }

        logger.info("BrowserUseA2AAgent initialized")

    async def initialize(self) -> bool:
        """Initialize the browser agent asynchronously."""
        try:
            if self.graph is None:
                self.graph = await create_browser_agent(
                    model=self.model,
                    is_debug=self.is_debug,
                    checkpointer=self.check_pointer,
                )
                logger.info("Browser agent graph created successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing BrowserUseA2AAgent: {e}")
            return False

    async def execute_for_a2a(
        self,
        input_dict: dict[str, Any],
        config: dict[str, Any] | None = None
    ) -> A2AOutput:
        """Execute the Browser Agent with A2A-compatible input and output.

        Args:
            input_dict: Input data containing messages and browser task
            config: Optional configuration

        Returns:
            A2AOutput: Standardized output for A2A processing
        """
        try:
            logger.info(f"Executing BrowserUseA2AAgent with input: {input_dict}")

            # Ensure agent is initialized
            await self.initialize()

            # Extract user request from input
            messages = input_dict.get("messages", [])
            user_request = ""

            for msg in messages:
                if msg.get("role") == "user":
                    user_request = msg.get("content", "")
                    break

            # Extract browser-specific parameters if provided
            target_url = input_dict.get("target_url")
            extraction_targets = input_dict.get("extraction_targets", [])
            form_data = input_dict.get("form_data", {})

            # Prepare input for LangGraph agent
            lg_input = {
                "messages": [HumanMessage(content=user_request)],
                "user_request": user_request,
                "target_url": target_url,
                "extraction_targets": extraction_targets,
                "form_data": form_data,
                "max_retries": 3,
                "workflow_phase": "initializing",
                "should_continue": True,
                "retry_count": 0,
                "page_loaded": False,
                "current_action_index": 0,
                "planned_actions": [],
                "executed_actions": [],
                "extracted_data": [],
                "screenshots": [],
                "total_execution_time": 0,
            }

            # Add configuration (use provided thread_id or conversation_id)
            if not config:
                config = {}
            config["configurable"] = config.get("configurable", {})
            if "thread_id" not in config["configurable"]:
                conv_id = input_dict.get("conversation_id") or input_dict.get("context_id")
                config["configurable"]["thread_id"] = (
                    conv_id if conv_id else f"browser-{datetime.now(pytz.UTC).isoformat()}"
                )

            # Execute the LangGraph agent
            result = await self.graph.ainvoke(lg_input, config)

            # Extract final output
            return self.extract_final_output(result)

        except Exception as e:
            logger.error(f"Error executing BrowserUseA2AAgent: {e}")
            return self.format_error(e, "Browser operation failed")

    def format_stream_event(
        self,
        event: dict[str, Any]
    ) -> A2AOutput | None:
        """Convert a streaming event to standardized A2A output.

        Args:
            event: Raw streaming event from LangGraph

        Returns:
            A2AOutput if the event should be forwarded, None otherwise
        """
        try:
            event_type = event.get("event", "")

            # Handle LLM streaming
            if event_type == "on_llm_stream":
                content = self.extract_llm_content(event)
                if content:
                    return self.create_a2a_output(
                        status="working",
                        text_content=content,
                        metadata={
                            "event_type": "llm_stream",
                            "timestamp": datetime.now(pytz.UTC).isoformat(),
                        },
                        stream_event=True,
                        final=False,
                    )

            # Handle node execution events
            elif event_type == "on_chain_start":
                node_name = event.get("name", "")
                if node_name in self.NODE_NAMES.values():
                    node_display_name = self._get_node_display_name(node_name)
                    return self.create_a2a_output(
                        status="working",
                        text_content=f"|실행 중 행 중: {node_display_name}",
                        metadata={
                            "event_type": "node_start",
                            "node_name": node_name,
                            "timestamp": datetime.now(pytz.UTC).isoformat(),
                        },
                        stream_event=True,
                        final=False,
                    )

            # Handle tool execution events
            elif event_type == "on_tool_start":
                tool_name = event.get("name", "")
                if "playwright" in tool_name.lower():
                    return self.create_a2a_output(
                        status="working",
                        text_content=f"Playwright �l �: {tool_name}",
                        metadata={
                            "event_type": "tool_start",
                            "tool_name": tool_name,
                            "timestamp": datetime.now(pytz.UTC).isoformat(),
                        },
                        stream_event=True,
                        final=False,
                    )

            # Handle browser action events (custom events from Playwright MCP)
            elif event_type == "browser_action":
                action_type = event.get("action_type", "")
                target = event.get("target", "")
                return self.create_a2a_output(
                    status="working",
                    text_content=f"|실행 중 aX: {action_type} - {target}",
                    data_content={
                        "action_type": action_type,
                        "target": target,
                        "value": event.get("value"),
                    },
                    metadata={
                        "event_type": "browser_action",
                        "timestamp": datetime.now(pytz.UTC).isoformat(),
                    },
                    stream_event=True,
                    final=False,
                )

            # Check for completion
            if self.is_completion_event(event):
                return self.create_a2a_output(
                    status="completed",
                    text_content="|실행 중 행 중t D�ȵ행 중.",
                    metadata={
                        "event_type": "completion",
                        "timestamp": datetime.now(pytz.UTC).isoformat(),
                    },
                    stream_event=True,
                    final=True,
                )

            return None

        except Exception as e:
            logger.error(f"Error formatting stream event: {e}")
            return None

    def extract_final_output(
        self,
        state: dict[str, Any]
    ) -> A2AOutput:
        """Extract final output from the agent's state.

        Args:
            state: Final state from the LangGraph execution

        Returns:
            A2AOutput: Final standardized output
        """
        try:
            workflow_phase = state.get("workflow_phase", "unknown")
            error = state.get("error")

            # Handle error state
            if error or workflow_phase == "failed":
                return self.create_a2a_output(
                    status="failed",
                    text_content=f"|실행 중 행 중 �(: {error}",
                    metadata={
                        "workflow_phase": workflow_phase,
                        "timestamp": datetime.now(pytz.UTC).isoformat(),
                    },
                    final=True,
                    error_message=error,
                )

            # Extract messages for response
            messages = state.get("messages", [])
            response_text = ""

            for msg in reversed(messages):
                if isinstance(msg, AIMessage):
                    response_text = msg.content
                    break

            # Prepare data content with browser operation results
            data_content = {}

            # Include extracted data
            extracted_data = state.get("extracted_data", [])
            if extracted_data:
                data_content["extracted_data"] = extracted_data

            # Include executed actions
            executed_actions = state.get("executed_actions", [])
            if executed_actions:
                data_content["executed_actions"] = [
                    {
                        "action_type": action.get("action_type"),
                        "target": action.get("target"),
                        "success": action.get("success"),
                        "timestamp": action.get("timestamp"),
                    }
                    for action in executed_actions
                ]

            # Include screenshots metadata
            screenshots = state.get("screenshots", [])
            if screenshots:
                data_content["screenshots_count"] = len(screenshots)
                data_content["screenshots"] = screenshots[:5]  # Limit to first 5 for response size

            # Include final URL
            current_url = state.get("current_url")
            if current_url:
                data_content["final_url"] = current_url

            # Include performance metrics
            total_execution_time = state.get("total_execution_time", 0)
            if total_execution_time > 0:
                data_content["execution_time_seconds"] = total_execution_time

            # Determine final status
            task_completed = state.get("task_completed", False)
            status = "completed" if task_completed and workflow_phase == "completed" else "working"

            return self.create_a2a_output(
                status=status,
                text_content=response_text or "|실행 중 행 중t D�ȵ행 중.",
                data_content=data_content if data_content else None,
                metadata={
                    "workflow_phase": workflow_phase,
                    "task_type": state.get("task_type", "unknown"),
                    "task_completed": task_completed,
                    "timestamp": datetime.now(pytz.UTC).isoformat(),
                },
                final=True,
            )

        except Exception as e:
            logger.error(f"Error extracting final output: {e}")
            return self.format_error(e, "Failed to extract browser operation results")

    def _get_node_display_name(self, node_name: str) -> str:
        """Get display-friendly name for a node.

        Args:
            node_name: Internal node name

        Returns:
            str: Display-friendly name
        """
        display_names = {
            "analyze_task": "행 중 �",
            "plan_actions": "aX č",
            "navigate_to_page": "�t� t�",
            "interact_with_page": "�t� �8행 중",
            "extract_data": "pt0 행 중",
            "validate_results": "행 중 행 중",
            "handle_error": "$X 행 중",
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
            url = f"http://browser-agent:{os.getenv('AGENT_PORT', '8000')}"

        skills = [
            create_agent_skill(
                skill_id="browse-web",
                name="웹 브라우징 및 자동화",
                description="웹사이트를 방문하고 데이터를 추출하거나 폼을 작성하는 등의 브라우저 자동화 작업을 수행합니다.",
                tags=["browser", "web", "automation", "scraping", "playwright"],
                examples=[
                    "이 웹사이트에서 가격 정보를 추출해주세요",
                    "로그인 폼을 작성하고 제출해주세요",
                    "페이지 스크린샷을 찍어주세요"
                ],
            ),
            create_agent_skill(
                skill_id="extract-data",
                name="데이터 추출",
                description="웹 페이지에서 구조화된 데이터를 추출합니다.",
                tags=["extraction", "scraping", "data"],
                examples=[
                    "테이블 데이터를 추출해주세요",
                    "상품 리스트를 수집해주세요"
                ],
            ),
        ]

        logger.info("A2A agent card created")

        return create_agent_card(
            name="BrowserAgent",
            description="웹 브라우징 자동화 및 데이터 추출을 위한 Agent입니다.",
            url=url,
            skills=skills,
        )


# Factory function for creating A2A-compatible Browser Agent
async def create_browser_use_a2a_agent(
    model=None,
    is_debug: bool = False,
    check_pointer=None,
) -> BrowserUseA2AAgent:
    """Create and initialize a Browser A2A Agent.

    Args:
        model: LLM model
        is_debug: Debug mode flag
        check_pointer: Checkpoint manager

    Returns:
        BrowserUseA2AAgent: Initialized A2A agent instance
    """
    return BrowserUseA2AAgent(
        model=model,
        check_pointer=check_pointer,
        is_debug=is_debug,
    )


def main() -> None:
    """BrowserAgent A2A 서버 실행.

    이 함수는 서버 실행의 진입점으로, 다음 작업을 수행합니다:
    1. 로깅 설정
    2. 비동기 초기화 실행
    3. 환경 설정 로드
    4. A2A 서버 생성 및 실행
    """

    async def async_init():
        """비동기 초기화 헬퍼 함수.

        MCP 서버와의 비동기 연결이 필요하므로 별도의 비동기 함수로 분리.

        Returns:
            BrowserUseA2AAgent: 초기화된 A2A 래퍼 인스턴스 또는 None
        """
        try:
            # BrowserUseA2AAgent 인스턴스 생성 (디버그 모드 활성화)
            _a2a_wrapper = BrowserUseA2AAgent(is_debug=True)

            # 비동기 초기화 실행 및 결과 확인
            if not await _a2a_wrapper.initialize():
                logger.error("❌ BrowserAgentA2A 초기화 실패")
                return None

            logger.info("✅ BrowserAgentA2A 초기화 완료")
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
        port = int(os.getenv("AGENT_PORT", "8005"))
        url = f"http://{host}:{port}"

        agent_card = a2a_agent.get_agent_card(url)

        # LangGraphAgentExecutor로 래핑
        executor = LangGraphAgentExecutor(
            agent_class=BrowserUseA2AAgent,
            is_debug=True
        )

        # A2A 서버 생성
        handler = build_request_handler(executor)
        server_app = build_a2a_starlette_application(
            agent_card=agent_card,
            handler=handler
        )

        # 서버 시작 정보 로깅
        logger.info(f"✅ BrowserAgent A2A server starting at {url} with CORS enabled")
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
