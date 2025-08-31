"""Configuration for the Multi-Agent System."""

import os

from typing import Any

from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings


class MCPConfig(BaseModel):
    """Langchain MCP Adapters 규격을 만족하는 MCP 서버 설정."""

    transport: str = Field(
        default='streamable_http',
    )
    url: str | None = Field(
        default=None,
    )


class Configuration(BaseSettings):
    """Main configuration class for the Deep Research agent."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    # MCP server configuration
    mcp_config: MCPConfig | None = Field(
        default=None,
        optional=True,
    )

    # OpenAI Configuration
    openai_api_key: str | None = Field(default=None, alias='OPENAI_API_KEY')

    # LangSmith Configuration
    langsmith_api_key: str | None = Field(
        default=None, alias='LANGSMITH_API_KEY'
    )
    langsmith_project: str | None = Field(
        default='default', alias='LANGSMITH_PROJECT'
    )
    langsmith_tracing: bool = Field(default=False, alias='LANGSMITH_TRACING')

    @classmethod
    def from_runnable_config(
        cls, config: RunnableConfig | None = None
    ) -> 'Configuration':
        """Create a Configuration instance from a RunnableConfig."""
        configurable = config.get('configurable', {}) if config else {}
        field_names = list(cls.model_fields.keys())
        values: dict[str, Any] = {
            field_name: os.environ.get(
                field_name.upper(), configurable.get(field_name)
            )
            for field_name in field_names
        }
        return cls(**{k: v for k, v in values.items() if v is not None})
