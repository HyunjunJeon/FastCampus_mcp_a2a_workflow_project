"""Simplified configuration and models for A2A integration."""


from pydantic import BaseModel, ConfigDict, Field


class LangGraphExecutorConfig(BaseModel):
    """Simplified configuration for LangGraph A2A Executor.

    Focuses only on essential settings without over-engineering.
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
    )

    # Core settings
    enable_streaming: bool = Field(
        default=False,  # 스트리밍 비활성화 - blocking 모드 문제 해결
        description='Enable streaming responses',
    )

    enable_interrupt_handling: bool = Field(
        default=True, description='Enable Human-in-the-Loop interrupt handling'
    )

    task_timeout_seconds: int = Field(
        default=300, description='Task timeout in seconds', gt=0
    )

    # Text extraction
    custom_text_keys: list[str] | None = Field(
        default=None, description='Custom keys for text extraction from results'
    )

    # Strategy configuration for custom processors
    strategy_config: dict | None = Field(
        default=None,
        description='Additional configuration for custom strategies and processors',
    )
