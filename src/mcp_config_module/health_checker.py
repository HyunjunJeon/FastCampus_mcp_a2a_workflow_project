"""MCP Service Health Checker.

This module provides health checking capabilities for MCP services
to ensure they are ready before attempting to use them.
"""

import asyncio
import logging

import httpx


logger = logging.getLogger(__name__)

# HTTP Status Code Constants
HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_METHOD_NOT_ALLOWED = 405
HTTP_NOT_ACCEPTABLE = 406


class MCPHealthChecker:
    """MCP 서비스 헬스체크 시스템.

    각 MCP 서비스의 상태를 확인하고 준비될 때까지 대기하는 기능을 제공합니다.
    Docker와 로컬 환경 모두를 지원하며, 서비스별 특성에 맞는 헬스체크를 수행합니다.
    """

    # MCP 서비스별 헬스체크 엔드포인트 정의
    # 각 서비스는 로컬과 Docker 환경에서 다른 URL을 가짐
    MCP_ENDPOINTS = {
        # OpenMemory: 메모리 저장/검색 서비스
        'openmemory-mcp': {
            'local': 'http://localhost:8031/health',
            'docker': 'http://openmemory-mcp:8031/health'
        },
        'playwright-mcp': {
            'local': 'http://localhost:8931/mcp',
            'docker': 'http://host.docker.internal:8931/mcp'  # Docker에서 호스트 접근
        },
        # Notion: Notion API 통합 서비스
        'notion-mcp': {
            'local': 'http://localhost:8930/health',
            'docker': 'http://notion-mcp:3000/health'
        },
        # LangChain Sandbox: Python 코드 실행 환경
        'langchain-sandbox': {
            'local': 'http://localhost:8035/health',
            'docker': 'http://langchain-sandbox-mcp:8035/health'
        },
    }

    @classmethod
    def _get_endpoint(cls, service_name: str, is_docker: bool = False) -> str | None:
        """서비스 엔드포인트 URL 가져오기.

        Args:
            service_name: 서비스 이름
            is_docker: Docker 환경 여부

        Returns:
            엔드포인트 URL 또는 None
        """
        if service_name not in cls.MCP_ENDPOINTS:
            return None

        env_key = 'docker' if is_docker else 'local'
        return cls.MCP_ENDPOINTS[service_name].get(env_key)

    @classmethod
    async def check_service(
        cls,
        service_name: str,
        is_docker: bool = False,
        timeout: float = 5.0
    ) -> bool:
        """단일 MCP 서비스 상태 확인.

        각 서비스의 특성에 맞는 헬스체크를 수행합니다.
        Playwright는 SSE 기반이므로 특별한 처리가 필요합니다.

        Args:
            service_name: 확인할 서비스 이름
            is_docker: Docker 환경 여부
            timeout: 요청 타임아웃 (초)

        Returns:
            서비스 사용 가능 여부
        """
        # 서비스에 해당하는 엔드포인트 URL 가져오기
        endpoint = cls._get_endpoint(service_name, is_docker)
        if not endpoint:
            logger.warning(f"Unknown service: {service_name}")
            return False

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                # Playwright MCP는 SSE(Server-Sent Events) 기반이므로 특별 처리 필요
                if service_name == 'playwright-mcp':
                    # Playwright MCP는 streamable_http 프로토콜을 사용하는 특수 서버
                    # 일반적인 health check 엔드포인트가 없음
                    # 서버 동작 여부는 연결 가능 여부로 판단
                    try:
                        # 루트 경로로 테스트 요청 전송
                        test_url = endpoint.replace('/mcp', '/')
                        response = await client.get(test_url, timeout=2.0)
                        # SSE 서버는 일반 GET 요청에 400/405/406 등을 반환할 수 있음
                        # 이러한 응답도 서버가 동작 중임을 의미
                        is_healthy = response.status_code in [HTTP_OK, HTTP_BAD_REQUEST, HTTP_METHOD_NOT_ALLOWED, HTTP_NOT_ACCEPTABLE]
                        if response.status_code == HTTP_BAD_REQUEST:
                            logger.debug("Playwright MCP returned 400 (expected for SSE server)")
                    except httpx.ConnectError:
                        # 연결 실패 = 서버 미동작
                        is_healthy = False
                    except Exception as e:
                        # 기타 예외도 실패로 처리
                        logger.debug(f"Playwright MCP check error: {e}")
                        is_healthy = False
                else:
                    # 일반 MCP 서비스들은 표준 HTTP GET 요청으로 확인
                    response = await client.get(endpoint)
                    # 200 OK 응답이면 정상
                    is_healthy = response.status_code == HTTP_OK

                # 헬스체크 결과 로깅
                if is_healthy:
                    logger.info(f"✅ {service_name} is healthy")
                else:
                    logger.warning(f"⚠️ {service_name} returned unhealthy status")

                return is_healthy

        except httpx.TimeoutException:
            logger.warning(f"⏱️ {service_name} health check timed out")
            return False
        except httpx.ConnectError:
            logger.warning(f"❌ {service_name} is not reachable at {endpoint}")
            return False
        except Exception as e:
            logger.error(f"Error checking {service_name}: {e}")
            return False

    @classmethod
    async def check_all_services(
        cls,
        is_docker: bool = False,
        timeout: float = 5.0
    ) -> dict[str, bool]:
        """모든 MCP 서비스 상태 확인.

        Args:
            is_docker: Docker 환경 여부
            timeout: 각 서비스 체크 타임아웃

        Returns:
            서비스별 상태 딕셔너리
        """
        results = {}
        tasks = []
        service_names = list(cls.MCP_ENDPOINTS.keys())

        for service_name in service_names:
            task = asyncio.create_task(
                cls.check_service(service_name, is_docker, timeout)
            )
            tasks.append((service_name, task))

        for service_name, task in tasks:
            try:
                results[service_name] = await task
            except Exception as e:
                logger.error(f"Error checking {service_name}: {e}")
                results[service_name] = False

        return results

    @classmethod
    async def wait_for_services(
        cls,
        services: list[str],
        is_docker: bool = False,
        timeout: int = 60,
        check_interval: float = 2.0
    ) -> bool:
        """특정 서비스들이 준비될 때까지 대기.

        지정된 서비스들을 주기적으로 체크하면서 모두 준비될 때까지 대기합니다.
        타임아웃이 발생하면 예외를 발생시킵니다.

        Args:
            services: 확인할 서비스 이름 리스트
            is_docker: Docker 환경 여부
            timeout: 전체 대기 타임아웃 (초)
            check_interval: 체크 간격 (초)

        Returns:
            모든 서비스가 준비되었는지 여부

        Raises:
            TimeoutError: 타임아웃 내에 서비스가 준비되지 않은 경우
        """
        logger.info(f"Waiting for services: {services}")

        # 시작 시간 기록
        start_time = asyncio.get_event_loop().time()
        # 각 서비스의 준비 상태를 추적하는 딕셔너리
        services_ready = dict.fromkeys(services, False)

        while True:
            # 경과 시간 계산 및 타임아웃 체크
            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed > timeout:
                # 준비되지 않은 서비스 목록 생성
                not_ready = [svc for svc, ready in services_ready.items() if not ready]
                raise TimeoutError(f"Services not ready after {timeout}s: {not_ready}")

            # 아직 준비되지 않은 서비스들에 대해서만 헬스체크 수행
            check_tasks = []
            for service in services:
                if not services_ready[service]:
                    # 비동기 태스크 생성 (개별 타임아웃 2초)
                    task = asyncio.create_task(
                        cls.check_service(service, is_docker, timeout=2.0)
                    )
                    check_tasks.append((service, task))

            # 모든 헬스체크 태스크 결과 수집
            for service, task in check_tasks:
                try:
                    services_ready[service] = await task
                except Exception:
                    # 예외 발생 시 해당 서비스는 준비되지 않은 것으로 처리
                    services_ready[service] = False

            # 모든 서비스가 준비되었는지 확인
            if all(services_ready.values()):
                logger.info("✅ All required services are ready!")
                return True

            # 아직 준비되지 않은 서비스 로깅 및 대기
            not_ready = [svc for svc, ready in services_ready.items() if not ready]
            logger.info(f"Waiting for: {not_ready} (elapsed: {elapsed:.1f}s)")
            # 지정된 간격만큼 대기 후 재시도
            await asyncio.sleep(check_interval)

    @classmethod
    async def ensure_services_ready(
        cls,
        agent_type: str,
        is_docker: bool = False,
        timeout: int = 60
    ) -> bool:
        """에이전트 타입에 필요한 서비스가 준비되었는지 확인.

        Args:
            agent_type: 에이전트 타입 (memory, browser, executor)
            is_docker: Docker 환경 여부
            timeout: 대기 타임아웃

        Returns:
            서비스 준비 여부
        """
        # 에이전트별 필요 서비스 매핑
        agent_services = {
            'memory': ['openmemory-mcp'],
            'browser': ['playwright-mcp'],
            'executor': ['langchain-sandbox'],
            'knowledge': ['openmemory-mcp'],  # knowledge == memory
        }

        required_services = agent_services.get(agent_type, [])
        if not required_services:
            logger.warning(f"Unknown agent type: {agent_type}")
            return True  # 알 수 없는 타입은 통과

        try:
            await cls.wait_for_services(required_services, is_docker, timeout)
            return True
        except TimeoutError as e:
            logger.error(f"Failed to wait for services: {e}")
            return False
