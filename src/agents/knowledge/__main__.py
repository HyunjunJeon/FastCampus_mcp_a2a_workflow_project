"""A2A Knowledge Agent 실행 모듈."""

import sys

import structlog


logger = structlog.get_logger("KnowledgeAgentA2A")


if __name__ == "__main__":
    try:
        from src.agents.knowledge.knowledge_agent_a2a import (
            main as knowledge_main,
        )
        logger.info("A2A Knowledge Agent를 시작합니다.")
        # uvicorn은 동기로 실행되어야 함
        knowledge_main()
        sys.exit(0)
    except Exception as e:
        logger.error(f"[Server] Error starting A2A Knowledge Agent: {e}")
        sys.exit(1)
