"""A2A Integration Interface for LangGraph Agents.

This module provides standardized interfaces and utilities for integrating
LangGraph agents with the A2A (Agent-to-Agent) protocol, ensuring consistent
data formats for both streaming and polling operations.
"""

from abc import ABC, abstractmethod
from typing import Any, Literal, TypedDict

import structlog

from a2a.types import AgentCard


logger = structlog.get_logger(__name__)


class A2AOutput(TypedDict):
    """Standardized output format for A2A integration.

    This format unifies streaming events and final results,
    enabling consistent handling in the A2A executor.
    """

    agent_type: str
    status: Literal['working', 'completed', 'failed', 'input_required']
    text_content: str | None  # For TextPart
    data_content: dict[str, Any] | None  # For DataPart (structured data)
    metadata: dict[str, Any]  # Additional context (timestamp, node_name, etc.)
    stream_event: bool  # True for streaming events, False for final results
    final: bool  # True when this is the last output
    error_message: str | None  # Error details if status is "failed"
    requires_approval: bool | None  # For Human-in-the-Loop scenarios


class BaseA2AAgent(ABC):
    """Abstract base class for LangGraph agents with A2A integration.

    This class defines the standard interface that all LangGraph agents
    must implement to support A2A protocol integration.
    """

    def __init__(self) -> None:
        """Initialize the base A2A agent."""
        self.agent_type = self.__class__.__name__.replace('Agent', '')
        logger.info(f'Initializing A2A agent: {self.agent_type}')

    @abstractmethod
    def get_agent_card(self) -> AgentCard:
        """Get the card of the agent."""
        raise NotImplementedError('get_agent_card method must be implemented')

    @abstractmethod
    async def execute_for_a2a(
        self, input_dict: dict[str, Any], config: dict[str, Any] | None = None
    ) -> A2AOutput:
        """
        Execute the agent with A2A-compatible input and output.

        This method replaces direct graph.ainvoke() calls, providing
        a standardized interface for the A2A executor.

        Args:
            input_dict: Input data in standard format
            config: Optional configuration (thread_id, etc.)

        Returns:
            A2AOutput: Standardized output for A2A processing
        """
        raise NotImplementedError('execute_for_a2a method must be implemented')

    @abstractmethod
    def format_stream_event(self, event: dict[str, Any]) -> A2AOutput | None:
        """
        Convert a streaming event to standardized A2A output.

        This method handles various streaming event types:
        - on_llm_stream: LLM token streaming
        - on_chain_start/end: Node execution events
        - on_tool_start/end: Tool execution events

        Args:
            event: Raw streaming event from LangGraph

        Returns:
            A2AOutput if the event should be forwarded, None otherwise
        """
        raise NotImplementedError(
            'format_stream_event method must be implemented'
        )

    @abstractmethod
    def extract_final_output(self, state: dict[str, Any]) -> A2AOutput:
        """
        Extract final output from the agent's state.

        This method is called when the agent execution completes,
        converting the final state to standardized A2A output.

        Args:
            state: Final state from the LangGraph execution

        Returns:
            A2AOutput: Final standardized output
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
        """Helper method to create standardized A2A output.

        Args:
            status: Current status of the agent
            text_content: Text content for TextPart
            data_content: Structured data for DataPart
            metadata: Additional metadata
            stream_event: Whether this is a streaming event
            final: Whether this is the final output
            **kwargs: Additional optional fields

        Returns:
            A2AOutput: Standardized output dictionary
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
        """Format an error as standardized A2A output.

        Args:
            error: The exception that occurred
            context: Optional context about where the error occurred

        Returns:
            A2AOutput: Error formatted as A2A output
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
        """Check if a streaming event indicates completion.

        Args:
            event: Streaming event to check

        Returns:
            bool: True if this is a completion event
        """
        event_type = event.get('event', '')

        if event_type == 'on_chain_end':
            node_name = event.get('name', '')
            if node_name in ['__end__', 'final', 'complete']:
                return True

        metadata = event.get('metadata', {})
        return bool(metadata.get('is_final', False))

    def extract_llm_content(self, event: dict[str, Any]) -> str | None:
        """Extract LLM content from a streaming event.

        Args:
            event: Streaming event containing LLM output

        Returns:
            str: Extracted content, or None if not an LLM event
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
    """Buffer for managing streaming content.

    This class helps accumulate streaming tokens and flush them
    at appropriate intervals for better user experience.
    """

    def __init__(self, max_size: int = 100):
        """Initialize the stream buffer.

        Args:
            max_size: Maximum buffer size before auto-flush
        """
        self.buffer: list[str] = []
        self.size: int = 0
        self.max_size = max_size

    def add(self, content: str) -> bool:
        """Add content to the buffer.

        Args:
            content: Content to add

        Returns:
            bool: True if buffer should be flushed
        """
        if not content:
            return False

        self.buffer.append(content)
        self.size += len(content)

        return self.size >= self.max_size

    def flush(self) -> str:
        """Flush the buffer and return accumulated content.

        Returns:
            str: Accumulated content
        """
        if not self.buffer:
            return ''

        content = ''.join(self.buffer)
        self.buffer.clear()
        self.size = 0

        return content

    def has_content(self) -> bool:
        """Check if buffer has content."""
        return len(self.buffer) > 0
