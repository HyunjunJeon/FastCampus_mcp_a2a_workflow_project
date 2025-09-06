"""LangGraph 로 구현된 Supervisor Agent 입니다.

Supervisor Agent는 다양한 Agent를 관리하고 조정하는 역할 + 사용자와 소통하며 최종 결과를 제공하는 역할을 합니다.
"""

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph_supervisor import create_supervisor

from src.agents.browser.browser_use_agent_lg import create_browser_agent
from src.agents.executor.task_executor_agent_lg import create_executor_agent
from src.agents.knowledge.knowledge_agent_lg import create_knowledge_agent
from src.agents.planner.planner_agent_lg import create_planner_agent
from src.agents.prompts import get_prompt


async def create_supervisor_agent_lg(
    model: ChatOpenAI | None = None,
    is_debug: bool = False
) -> CompiledStateGraph:
    """Supervisor Agent를 생성합니다.

    langgraph-supervisor 패키지를 사용하여 여러 에이전트를 관리합니다.
    """
    # 모델 설정
    if model is None:
        model = ChatOpenAI(
            model='gpt-4.1',
            temperature=0.0,
        )

    # 하위 에이전트들 초기화 (async로 await 필요)
    planner_agent = await create_planner_agent(is_debug=is_debug)
    memory_agent = await create_knowledge_agent(is_debug=is_debug)
    browser_agent = await create_browser_agent(is_debug=is_debug)
    executor_agent = await create_executor_agent(is_debug=is_debug)

    return create_supervisor(
        agents=[
            planner_agent,
            memory_agent,
            browser_agent,
            executor_agent,
        ],
        model=model,
        prompt=get_prompt('supervisor', 'system'),
    ).compile(
        checkpointer=InMemorySaver(),
        name='SupervisorLangGraphAgent',
        debug=is_debug,
    )
