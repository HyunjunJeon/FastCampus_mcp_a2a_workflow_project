from typing import Any, ClassVar, Never, get_type_hints

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import (
    MultiServerMCPClient,
)
from langchain_mcp_adapters.sessions import (
    StreamableHttpConnection,
)
from langgraph.cache.base import BaseCache
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.store.base import BaseStore
from langgraph.types import RetryPolicy

from src.base.error_handling import AgentExecutionError


class BaseGraphAgent:
    """LangGraph 기반 에이전트의 추상 기본 클래스.

    모든 LangGraph 에이전트가 상속받아야 하는 핵심 기능을 제공합니다.
    Sub-Graph와 Main-Graph를 객체지향적으로 구성할 수 있도록 공통 기능을 제공합니다.

    주요 기능:
    - StateGraph 구축 및 컴파일
    - 노드/엣지 초기화 추상 메서드
    - 상태 검증 및 스키마 관리
    - 에러 처리 및 복구 전략
    - Human-in-the-Loop 인터럽트 시스템 통합

    생명주기:
    1. __init__: 에이전트 초기화 및 설정
    2. build_graph: StateGraph 구축 및 컴파일
    3. init_nodes/init_edges: 서브클래스에서 구현
    4. 실행: 컴파일된 그래프를 통한 워크플로우 실행
    """

    # 노드 이름을 클래스 속성으로 정의하여 문자열 오타를 방지
    NODE_NAMES: ClassVar[dict[str, str]] = {
        'DEFAULT': 'default',
    }

    def __init__(
        self,
        model: BaseChatModel | None = None,
        state_schema: type | None = None,
        config_schema: type | None = None,
        input_state: type | None = None,
        output_state: type | None = None,
        checkpointer: BaseCheckpointSaver | None = None,
        store: BaseStore | None = None,
        cache: BaseCache | None = None,
        tools: list[BaseTool] | None = None,
        mcp_servers: list[dict[str, Any]] | None = None,
        **kwargs
    ) -> None:
        """BaseGraphAgent 초기화 메서드.

        LangGraph 에이전트의 핵심 구성 요소를 설정하고 초기화합니다.
        상태 관리, 체크포인팅, 인터럽트 시스템 등을 설정합니다.

        Args:
            model: LLM 모델 인스턴스 (OpenAI, Anthropic 등)
            state_schema: TypedDict로 정의된 상태 스키마 타입
            config_schema: 설정 스키마 타입 (선택적)
            input_state: 에이전트 입력 상태 타입 (선택적)
            output_state: 에이전트 출력 상태 타입 (선택적)
            checkpointer: 단기 메모리를 위한 체크포인터
            store: 장기 메모리를 위한 스토어 객체
            cache: 캐시 객체
            max_retry_attempts: 실패 시 최대 재시도 횟수 (default: 2)
            agent_name: 에이전트 식별 이름 (로깅/디버깅용)
            is_debug: 디버그 모드 활성화 여부 (default: True)

        Raises:
            ValueError: 필수 매개변수가 잘못된 경우

        """
        self.model = model
        self.checkpointer = checkpointer
        self.store = store
        self.tools = tools or []
        self.mcp_servers = mcp_servers
        self.cache = cache
        self.state_schema = state_schema
        self.config_schema = config_schema
        self.input_state = input_state
        self.output_state = output_state

        # kwargs에서 추가 설정값 추출
        self.max_retry_attempts = kwargs.get('max_retry_attempts', 2)
        self.agent_name = kwargs.get('agent_name')
        self.is_debug = kwargs.get('is_debug', True)
        self.lazy_init = kwargs.get('lazy_init', False)

        _retry_policy = (
            RetryPolicy(
                max_attempts=self.max_retry_attempts,
            )
            if self.max_retry_attempts > 0
            else None
        )
        self.retry_policy = _retry_policy
        if not self.lazy_init:
            self.graph = self.build_graph()

    async def mcp_tools_init(self) -> list[BaseTool] | None:
        """MCP 서버를 초기화하는 메서드."""
        connections = {}
        for server in self.mcp_servers:
            # TODO: [Performance] Connection pooling 구현 필요 - 현재 각 서버마다 새 연결 생성
            connections[server['name']] = StreamableHttpConnection(
                url=server['url']
            )

        # MCP 클라이언트 생성
        # TODO: [Error Handling] MCP 서버 연결 실패 시 retry 로직 구현 필요
        self.mcp_client = MultiServerMCPClient(connections=connections)
        __mcp_tools: list[BaseTool] = await self.mcp_client.get_tools()
        return self._merge_tools(__mcp_tools)

    async def initialize(self) -> None:
        """비동기 초기화 메서드."""
        # MCP tools 초기화
        if self.mcp_servers:
            mcp_tools = await self.mcp_tools_init()
            self.tools = mcp_tools

        # Lazy init인 경우 그래프 빌드
        if self.lazy_init and self._graph is None:
            self._graph = self.build_graph()
            self.graph = self._graph

        return self

    @classmethod
    async def create(cls, **kwargs) -> "BaseGraphAgent":
        """비동기 팩토리 메서드."""
        instance = cls(**kwargs, lazy_init=True)
        await instance.initialize()
        return instance

    @property
    def graph(self) -> CompiledStateGraph | None:
        """그래프 접근자."""
        if self.lazy_init and self._graph is None:
            raise RuntimeError(
                'Agent not initialized. Call await agent.initialize() first.'
            )
        return self._graph if self.lazy_init else self._internal_graph

    @graph.setter
    def graph(self, value: CompiledStateGraph | None) -> None:
        if self.lazy_init:
            self._graph = value
        else:
            self._internal_graph = value

    def get_node_name(self, key: str = '') -> str:
        """노드 이름을 안전하게 가져오는 헬퍼 메서드.

        NODE_NAMES 딕셔너리에서 키에 해당하는 노드 이름을 반환합니다.
        문자열 하드코딩 대신 상수를 사용하여 오타를 방지합니다.

        Args:
            key: 노드 이름 키 (default: "DEFAULT")

        Returns:
            str: 해당 키에 대한 노드 이름

        Raises:
            ValueError: 키가 NODE_NAMES에 정의되지 않은 경우
        """
        if key not in self.NODE_NAMES:
            raise ValueError(f"노드 이름 키 '{key}'가 정의되어 있지 않습니다.")
        return self.NODE_NAMES.get(key)

    def init_nodes(self, graph: StateGraph) -> Never:
        """그래프에 노드를 등록하는 추상 메서드.

        서브클래스에서 반드시 구현해야 하며, graph.add_node()를 사용하여
        워크플로우의 각 단계를 노드로 등록합니다.

        Args:
            graph: 노드를 추가할 StateGraph 객체

        Example:
            ```python
            def init_nodes(self, graph):
                graph.add_node('process', self.process_data)
                graph.add_node('analyze', self.analyze_data)
            ```

        Raises:
            NotImplementedError: 서브클래스에서 구현하지 않은 경우
        """
        raise NotImplementedError('Subclasses must implement init_nodes method')

    def init_edges(self, graph: StateGraph) -> Never:
        """그래프의 노드 간 연결을 정의하는 추상 메서드.

        서브클래스에서 반드시 구현해야 하며, graph.add_edge()와
        graph.add_conditional_edges()를 사용하여 워크플로우를 정의합니다.

        Args:
            graph: 엣지를 추가할 StateGraph 객체

        Example:
            ```python
            def init_edges(self, graph):
                graph.add_edge(START, 'process')
                graph.add_conditional_edges(
                    'process',
                    self.should_continue,
                    {'continue': 'analyze', 'end': END},
                )
            ```

        Raises:
            NotImplementedError: 서브클래스에서 구현하지 않은 경우
        """
        raise NotImplementedError('Subclasses must implement init_edges method')

    def build_graph(self) -> CompiledStateGraph:
        """StateGraph를 구축하고 컴파일하는 메서드.

        Raises:
            NotImplementedError: init_nodes/init_edges가 구현되지 않은 경우
        """
        _graph = StateGraph(
            state_schema=self.state_schema,
            context_schema=self.config_schema,
            input_schema=self.input_state,
            output_schema=self.output_state,
        )

        self.init_nodes(_graph)
        self.init_edges(_graph)

        return _graph.compile(
            checkpointer=self.checkpointer,
            store=self.store,
            cache=self.cache,
            debug=self.is_debug,
            name=f'{self.agent_name or self.__class__.__name__}',
        )

    def get_input_schema(self, config: RunnableConfig | None = None) -> dict:
        """Agent의 입력 스키마를 반환합니다.

        Returns:
            입력 상태 TypedDict 타입 또는 None
        """
        try:
            schema = self.graph.get_input_schema(config)
            # Check if it's a Pydantic model class
            if hasattr(schema, '__pydantic_model__'):
                return schema.__pydantic_model__.model_json_schema()
            # Check if it's a Pydantic model instance
            if hasattr(schema, 'model_dump'):
                # Try to instantiate if it's a class
                if isinstance(schema, type):
                    return schema.model_json_schema()
                return schema.model_dump()
            if hasattr(schema, 'schema'):
                return schema.schema()
            return {'properties': {}, 'required': []}
        except Exception:
            return {'properties': {}, 'required': []}

    def get_output_schema(self, config: RunnableConfig | None = None) -> dict:
        """Agent의 출력 스키마를 반환합니다.

        Returns:
            출력 상태 TypedDict 타입 또는 None
        """
        try:
            schema = self.graph.get_output_schema(config)
            # Check if it's a Pydantic model class
            if hasattr(schema, '__pydantic_model__'):
                return schema.__pydantic_model__.model_json_schema()
            # Check if it's a Pydantic model instance
            if hasattr(schema, 'model_dump'):
                # Try to instantiate if it's a class
                if isinstance(schema, type):
                    return schema.model_json_schema()
                return schema.model_dump()
            if hasattr(schema, 'schema'):
                return schema.schema()
            return {'properties': {}, 'required': []}
        except Exception:
            return {'properties': {}, 'required': []}

    def get_required_fields(self) -> dict[str, list[str]]:
        """Agent의 필수/선택 필드를 반환합니다.

        서브클래스에서 오버라이드하여 구현합니다.

        Returns:
            {"required": [...], "optional": [...]} 형태의 딕셔너리
        """
        raise NotImplementedError(
            'Subclasses must implement get_required_fields method'
        )

    def validate_input(self, data: dict) -> tuple[bool, str]:
        """입력 데이터의 유효성을 검증합니다.

        Args:
            data: 검증할 입력 데이터

        Returns:
            (is_valid, error_message) 튜플

        """
        try:
            # 입력 스키마 가져오기
            input_schema = self.get_input_schema()
            if not input_schema:
                return True, 'No schema defined'

            # TypedDict의 필수 필드 확인
            if hasattr(input_schema, '__required_keys__'):
                required_keys = input_schema.__required_keys__
                missing_keys = required_keys - data.keys()
                if missing_keys:
                    return (
                        False,
                        f'Missing required fields: {", ".join(missing_keys)}',
                    )

            # 타입 힌트 검증
            type_hints = get_type_hints(input_schema)
            for field, expected_type in type_hints.items():
                if field in data:
                    value = data[field]
                    # None 값 허용 여부 확인
                    if value is None:
                        if not (
                            hasattr(expected_type, '__origin__')
                            and type(None) in expected_type.__args__
                        ):
                            return False, f"Field '{field}' cannot be None"
                    # 기본 타입 검증
                    elif not self._check_type(value, expected_type):
                        return False, f"Field '{field}' type mismatch"

            return True, 'Valid'

        except Exception as e:
            return False, f'Validation error: {e!s}'

    def validate_output(self, data: dict) -> tuple[bool, str]:
        """출력 데이터의 유효성을 검증합니다.

        Args:
            data: 검증할 출력 데이터

        Returns:
            (is_valid, error_message) 튜플
        """
        try:
            output_schema = self.get_output_schema()
            if not output_schema:
                return True, 'No schema defined'

            # 출력 스키마 검증 로직
            if hasattr(output_schema, '__required_keys__'):
                required_keys = output_schema.__required_keys__
                missing_keys = required_keys - data.keys()
                if missing_keys:
                    return (
                        False,
                        f'Missing required output fields: {", ".join(missing_keys)}',
                    )

            return True, 'Valid'

        except Exception as e:
            return False, f'Output validation error: {e!s}'

    def _check_type(self, value: Any, expected_type: type) -> bool:
        """타입 체크 헬퍼 메서드.

        Args:
            value: 검증할 값
            expected_type: 예상 타입

        Returns:
            타입 일치 여부
        """
        # Union 타입 처리
        if hasattr(expected_type, '__origin__'):
            origin = expected_type.__origin__
            origin_checks = {
                list: lambda v: isinstance(v, list),
                dict: lambda v: isinstance(v, dict),
                tuple: lambda v: isinstance(v, tuple),
                type(None): lambda v: v is None,
            }

            check_func = origin_checks.get(origin)
            if check_func:
                return check_func(value)

        # 기본 타입 체크
        if expected_type in (str, int, float, bool):
            return isinstance(value, expected_type)

        # TypedDict는 dict로 처리하거나 복잡한 타입은 통과
        return isinstance(value, dict) or True

    def handle_agent_error(
        self, error: Exception, error_context: dict | None = None
    ) -> None:
        """에이전트 실행 중 발생한 에러를 통합 처리합니다.

        에러 정보를 표준화하여 AgentExecutionError로 래핑하고,
        컨텍스트 정보를 추가하여 디버깅을 용이하게 합니다.

        Args:
            error: 발생한 예외 객체
            error_context: 추가 컨텍스트 정보 (노드 이름, 상태 등)

        Raises:
            AgentExecutionError: 에러 정보가 포함된 통합 예외

        Note:
            원본 예외는 original_error 속성으로 접근 가능
        """
        agent_name = self.agent_name or self.__class__.__name__

        if error_context is None:
            error_context = {}

        error_context.update(
            {
                'agent_name': agent_name,
                'error_type': type(error).__name__,
                'error_message': str(error),
            }
        )

        # 에러 재발생 (호출하는 쪽에서 처리)
        raise AgentExecutionError(
            f'{agent_name}: 실행 중 오류 발생 - {error!s}',
            agent_name=agent_name,
            original_error=error,
        ) from error

    def _merge_tools(self, new_tools: list[BaseTool]) -> list[BaseTool]:
        """Tool 중복 제거."""
        if not self.tools:
            return new_tools

        existing_names = {tool.name for tool in self.tools}
        unique_tools = []

        for tool in new_tools:
            if tool.name not in existing_names:
                unique_tools.append(tool)
                existing_names.add(tool.name)

        self.tools.extend(unique_tools)
        return self.tools
