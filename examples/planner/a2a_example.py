#!/usr/bin/env python3
"""Planner Agent - A2A 프로토콜 호출 예제.

A2A 프로토콜을 통해 Planner Agent와 통신하는 예제입니다.
Agent는 별도 프로세스로 실행되며, A2A 클라이언트를 통해 원격 호출합니다.

실행 전제 조건:
1. Planner A2A 서버가 실행되어 있어야 함 (포트 8001)
2. OpenAI API 키가 설정되어 있어야 함
"""

import asyncio
import json
import sys
import traceback

from pathlib import Path

import httpx

from a2a.types import DataPart, Part


# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# 공통 모듈 import
from examples.common.logging import (  # noqa: E402
    LogCapture,
    get_log_filename,
    get_result_filename,
)
from src.a2a_integration.a2a_lg_client_utils import (  # noqa: E402
    A2AClientManager,
)


def print_section(title: str) -> None:
    """섹션 구분선 출력."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


async def test_agent_card():
    """에이전트 카드 조회 테스트.

    A2A 서버의 에이전트 정보를 확인합니다.
    """
    print("테스트 1: 에이전트 카드 조회")
    print("-"*40)

    async with httpx.AsyncClient() as client:
        try:
            # 에이전트 카드 조회
            response = await client.get(
                "http://localhost:8001/.well-known/agent-card.json",
                timeout=5.0
            )

            if response.status_code == 200:
                agent_card = response.json()
                print("\n[성공] 에이전트 카드 조회됨:")
                print(f"  이름: {agent_card['name']}")
                print(f"  설명: {agent_card['description']}")
                print(f"  버전: {agent_card['version']}")

                if "skills" in agent_card:
                    print(f"\n사용 가능한 스킬 ({len(agent_card['skills'])}개):")
                    for skill in agent_card['skills']:
                        print(f"    - {skill['id']}: {skill['description']}")

                if "capabilities" in agent_card:
                    print("\n기능:")
                    caps = agent_card['capabilities']
                    print(f"    - 스트리밍: {caps.get('streaming', False)}")
                    print(f"    - 푸시 알림: {caps.get('push_notifications', False)}")

                return agent_card
            print(f"[오류] 에이전트 카드 조회 실패: {response.status_code}")
            return None

        except Exception as e:
            print(f"[오류] 에이전트 카드 조회 중 오류: {e}")
            print("   Planner Agent가 포트 8001에서 실행 중인지 확인하세요")
            return None


async def test_schema_endpoint():
    """스키마 엔드포인트 테스트.

    입력/출력 스키마 정보를 확인합니다.
    """
    print("테스트 2: 입출력 스키마 조회")
    print("-"*40)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "http://localhost:8001/schemas",
                timeout=5.0
            )

            if response.status_code == 200:
                schemas = response.json()
                print("\n[성공] 스키마 조회됨:")

                if "input_schema" in schemas:
                    print("\n입력 스키마:")
                    print(json.dumps(schemas["input_schema"], indent=2, ensure_ascii=False))

                if "output_schema" in schemas:
                    print("\n출력 스키마:")
                    print(json.dumps(schemas["output_schema"], indent=2, ensure_ascii=False))

                return schemas
            print(f"[오류] 스키마 조회 실패: {response.status_code}")
            return None

        except Exception as e:
            print(f"[오류] 스키마 조회 중 오류: {e}")
            return None


async def test_simple_planning():
    """단순 계획 수립 테스트.

    A2A를 통한 기본적인 계획 수립을 테스트합니다.
    """
    print("테스트 3: A2A를 통한 단순 계획 수립")
    print("-"*40)

    # A2A 클라이언트 생성
    client_manager = A2AClientManager(
        base_url="http://localhost:8001",
        streaming=False,
        max_retries=3
    )

    try:
        # 클라이언트 초기화
        await client_manager.initialize()
        print(f"\n[성공] {client_manager.agent_card.name}에 연결됨")

        # 계획 수립 요청
        request = "Tesla 주식을 분석하고 거래 추천을 제공하는 계획을 수립해주세요"
        print(f"\n요청: {request}")

        # 데이터 Part로 전송 (A2A 표준) - send_parts 사용
        resp = await client_manager.send_parts(
            parts=[
                Part(root=DataPart(data={
                    "messages": [{"role": "user", "content": request}],
                    "user_request": request
                }))
            ]
        )

        # 결과 파싱
        data = resp.merged_data if resp.merged_data else (resp.data_parts[0] if resp.data_parts else None)
        if isinstance(data, dict):
            plan_result = data
            if "result" in plan_result:
                plan_data = plan_result["result"]

                print("\n[성공] 계획 생성됨:")

                # 계획 작업 표시
                if "plan" in plan_data and isinstance(plan_data["plan"], list):
                    print(f"\n작업 ({len(plan_data['plan'])}개):")
                    for task in plan_data["plan"]:
                        print(f"\n  단계 {task['step_number']}:")
                        print(f"    에이전트: {task['agent_to_use']}")
                        print(f"    작업: {task['prompt']}")
                        if task['dependencies']:
                            print(f"    의존성: {task['dependencies']}")

                # 메타데이터 표시
                if "metadata" in plan_data:
                    meta = plan_data["metadata"]
                    print("\n계획 메타데이터:")
                    print(f"    총 작업 수: {meta.get('total_tasks', 0)}")
                    print(f"    복잡도 점수: {meta.get('complexity_score', 0):.2f}")
                    print(f"    예상 소요 시간: {meta.get('estimated_duration', 0)}초")

                return plan_data

        print("[오류] 유효한 계획이 반환되지 않음")
        return None

    except Exception as e:
        print(f"[오류] A2A 계획 수립 중 오류: {e}")
        traceback.print_exc()
        return None

    finally:
        await client_manager.close()


async def test_complex_planning():
    """복잡한 계획 수립 테스트.

    의존성이 있는 복잡한 계획 수립을 테스트합니다.
    """
    print("테스트 4: 의존성이 있는 복잡한 계획 수립")
    print("-"*40)

    client_manager = A2AClientManager(
        base_url="http://localhost:8001",
        streaming=False
    )

    try:
        await client_manager.initialize()

        # 복잡한 다단계 요청
        request = """
        포괄적인 투자 분석을 수행해주세요:
        1. FAANG 주식들의 과거 6개월 데이터 수집 (Facebook, Apple, Amazon, Netflix, Google)
        2. 각 주식의 기술적 지표 분석
        3. 포트폴리오 전반의 기본적 지표 비교
        4. 현재 시장 심리 평가
        5. 위험 조정 포트폴리오 추천 생성
        6. 각 포지션의 진입 및 청산 전략 수립
        """

        print(f"\n복잡한 요청: {request}")

        resp = await client_manager.send_parts(
            parts=[
                Part(root=DataPart(data={
                    "messages": [{"role": "user", "content": request}],
                    "user_request": request
                }))
            ]
        )

        data = resp.merged_data if resp.merged_data else (resp.data_parts[0] if resp.data_parts else None)
        if isinstance(data, dict):
            plan_result = data
            if "result" in plan_result:
                plan_data = plan_result["result"]

                print("\n[성공] 복잡한 계획 생성됨:")

                # 에이전트별 작업 분배 분석
                if "agent_assignments" in plan_data:
                    assignments = plan_data["agent_assignments"]
                    print("\n에이전트 작업 분배:")
                    for agent, task_ids in assignments.items():
                        print(f"    {agent}: {len(task_ids)}개 작업")

                # 의존성 분석
                if "plan" in plan_data:
                    dep_count = sum(1 for t in plan_data["plan"] if t["dependencies"])
                    parallel_count = sum(1 for t in plan_data["plan"] if not t["dependencies"])

                    print("\n작업 의존성:")
                    print(f"    순차 작업: {dep_count}개")
                    print(f"    병렬 작업: {parallel_count}개")

                    # 중요 경로 찾기
                    max_chain = 0
                    for task in plan_data["plan"]:
                        chain_length = 1
                        deps = task["dependencies"]
                        while deps:
                            chain_length += 1
                            # 의존성이 있는 작업들 찾기
                            next_deps = []
                            for dep in deps:
                                dep_num = int(dep.replace("task_", ""))
                                dep_task = next((t for t in plan_data["plan"]
                                                if t["step_number"] == dep_num), None)
                                if dep_task:
                                    next_deps.extend(dep_task["dependencies"])
                            deps = next_deps
                        max_chain = max(max_chain, chain_length)

                    print(f"    중요 경로 길이: {max_chain}단계")

                return plan_data

        print("[오류] 복잡한 계획 수립 실패")
        return None

    except Exception as e:
        print(f"[오류] 오류 발생: {e}")
        return None

    finally:
        await client_manager.close()


async def main() -> None:
    """메인 실행 함수."""
    # 로그 캡처 시작
    log_capture = LogCapture()
    log_capture.start_capture()

    try:
        print_section("Planner Agent - A2A 프로토콜 예제")
        print("A2A 프로토콜을 통해 원격 Planner Agent와 통신합니다.")

        # 테스트 실행
        all_results = []

        # 테스트 1: 단순 계획 수립
        result3 = await test_simple_planning()
        all_results.append(result3)

        # 테스트 2: 복잡한 계획 수립
        result4 = await test_complex_planning()
        all_results.append(result4)

        # 결과 요약
        print_section("테스트 결과 요약")

        successful_tests = sum(1 for r in all_results if r is not None)
        total_tests = len(all_results)

        print(f"✨ 테스트 성공률: {successful_tests}/{total_tests} ({successful_tests/total_tests*100:.1f}%)")

        test_names = [
            "에이전트 카드 조회",
            "스키마 엔드포인트",
            "단순 계획 수립",
            "복잡한 계획 수립"
        ]

        for i, result in enumerate(all_results):
            status = "✅" if result is not None else "❌"
            print(f"{status} {test_names[i]}")

        # 전체 결과를 JSON 파일로 저장
        output_dir = Path("../../logs/examples/a2a")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / get_result_filename("planner_a2a_result")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)

        print(f"\n전체 결과가 {output_file}에 저장되었습니다.")

        print_section("테스트 완료")
        print("\n🧠 Planner Agent A2A 핵심 기능:")
        print("  - HTTP 서비스로 원격 계획 수립")
        print("  - 표준 A2A 프로토콜 지원")
        print("  - 에이전트 카드 및 스키마 제공")
        print("  - 복잡한 의존성 분석")

    except Exception as e:
        print(f"\n❌ 실행 중 오류 발생: {e!s}")
        traceback.print_exc()

    finally:
        try:
            log_capture.stop_capture()
            log_dir = Path("../../logs/examples/a2a")
            log_dir.mkdir(parents=True, exist_ok=True)
            log_filename = log_dir / get_log_filename("planner_a2a_log")
            log_capture.save_log(str(log_filename))
            print(f"\n실행 로그가 {log_filename}에 저장되었습니다.")
        except Exception as log_error:
            print(f"\n로그 저장 실패: {log_error}")


if __name__ == "__main__":
    asyncio.run(main())
