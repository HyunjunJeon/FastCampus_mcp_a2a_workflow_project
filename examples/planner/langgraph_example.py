#!/usr/bin/env python3
"""Planner Agent - LangGraph 직접 호출 예제.

Planner Agent를 직접 import하여 사용하는 예제입니다.
create_react_agent 기반 API를 사용하여 작업 계획을 수립합니다.

실행 전제 조건:
- OpenAI API 키가 설정되어 있어야 함
- o3-mini 추론 모델에 접근 가능해야 함!! (또는 추론형 모델 다른 것도 괜찮음.)
"""

import asyncio
import json
import sys

from pathlib import Path


# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# 공통 모듈 import
from examples.common.logging import (  # noqa: E402
    LogCapture,
    get_log_filename,
    get_result_filename,
)
from src.agents.planner.planner_agent_lg import (  # noqa: E402
    create_planner_agent,
    create_task_plan,
)


def print_section(title: str) -> None:
    """섹션 구분선 출력."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


async def test_simple_request():
    """단순 요청 테스트.

    기본적인 작업 분해와 계획 수립을 테스트합니다.
    """
    print("-"*40)
    print("테스트 1: 단순 요청 - 주식 분석")
    print("-"*40)

    # 에이전트 생성
    agent = await create_planner_agent(is_debug=False)

    # 작업 계획 실행
    request = "AAPL 주식을 분석하고 투자 추천을 제공해주세요"
    result = await create_task_plan(
        agent=agent,
        user_request=request,
        context_id="test_simple"
    )

    # 결과 출력
    print("\n[성공] 실행 완료!")
    print(f"\n워크플로우 상태: {result.get('workflow_status')}")
    print(f"성공: {result.get('success')}")

    if result.get('success') and result.get('result'):
        print("\n생성된 계획:")
        plan_content = result['result'].get('plan', '')

        # JSON으로 파싱 시도
        if plan_content.strip().startswith('['):
            try:
                plan_json = json.loads(plan_content)
                for i, task in enumerate(plan_json, 1):
                    print(f"\n  단계 {task.get('step_number', i)}:")
                    print(f"    에이전트: {task.get('agent_to_use')}")
                    print(f"    작업: {task.get('prompt')[:100]}...")
                    print(f"    의존성: {task.get('dependencies', [])}")
                    if 'expected_output' in task:
                        print(f"    예상 출력: {task.get('expected_output')[:50]}...")
            except:
                print(plan_content[:500])
        else:
            print(plan_content[:500])

    return result


async def test_complex_workflow():
    """복잡한 워크플로우 테스트.

    다단계 의존성이 있는 복잡한 작업 계획을 수립합니다.
    """
    print("-"*40)
    print("테스트 2: 복잡한 워크플로우 - 포트폴리오 최적화")
    print("-"*40)

    # 에이전트 생성
    agent = await create_planner_agent(is_debug=False)

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

    print(f"\n복잡한 요청: {request[:100]}...")

    result = await create_task_plan(
        agent=agent,
        user_request=request,
        context_id="test_complex"
    )

    if result.get('success'):
        data = result.get('result', {})
        if data:
            print("\n[성공] 복잡한 계획 생성됨:")

            # 에이전트별 작업 분배 분석 (있을 때만 출력)
            if "agent_assignments" in data:
                assignments = data["agent_assignments"]
                print("\n에이전트 작업 분배:")
                for agent_name, task_ids in assignments.items():
                    print(f"    {agent_name}: {len(task_ids)}개 작업")

            # 계획(JSON 문자열)을 파싱하여 분석
            plan_content = data.get("plan", "")
            plan_json = None
            if isinstance(plan_content, list):
                plan_json = plan_content
            elif isinstance(plan_content, str) and plan_content.strip().startswith('['):
                try:
                    plan_json = json.loads(plan_content)
                except Exception:
                    plan_json = None

            if plan_json:
                dep_count = sum(1 for t in plan_json if t.get("dependencies"))
                parallel_count = sum(1 for t in plan_json if not t.get("dependencies"))

                print("\n작업 의존성:")
                print(f"    순차 작업: {dep_count}개")
                print(f"    병렬 작업: {parallel_count}개")

                # 중요 경로 찾기
                max_chain = 0
                for task in plan_json:
                    chain_length = 1
                    deps = task.get("dependencies", [])
                    while deps:
                        chain_length += 1
                        # 의존성이 있는 작업들 찾기
                        next_deps = []
                        for dep in deps:
                            try:
                                dep_num = int(str(dep).replace("task_", ""))
                            except ValueError:
                                continue
                            dep_task = next((t for t in plan_json if t.get("step_number") == dep_num), None)
                            if dep_task:
                                next_deps.extend(dep_task.get("dependencies", []))
                        deps = next_deps
                    max_chain = max(max_chain, chain_length)

                print(f"    중요 경로 길이: {max_chain}단계")

                return data

    print("[오류] 복잡한 계획 수립 실패")
    return None


async def test_dependency_chain():
    """의존성 체인 테스트.

    명확한 의존성이 있는 작업들의 순서를 분석합니다.
    """
    print("-"*40)
    print("테스트 3: 의존성 체인 - 거래 전략")
    print("-"*40)

    # 에이전트 생성
    agent = await create_planner_agent(is_debug=False)

    # 명확한 의존성이 있는 요청
    request = """
    거래 전략을 실행해주세요:
    먼저 SPY의 시장 데이터를 수집하고
    그 다음 기술적 지표를 분석한 후
    분석 결과를 바탕으로 진입점을 결정하고
    마지막으로 적절한 포지션 크기로 거래를 실행하세요
    """

    # 작업 계획 실행
    result = await create_task_plan(
        agent=agent,
        user_request=request,
        context_id="test_deps"
    )

    # 의존성 체인 분석
    print("\n의존성 체인 분석:")

    if result.get('success') and result.get('result'):
        plan_content = result['result'].get('plan', '')

        if plan_content.strip().startswith('['):
            try:
                plan_json = json.loads(plan_content)

                print(f"총 단계: {len(plan_json)}개")

                for task in plan_json:
                    step = task.get('step_number')
                    deps = task.get('dependencies', [])
                    if deps:
                        print(f"  단계 {step}는 다음에 의존: {deps}")
                    else:
                        print(f"  단계 {step}는 의존성 없음 (즉시 시작 가능)")

            except:
                print("계획을 의존성 분석용으로 파싱할 수 없음")

    return result


async def test_minimum_decomposition():
    """최소 분해 검증 테스트.

    플래너가 최소 5단계 이상으로 작업을 분해하는지 확인합니다.
    """
    print("-"*40)
    print("테스트 4: 최소 분해 검증 - 단순 요청")
    print("-"*40)

    # 에이전트 생성
    agent = await create_planner_agent(is_debug=False)

    # 단순한 요청도 분해되어야 함
    request = "날씨를 확인해주세요"

    # 작업 계획 실행
    result = await create_task_plan(
        agent=agent,
        user_request=request,
        context_id="test_minimum"
    )

    print("\n최소 분해 테스트:")

    if result.get('success') and result.get('result'):
        plan_content = result['result'].get('plan', '')

        if plan_content.strip().startswith('['):
            try:
                plan_json = json.loads(plan_content)
                task_count = len(plan_json)

                print(f"생성된 작업 수: {task_count}개")

                if task_count >= 5:
                    print("✅ 통과: 최소 5단계 이상 요구사항 충족")
                else:
                    print(f"❌ 실패: {task_count}개 작업만 생성됨 (5개 이상 필요)")

                for task in plan_json:
                    print(f"  단계 {task.get('step_number')}: {task.get('prompt')[:60]}...")

            except:
                print("작업 개수 확인을 위한 계획 파싱 불가")

    return result


async def main() -> None:
    """메인 실행 함수."""
    # 로그 캡처 시작
    log_capture = LogCapture()
    log_capture.start_capture()

    try:
        print_section("Planner Agent - LangGraph 예제")
        print("Planner Agent를 직접 사용하여 작업 계획을 수립합니다.")

        # 테스트 실행
        all_results = []

        # 테스트 1: 단순 요청
        result1 = await test_simple_request()
        all_results.append(result1)
        print("\n" + "="*60)

        # 테스트 2: 복잡한 워크플로우
        result2 = await test_complex_workflow()
        all_results.append(result2)
        print("\n" + "="*60)

        # 테스트 3: 의존성 체인
        result3 = await test_dependency_chain()
        all_results.append(result3)
        print("\n" + "="*60)

        # 테스트 4: 최소 분해
        result4 = await test_minimum_decomposition()
        all_results.append(result4)

        print_section("테스트 완료")
    except Exception as e:
        print(f"\n❌ 실행 중 오류 발생: {e!s}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
