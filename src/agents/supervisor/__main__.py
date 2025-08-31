"""A2A Supervisor Agent 실행 모듈."""

import sys

import structlog


logger = structlog.get_logger("SupervisorAgentA2A")


if __name__ == "__main__":
    try:
        from src.agents.supervisor.supervisor_agent_a2a import (
            main as supervisor_main,
        )
        logger.info("A2A Supervisor Agent를 시작합니다.")
        # uvicorn은 동기로 실행되어야 함
        supervisor_main()
        sys.exit(0)
    except Exception as e:
        logger.error(f"[Server] Error starting A2A Supervisor Agent: {e}")
        sys.exit(1)
