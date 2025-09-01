"""LangGraph 에이전트의 A2A 통합 인터페이스.

이 모듈은 A2A(Agent-to-Agent) 프로토콜과의 통합을 위한 표준
인터페이스와 유틸리티를 제공합니다. 스트리밍과 폴링 방식 모두에서
일관된 데이터 포맷을 유지하도록 설계되었으며, 실행 과정의 중간 이벤트와
최종 결과를 동일한 스키마로 취급할 수 있게 합니다.

주요 목표
- LangGraph 실행 이벤트를 A2A 표준 출력으로 손실 없이 변환
- 스트리밍 토큰과 노드/도구 실행 이벤트의 일관된 처리
- 최종 상태를 A2A 결과로 안전하게 추출

사용 가이드
- 구체 에이전트는 :class:`BaseA2AAgent` 를 상속하여 필수 추상 메서드를
  구현해야 합니다.
- 스트리밍 사용 시 :meth:`format_stream_event` 로 이벤트를 표준 출력으로
  매핑하고, 완료 시 :meth:`extract_final_output` 으로 최종 출력을 생성합니다.
"""

from abc import ABC, abstractmethod
from typing import Any, Literal, TypedDict

import structlog

from a2a.types import AgentCard


logger = structlog.get_logger(__name__)


class A2AOutput(TypedDict):
    """A2A 통합을 위한 표준 출력 형식.

    이 형식은 스트리밍 중간 이벤트와 최종 결과를 하나의 스키마로
    통합하여 A2A 실행기(executor)가 일관되게 처리할 수 있게 합니다.
    에이전트 구현은 본 타입의 사전을 반환해야 하며, 필드의 의미는
    아래 타입 주석과 인라인 주석을 참고하세요.
    """

    agent_type: str
    status: Literal['working', 'completed', 'failed', 'input_required']
    text_content: str | None  # 텍스트 조각(예: LLM 토큰 누적)의 표시용 내용
    data_content: dict[str, Any] | None  # 구조화 데이터(툴 결과, 표 등)
    metadata: dict[str, Any]  # 부가 정보(예: timestamp, node_name, is_final)
    stream_event: bool  # 스트리밍 이벤트면 True, 최종 결과만이면 False
    final: bool  # 이 출력이 마지막 결과임을 표시(스트리밍 종료 신호)
    error_message: str | None  # 상태가 "failed" 일 때 에러 상세 메시지
    requires_approval: bool | None  # Human-in-the-Loop 승인 필요 여부


