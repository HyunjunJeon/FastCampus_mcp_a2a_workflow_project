"""A2A Task Executor Agent 실행 모듈."""

import sys

import structlog


logger = structlog.get_logger("TaskExecutorAgentA2A")


if __name__ == "__main__":
    try:
        from src.agents.executor.task_executor_agent_a2a import (
            main as executor_main,
        )
        logger.info("A2A Task Executor Agent를 시작합니다.")
        # uvicorn은 동기로 실행되어야 함
        executor_main()
        sys.exit(0)
    except Exception as e:
        logger.error(f"[Server] Error starting A2A Task Executor Agent: {e}")
        sys.exit(1)
