import os

from functools import lru_cache
from pathlib import Path
from typing import Any

from langchain_core.messages import (
    AIMessage,
    convert_to_messages,
    filter_messages,
)
from langchain_core.runnables import RunnableConfig


@lru_cache(1)
def load_env_file() -> None:
    """프로젝트 루트의 .env 파일을 로드."""
    project_root = Path(__file__).parent.parent.parent
    env_path = project_root / '.env'
    if env_path.exists():
        with env_path.open(encoding='utf-8') as f:
            for line in f:
                stripped_line = line.strip()
                if stripped_line.startswith('#') or not stripped_line:
                    continue
                line = stripped_line
                if '=' in line:
                    key, value = line.split('=', 1)
                    value = value.strip('\'"')
                    os.environ[key] = value


def extract_ai_messages_from_response(
    react_agent_response: dict[str, Any],
) -> list[AIMessage]:
    """응답에서 AI 메시지를 추출하는 공통 함수.

    Args:
        react_agent_response: 에이전트 응답 딕셔너리 (full_messages 키 포함)

    Returns:
        List[AIMessage]: 추출된 AI 메시지 리스트
    """
    original_messages = react_agent_response.get('full_messages', [])
    converted_messages = convert_to_messages(original_messages)
    return filter_messages(converted_messages, include_types=[AIMessage])


def get_api_key_for_model(model_name: str, config: RunnableConfig) -> str | None:
    """Get API key for a specific model from environment or config."""
    should_get_from_config = os.getenv('GET_API_KEYS_FROM_CONFIG', 'false')
    model_name = model_name.lower()

    # 모델 타입별 API 키 매핑
    model_key_mapping = {
        'openai': 'OPENAI_API_KEY',
        'anthropic': 'ANTHROPIC_API_KEY',
        'google': 'GOOGLE_API_KEY',
    }

    # 환경 변수에서 가져올지 config에서 가져올지 결정
    if should_get_from_config.lower() == 'true':
        api_keys = config.get('configurable', {}).get('apiKeys', {})
        if not api_keys:
            return None
        source = api_keys
    else:
        source = os.environ

    # 모델 타입에 따라 적절한 API 키 반환
    for model_prefix, key_name in model_key_mapping.items():
        if model_name.startswith(model_prefix):
            return source.get(key_name) if source is os.environ else source.get(key_name)

    return None


def get_tavily_api_key(config: RunnableConfig) -> str | None:
    """Get Tavily API key from environment or config."""
    should_get_from_config = os.getenv('GET_API_KEYS_FROM_CONFIG', 'false')
    if should_get_from_config.lower() == 'true':
        api_keys = config.get('configurable', {}).get('apiKeys', {})
        if not api_keys:
            return None
        return api_keys.get('TAVILY_API_KEY')
    return os.getenv('TAVILY_API_KEY')