class BaseA2AAgent(ABC):
    """A2A 통합을 지원하는 추상 클래스.

    모든 구체 에이전트는 이 클래스를 상속하고, A2A 프로토콜 연계를 위한
    표준 인터페이스를 구현해야 합니다. 구현체는 그래프 실행의 스트리밍
    이벤트를 표준 출력으로 변환하고, 실행 완료 시 최종 출력을 추출합니다.
    """

    def __init__(self) -> None:
        """기본 A2A 에이전트를 초기화합니다.

        에이전트 클래스명에서 접미사 ``Agent`` 를 제거해 ``agent_type`` 을
        유도합니다. 로깅을 통해 초기화 사실을 남깁니다.
        """
        self.agent_type = self.__class__.__name__.replace('Agent', '')
        logger.info(f'Initializing A2A agent: {self.agent_type}')

    @abstractmethod
    def get_agent_card(self) -> AgentCard:
        """에이전트의 카드(메타데이터)를 반환합니다.

        Returns:
            AgentCard: 에이전트 식별, 설명, 제공 기능 등 메타 정보
        """
        raise NotImplementedError('get_agent_card method must be implemented')

    @abstractmethod
    async def execute_for_a2a(
        self, input_dict: dict[str, Any], config: dict[str, Any] | None = None
    ) -> A2AOutput:
        """A2A 표준 입출력으로 에이전트를 실행합니다.

        이 메서드는 직접적인 ``graph.ainvoke()`` 호출을 대체하여, A2A
        실행기가 소비할 수 있는 표준 출력(:class:`A2AOutput`)을 생성합니다.

        Args:
            input_dict: 에이전트에 전달할 표준 입력 사전
            config: 실행 구성값(예: ``thread_id``) 또는 ``None``

        Returns:
            A2AOutput: A2A 실행기에 전달 가능한 표준화된 출력
        """
        raise NotImplementedError('execute_for_a2a method must be implemented')

    @abstractmethod
    def format_stream_event(self, event: dict[str, Any]) -> A2AOutput | None:
        """스트리밍 이벤트를 A2A 표준 출력으로 변환합니다.

        다음과 같은 이벤트 유형을 처리하도록 구현합니다.
        - ``on_llm_stream``: LLM 토큰 스트리밍
        - ``on_chain_start/end``: 노드 실행 시작/종료
        - ``on_tool_start/end``: 도구 실행 시작/종료

        Args:
            event: LangGraph가 방출한 원시 스트리밍 이벤트

        Returns:
            A2AOutput | None: 전달할 가치가 있는 이벤트면 표준 출력,
            그렇지 않으면 ``None``
        """
        raise NotImplementedError(
            'format_stream_event method must be implemented'
        )

    @abstractmethod
    def extract_final_output(self, state: dict[str, Any]) -> A2AOutput:
        """에이전트의 최종 상태에서 A2A 최종 출력을 추출합니다.

        에이전트 실행이 완료되었을 때 호출되며, LangGraph의 최종 상태를
        표준 A2A 출력으로 변환합니다.

        Args:
            state: LangGraph 실행이 반환한 최종 상태 사전

        Returns:
            A2AOutput: 사용자에게 전달 가능한 최종 표준 출력
        """
        raise NotImplementedError(
            'extract_final_output method must be implemented'
        )

    def create_a2a_output(  # noqa: PLR0913
        self,
        status: Literal['working', 'completed', 'failed', 'input_required'],
        text_content: str | None = None,
        data_content: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        stream_event: bool = False,
        final: bool = False,
        **kwargs: Any,
    ) -> A2AOutput:
        """A2A 표준 출력 사전을 생성하는 헬퍼 메서드입니다.

        Args:
            status: 에이전트의 현재 상태
            text_content: TextPart로 전달할 텍스트 내용
            data_content: DataPart로 전달할 구조화 데이터
            metadata: 타임스탬프, 노드명 등 부가 메타데이터
            stream_event: 스트리밍 이벤트 여부
            final: 최종 출력 여부
            **kwargs: 추가 필드. ``error_message``, ``requires_approval`` 등

        Returns:
            A2AOutput: 표준화된 출력 사전
        """
        output: A2AOutput = {
            'agent_type': self.agent_type,
            'status': status,
            'text_content': text_content,
            'data_content': data_content,
            'metadata': metadata or {},
            'stream_event': stream_event,
            'final': final,
            'error_message': kwargs.get('error_message'),
            'requires_approval': kwargs.get('requires_approval'),
        }

        return output

    def format_error(
        self, error: Exception, context: str | None = None
    ) -> A2AOutput:
        """예외를 A2A 표준 에러 출력으로 변환합니다.

        Args:
            error: 발생한 예외 객체
            context: 예외 발생 위치/맥락에 대한 부가 설명 또는 ``None``

        Returns:
            A2AOutput: 상태가 ``failed`` 인 표준 에러 출력
        """
        error_message = f'{type(error).__name__}: {error!s}'
        if context:
            error_message = f'{context}: {error_message}'

        logger.error(f'A2A Agent Error: {error_message}')

        return self.create_a2a_output(
            status='failed',
            text_content=f'에러가 발생했습니다: {error!s}',
            metadata={'error_type': type(error).__name__, 'context': context},
            final=True,
            error_message=error_message,
        )

    def is_completion_event(self, event: dict[str, Any]) -> bool:
        """해당 스트리밍 이벤트가 완료를 의미하는지 판별합니다.

        Args:
            event: 검사할 스트리밍 이벤트

        Returns:
            bool: 완료 이벤트이면 ``True``
        """
        event_type = event.get('event', '')

        if event_type == 'on_chain_end':
            node_name = event.get('name', '')
            if node_name in ['__end__', 'final', 'complete']:
                return True

        metadata = event.get('metadata', {})
        return bool(metadata.get('is_final', False))

    def extract_llm_content(self, event: dict[str, Any]) -> str | None:
        """스트리밍 이벤트에서 LLM 텍스트 조각을 추출합니다.

        Args:
            event: LLM 출력이 포함되었을 수 있는 스트리밍 이벤트

        Returns:
            str | None: 추출된 텍스트. LLM 이벤트가 아니면 ``None``
        """
        if event.get('event') != 'on_llm_stream':
            return None

        data = event.get('data', {})
        chunk = data.get('chunk', {})

        if hasattr(chunk, 'content'):
            return chunk.content

        if isinstance(chunk, dict):
            return chunk.get('content', '')

        return None


class A2AStreamBuffer:
    """스트리밍 텍스트를 관리하기 위한 버퍼.

    스트리밍 중 수신한 토큰을 누적하다가, 적절한 시점에 묶어서 내보내
    사용자 경험을 개선합니다. 임계치에 도달하면 플러시를 권고합니다.
    """

    def __init__(self, max_size: int = 100):
        """스트림 버퍼를 초기화합니다.

        Args:
            max_size: 자동 플러시를 권고하기 전까지의 누적 크기 임계치
        """
        self.buffer: list[str] = []
        self.size: int = 0
        self.max_size = max_size

    def add(self, content: str) -> bool:
        """버퍼에 내용을 추가합니다.

        Args:
            content: 추가할 텍스트 내용

        Returns:
            bool: 플러시 권고 임계치에 도달하면 ``True``
        """
        if not content:
            return False

        self.buffer.append(content)
        self.size += len(content)

        return self.size >= self.max_size

    def flush(self) -> str:
        """버퍼를 비우고 누적된 내용을 반환합니다.

        Returns:
            str: 지금까지 누적된 텍스트
        """
        if not self.buffer:
            return ''

        content = ''.join(self.buffer)
        self.buffer.clear()
        self.size = 0

        return content

    def has_content(self) -> bool:
        """버퍼에 내용이 존재하는지 여부를 반환합니다."""
        return len(self.buffer) > 0
