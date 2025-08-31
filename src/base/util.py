import os

from functools import lru_cache
from pathlib import Path
from typing import Any

from langchain_core.messages import (
    AIMessage,
    convert_to_messages,
    filter_messages,
)


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
                parsed_line = stripped_line
                if '=' in parsed_line:
                    key, value = parsed_line.split('=', 1)
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
