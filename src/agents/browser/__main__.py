"""A2A Browser Agent 실행 모듈."""

import sys

import structlog


logger = structlog.get_logger("BrowserAgentA2A")


if __name__ == "__main__":
    try:
        from src.agents.browser.browser_use_agent_a2a import (
            main as browser_main,
        )
        logger.info("A2A Browser Agent를 시작합니다.")
        # uvicorn은 동기로 실행되어야 함
        browser_main()
        sys.exit(0)
    except Exception as e:
        logger.error(f"[Server] Error starting A2A Browser Agent: {e}")
        sys.exit(1)
