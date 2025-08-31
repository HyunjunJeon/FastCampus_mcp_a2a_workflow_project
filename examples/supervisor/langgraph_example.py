#!/usr/bin/env python3
"""Supervisor Agent - LangGraph 직접 호출 예제.

Supervisor Agent를 직접 사용하여 다중 에이전트 조율을 수행하는 예제입니다.
복잡한 업무를 여러 에이전트가 협력하여 처리하는 전체 워크플로우를 보여줍니다.

실행 전제 조건:
- 모든 하위 에이전트들이 사용 가능해야 함 (Planner, Knowledge, Executor, Browser)
- 각 에이전트별 MCP 서버들이 실행 중이어야 함
"""

import asyncio
import json
import sys

from pathlib import Path
from typing import Any

from langchain_core.messages import HumanMessage


# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# 공통 모듈 import
from examples.common.logging import (  # noqa: E402
    LogCapture,
    get_log_filename,
    get_result_filename,
)
from examples.common.server_checks import check_mcp_servers  # noqa: E402
from src.agents.supervisor.supervisor_agent_lg import (  # noqa: E402
    create_supervisor_agent_lg,
)


def print_section(title: str) -> None:
    """섹션 구분선 출력."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


async def orchestrate_workflow(
    request: str,
    context_id: str = "default",
    is_debug: bool = False
) -> dict[str, Any]:
    """Supervisor Agent를 통한 워크플로우 실행.

    Args:
        request: 사용자 요청
        context_id: 컨텍스트 ID
        is_debug: 디버그 모드 플래그

    Returns:
        실행 결과를 포함한 딕셔너리
    """
    try:
        # Supervisor Agent 생성
        print("\n[정보] Supervisor Agent 생성 중...")
        agent_graph = await create_supervisor_agent_lg(is_debug=is_debug)

        # 메시지 준비
        messages = [HumanMessage(content=request)]

        # 에이전트 실행
        print("[정보] 워크플로우 실행 중...")
        print(f"   요청: {request[:100]}...")

        # graph.ainvoke 호출
        result = await agent_graph.ainvoke(
            {"messages": messages},
            config={"configurable": {"thread_id": context_id}}
        )

        # 결과 처리
        if result:
            # 마지막 메시지 추출
            final_messages = result.get("messages", [])
            if final_messages:
                last_message = final_messages[-1]
                response_content = last_message.content if hasattr(last_message, 'content') else str(last_message)
            else:
                response_content = "응답 없음"

            return {
                "success": True,
                "request": request,
                "response": response_content,
                "message_count": len(final_messages),
                "context_id": context_id
            }
        return {
            "success": False,
            "request": request,
            "error": "에이전트로부터 결과 없음",
            "context_id": context_id
        }

    except Exception as e:
        print(f"[오류] 워크플로우 실행 실패: {e!s}")
        return {
            "success": False,
            "request": request,
            "error": str(e),
            "context_id": context_id
        }


async def test_planning_workflow():
    """계획 기반 조율 워크플로우 테스트.

    Planner → 다른 에이전트들 순차 실행하는 전체 워크플로우를 테스트합니다.
    """
    print_section("테스트 1: 계획 기반 조율 워크플로우")

    request = """
    블로그 웹사이트 구축을 위한 포괄적인 프로젝트를 진행해주세요:

    1. 먼저 상세한 5단계 계획을 수립하세요
    2. 사용자 인증, 포스트 작성/편집, 댓글 시스템, 검색 기능이 포함되어야 합니다
    3. 각 단계별 구체적인 작업과 의존성을 명시하세요
    4. 기술 스택 선택과 아키텍처 설계를 포함하세요
    5. 최종적으로 프로젝트 계획을 문서화하여 저장하세요

    모든 단계를 체계적으로 진행하고 결과를 통합해주세요.
    """

    result = await orchestrate_workflow(
        request=request,
        context_id="test_planning",
        is_debug=False
    )

    # 결과 출력
    if result.get("success"):
        print("[성공] 계획 기반 워크플로우 완료!")
        print(f"   응답 미리보기: {result.get('response', '')[:300]}...")
        print(f"   메시지 수: {result.get('message_count', 0)}")
    else:
        print(f"[실패] 오류: {result.get('error')}")

    return result


async def test_knowledge_workflow():
    """지식 관리 통합 워크플로우 테스트.

    정보 수집 → 정리 → 저장 → 검증의 전체 지식 관리 워크플로우를 테스트합니다.
    """
    print_section("테스트 2: 지식 관리 통합 워크플로우")

    request = """
    FastCampus 멀티 에이전트 시스템에 대한 종합적인 지식 관리를 수행해주세요:

    1. 프로젝트 정보를 체계적으로 정리하고 저장하세요:
       - 프로젝트명: FastCampus Multi-Agent System
       - 기술 스택: Python, LangGraph, MCP, Docker
       - 팀 구성: Alice (백엔드), Bob (프론트엔드), Charlie (DevOps)
       - 스프린트 목표: 월말까지 MVP 완성
       - 핵심 기능: 에이전트 조율, 메모리 지속성, 웹 자동화

    2. 저장 후 "프로젝트 기술 스택"을 검색하여 정보가 올바르게 저장되었는지 검증하세요
    3. 추가로 프로젝트 진행 상황과 팀 역할에 대한 정보도 검색해보세요
    4. 모든 검색 결과를 종합하여 프로젝트 현황 보고서를 작성하세요

    전체 지식 관리 프로세스를 체계적으로 진행해주세요.
    """

    result = await orchestrate_workflow(
        request=request,
        context_id="test_knowledge",
        is_debug=False
    )

    # 결과 출력
    if result.get("success"):
        print("[성공] 지식 관리 워크플로우 완료!")
        print(f"   응답 미리보기: {result.get('response', '')[:500]}...")
        print(f"   총 메시지: {result.get('message_count', 0)}")
    else:
        print(f"[실패] 오류: {result.get('error')}")

    return result


async def test_data_analysis_pipeline():
    """데이터 분석 파이프라인 워크플로우 테스트.

    데이터 생성 → 분석 → 시각화 → 저장의 전체 데이터 파이프라인을 테스트합니다.
    """
    print_section("테스트 3: 데이터 분석 파이프라인")

    request = """
    완전한 데이터 분석 파이프라인을 구축하고 실행해주세요:

    1. 지난 30일간의 샘플 판매 데이터를 생성하세요 (100개 거래)
    2. 주요 지표를 계산하세요: 총 수익, 평균 주문 가치, 최고 판매일
    3. 시각화를 생성하세요: 판매 트렌드 차트, 일별 수익 막대 차트
    4. 분석 결과와 인사이트를 메모리에 저장하세요
    5. 경영진을 위한 요약 보고서를 생성하세요

    Python pandas를 사용하여 데이터 처리를 수행하고 명확한 인사이트를 제공하세요.
    전체 파이프라인의 각 단계를 체계적으로 진행하고 결과를 통합해주세요.
    """

    result = await orchestrate_workflow(
        request=request,
        context_id="test_data_pipeline",
        is_debug=False
    )

    if result.get("success"):
        print("[성공] 데이터 분석 파이프라인 완료!")
        print(f"   파이프라인 결과: {result.get('response', '')[:500]}...")
    else:
        print(f"[실패] 오류: {result.get('error')}")

    return result


async def test_web_research_integration():
    """웹 리서치 통합 워크플로우 테스트.

    브라우저 → 분석 → 문서화의 전체 리서치 워크플로우를 테스트합니다.
    """
    print_section("테스트 4: 웹 리서치 통합 워크플로우")

    request = """
    Python asyncio에 대한 포괄적인 리서치를 수행해주세요:

    1. 브라우저를 사용하여 Python 공식 문서(docs.python.org)에서 asyncio 정보를 수집하세요
    2. 핵심 개념과 주요 기능을 추출하세요
    3. async/await 패턴의 코드 예제를 찾아서 정리하세요
    4. Python 비동기 프로그래밍 모범 사례를 요약하세요
    5. 수집된 모든 정보를 구조화하여 메모리에 저장하세요
    6. 최종적으로 asyncio 학습 가이드 문서를 작성하세요

    전체 리서치 프로세스를 체계적으로 진행하고 실용적인 가이드를 제공해주세요.
    """

    result = await orchestrate_workflow(
        request=request,
        context_id="test_web_research",
        is_debug=False
    )

    # 결과 출력
    if result.get("success"):
        print("[성공] 웹 리서치 워크플로우 완료!")
        print(f"   리서치 결과: {result.get('response', '')[:500]}...")
    else:
        print(f"[실패] 오류: {result.get('error')}")

    return result


async def test_full_integration_workflow():
    """전체 통합 워크플로우 테스트.

    모든 에이전트가 참여하는 복합적인 업무 처리 시나리오를 테스트합니다.
    """
    print_section("테스트 5: 전체 통합 워크플로우")

    request = """
    REST API 기반 할일 관리 애플리케이션 개발 프로젝트를 완전히 진행해주세요:

    1. [Planner] 할일 관리 REST API 구축을 위한 상세한 계획을 수립하세요
    2. [Browser] FastAPI 문서에서 모범 사례와 인증 방법을 리서치하세요
    3. [Executor] 사용자 인증이 포함된 기본 CRUD API를 위한 Python 코드를 작성하세요
    4. [Knowledge] API 엔드포인트 문서와 사용 예제를 저장하세요
    5. [Executor] API 엔드포인트를 위한 단위 테스트를 생성하세요
    6. [Knowledge] 향후 참조를 위해 프로젝트 구조와 설정 지침을 저장하세요

    모든 에이전트를 조율하여 이 워크플로우를 완료하고 포괄적인 최종 보고서를 제공하세요.
    각 단계의 결과가 다음 단계의 입력으로 사용되도록 체계적으로 진행해주세요.
    """

    result = await orchestrate_workflow(
        request=request,
        context_id="test_full_integration",
        is_debug=False
    )

    # 결과 출력
    if result.get("success"):
        print("[성공] 전체 통합 워크플로우 완료!")
        print(f"   통합 결과: {result.get('response', '')[:600]}...")
    else:
        print(f"[실패] 오류: {result.get('error')}")

    return result


async def main() -> None:
    """메인 실행 함수."""
    # 로그 캡처 시작
    log_capture = LogCapture()
    log_capture.start_capture()

    try:
        print_section("Supervisor Agent - LangGraph 예제")
        print("Supervisor Agent를 사용하여 복잡한 워크플로우를 조율합니다.")

        # 1. MCP 서버 상태 확인 (선택사항)
        print("\n[정보] MCP 서버 상태 확인...")
        await check_mcp_servers("all")

        # 2. 테스트 케이스 실행
        all_results = []

        # 테스트 1: 계획 기반 워크플로우
        result1 = await test_planning_workflow()
        all_results.append(result1)
        await asyncio.sleep(2)  # 서버 과부하 방지

        # 테스트 2: 지식 관리 워크플로우
        result2 = await test_knowledge_workflow()
        all_results.append(result2)
        await asyncio.sleep(2)

        # 테스트 3: 데이터 분석 파이프라인
        result3 = await test_data_analysis_pipeline()
        all_results.append(result3)
        await asyncio.sleep(2)

        # 테스트 4: 웹 리서치 통합
        result4 = await test_web_research_integration()
        all_results.append(result4)
        await asyncio.sleep(2)

        # 테스트 5: 전체 통합 워크플로우
        result5 = await test_full_integration_workflow()
        all_results.append(result5)

        # 3. 결과 요약
        print_section("테스트 결과 요약")

        successful_tests = sum(1 for r in all_results if r.get("success"))
        total_tests = len(all_results)

        print(f"✨ 테스트 성공률: {successful_tests}/{total_tests} ({successful_tests/total_tests*100:.1f}%)")


        for i, result in enumerate(all_results):
            status = "✅" if result.get("success") else "❌"
            context_id = result.get("context_id", "unknown")
            print(f"{status} 테스트 {i+1} ({context_id})")

        # 4. 전체 결과를 JSON 파일로 저장
        output_dir = Path("../../logs/examples/langgraph")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / get_result_filename("supervisor_result")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)

        print(f"\n전체 결과가 {output_file}에 저장되었습니다.")

        print_section("테스트 완료")
        print("\n🎯 Supervisor Agent 핵심 기능:")
        print("  - 자동 하위 에이전트 선택 및 조율")
        print("  - 복잡한 작업 분해 및 실행")
        print("  - 결과 통합 및 최종 응답 생성")
        print("  - 에이전트 간 협업 관리")

    except Exception as e:
        print(f"\n❌ 실행 중 오류 발생: {e!s}")
        import traceback
        traceback.print_exc()

    finally:
        try:
            log_capture.stop_capture()
            log_dir = Path("../../logs/examples/langgraph")
            log_dir.mkdir(parents=True, exist_ok=True)
            log_filename = log_dir / get_log_filename("supervisor_langgraph_log")
            log_capture.save_log(str(log_filename))
            print(f"\n실행 로그가 {log_filename}에 저장되었습니다.")
        except Exception as log_error:
            print(f"\n로그 저장 실패: {log_error}")


if __name__ == "__main__":
    asyncio.run(main())
