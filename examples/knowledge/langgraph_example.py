#!/usr/bin/env python3
"""Knowledge Agent - LangGraph 직접 호출 예제.

Knowledge Agent를 직접 import하여 사용하는 예제입니다.
MCP Memory Service를 활용하여 메모리 관리 작업을 수행합니다.

실행 전제 조건:
- MCP Memory Service가 Docker로 실행 중이어야 함
- 벡터 검색을 위한 임베딩 모델이 활성화되어 있어야 함
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
from examples.common.server_checks import check_mcp_servers  # noqa: E402
from src.agents.knowledge.knowledge_agent_lg import (  # noqa: E402
    create_knowledge_agent,
    manage_knowledge,
)


def print_section(title: str) -> None:
    """섹션 구분선 출력."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


async def test_store_memory():
    """메모리 저장 테스트.

    태그와 카테고리를 포함한 메모리를 저장합니다.
    """
    print("=" * 50)
    print("1. 메모리 저장 테스트")
    print("=" * 50)

    # Knowledge Agent 생성
    agent = await create_knowledge_agent(is_debug=True)

    # 사용자 정보 저장
    result = await manage_knowledge(
        agent=agent,
        operation="save",
        data={
            "name": "김개발",
            "role": "Python 개발자",
            "preferred_ide": "VS Code",
            "skills": ["Python", "FastAPI", "Docker", "LangGraph"],
            "project": "멀티 에이전트 워크플로우 시스템"
        },
        context_id="test_store"
    )

    print("저장 결과:")
    print(f"- 상태: {result.get('workflow_status')}")
    print(f"- 성공: {result.get('success')}")

    if result.get('result'):
        print(f"- 응답: {result['result'].get('response')[:200]}...")

    return result


async def test_semantic_search():
    """시맨틱 검색 테스트.

    벡터 임베딩을 사용한 의미 기반 검색을 수행합니다.
    """
    print("\n" + "=" * 50)
    print("2. 시맨틱 검색 테스트")
    print("=" * 50)

    # Knowledge Agent 생성
    agent = await create_knowledge_agent(is_debug=True)

    # Python 개발자 정보 검색
    result = await manage_knowledge(
        agent=agent,
        operation="retrieve",
        query="에이전트 시스템을 개발하는 Python 개발자는 누구인가요?",
        context_id="test_semantic"
    )

    print("검색 결과:")
    print(f"- 상태: {result.get('workflow_status')}")
    print(f"- 성공: {result.get('success')}")

    if result.get('result'):
        response = result['result'].get('response', '')
        print("- 발견된 메모리:")
        print(response[:500])

    return result


async def test_time_based_query():
    """시간 기반 쿼리 테스트.

    자연어 시간 표현을 사용한 쿼리를 처리합니다.
    """
    print("\n" + "=" * 50)
    print("3. 시간 기반 쿼리 테스트")
    print("=" * 50)

    # Knowledge Agent 생성
    agent = await create_knowledge_agent(is_debug=True)

    # 최근 이벤트 저장
    await manage_knowledge(
        agent=agent,
        operation="save",
        data="프로젝트 마일스톤: create_react_agent 패턴을 사용한 에이전트 리팩토링 완료",
        context_id="test_time_store"
    )

    # 최근 메모리 쿼리
    result = await manage_knowledge(
        agent=agent,
        operation="retrieve",
        query="오늘 에이전트와 관련해서 무슨 일이 있었나요?",
        context_id="test_time_query"
    )

    print("시간 쿼리 결과:")
    print(f"- 상태: {result.get('workflow_status')}")
    print(f"- 성공: {result.get('success')}")

    if result.get('result'):
        print("- 최근 메모리 발견됨")

    return result


async def test_tag_search():
    """태그 기반 검색 테스트.

    태그를 사용한 메모리 조직화와 검색을 수행합니다.
    """
    print("\n" + "=" * 50)
    print("4. 태그 기반 검색 테스트")
    print("=" * 50)

    # Knowledge Agent 생성
    agent = await create_knowledge_agent(is_debug=True)

    # 특정 태그가 있는 메모리들 저장
    memories_to_store = [
        {
            "content": "FastAPI 백엔드 서버 구성 완료",
            "tags": ["backend", "fastapi", "configuration"]
        },
        {
            "content": "멀티 에이전트 시스템용 Docker compose 설정",
            "tags": ["docker", "deployment", "configuration"]
        },
        {
            "content": "LangGraph 에이전트 구현 가이드라인",
            "tags": ["langgraph", "agents", "documentation"]
        }
    ]

    for memory in memories_to_store:
        await manage_knowledge(
            agent=agent,
            operation="save",
            data=memory,
            context_id=f"test_tag_store_{memories_to_store.index(memory)}"
        )

    # 태그로 검색
    result = await manage_knowledge(
        agent=agent,
        operation="retrieve",
        query="구성(configuration) 관련된 모든 메모리를 보여주세요",
        context_id="test_tag_search"
    )

    print("태그 검색 결과:")
    print(f"- 상태: {result.get('workflow_status')}")
    print(f"- 성공: {result.get('success')}")

    if result.get('result'):
        print("- 구성 관련 메모리 검색됨")

    return result


async def test_complex_workflow():
    """복잡한 워크플로우 테스트.

    저장, 검색, 업데이트, 검증의 전체 메모리 관리 워크플로우를 실행합니다.
    """
    print("\n" + "=" * 50)
    print("5. 복잡한 워크플로우 테스트")
    print("=" * 50)

    # Knowledge Agent 생성
    agent = await create_knowledge_agent(is_debug=True)

    # 복잡한 워크플로우: 프로젝트 정보 저장, 검색, 업데이트, 검증
    workflow_steps = [
        {
            "step": "프로젝트 아키텍처 저장",
            "operation": "save",
            "data": {
                "project": "멀티 에이전트 시스템",
                "architecture": {
                    "agents": ["Planner", "Knowledge", "Executor", "Browser"],
                    "pattern": "create_react_agent",
                    "mcp_tools": ["memory-service", "playwright", "notion", "codeinterpreter"]
                },
                "status": "개발 중"
            }
        },
        {
            "step": "아키텍처 정보 검색",
            "operation": "retrieve",
            "query": "멀티 에이전트 시스템에는 어떤 에이전트들이 있나요?"
        },
        {
            "step": "프로젝트 상태 업데이트",
            "operation": "update",
            "data": "프로젝트 상태 업데이트: 테스트 단계로 변경"
        },
        {
            "step": "업데이트 검증",
            "operation": "retrieve",
            "query": "현재 프로젝트 상태는 무엇인가요?"
        }
    ]

    for step in workflow_steps:
        print(f"\n실행 중: {step['step']}")

        if step['operation'] in ['save', 'update']:
            result = await manage_knowledge(
                agent=agent,
                operation=step['operation'],
                data=step['data'],
                context_id=f"workflow_{workflow_steps.index(step)}"
            )
        else:
            result = await manage_knowledge(
                agent=agent,
                operation=step['operation'],
                query=step.get('query'),
                context_id=f"workflow_{workflow_steps.index(step)}"
            )

        print(f"  결과: {'성공' if result.get('success') else '실패'}")

    print("\n✅ 복잡한 워크플로우 완료")
    return result


async def main() -> None:
    """메인 실행 함수."""
    # 로그 캡처 시작
    log_capture = LogCapture()
    log_capture.start_capture()

    try:
        print_section("Knowledge Agent - LangGraph 예제")
        print("Knowledge Agent를 직접 사용하여 메모리 관리 작업을 수행합니다.")

        # 1. MCP 서버 상태 확인 (선택사항)
        print("\n[정보] MCP 서버 상태 확인...")
        await check_mcp_servers("knowledge")

        # 2. 테스트 케이스 실행
        all_results = []

        # 테스트 1: 메모리 저장
        result1 = await test_store_memory()
        all_results.append(result1)

        # 테스트 2: 시맨틱 검색
        # result2 = await test_semantic_search()
        # all_results.append(result2)

        # # 테스트 3: 시간 기반 쿼리
        # result3 = await test_time_based_query()
        # all_results.append(result3)

        # # 테스트 4: 태그 검색
        # result4 = await test_tag_search()
        # all_results.append(result4)

        # 테스트 5: 복잡한 워크플로우
        result5 = await test_complex_workflow()
        all_results.append(result5)

        # 3. 결과 요약
        print_section("테스트 결과 요약")

        successful_tests = sum(1 for r in all_results if r.get("success"))
        total_tests = len(all_results)

        print(f"✨ 테스트 성공률: {successful_tests}/{total_tests} ({successful_tests/total_tests*100:.1f}%)")

        test_names = [
            "메모리 저장",
            "시맨틱 검색",
            "시간 기반 쿼리",
            "태그 검색",
            "복잡한 워크플로우"
        ]

        for i, result in enumerate(all_results):
            status = "✅" if result.get("success") else "❌"
            print(f"{status} {test_names[i]}")

        # 4. 전체 결과를 JSON 파일로 저장
        output_dir = Path("../../logs/examples/langgraph")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / get_result_filename("knowledge_result")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)

        print(f"\n전체 결과가 {output_file}에 저장되었습니다.")

        print_section("테스트 완료")
        print("\n🧠 Knowledge Agent 핵심 기능:")
        print("  - 벡터 임베딩을 통한 시맨틱 검색")
        print("  - 자연어 시간 쿼리 처리")
        print("  - 태그 기반 조직화")
        print("  - Docker MCP 서비스 통합")
        print("  - 자동 작업 감지")

    except Exception as e:
        print(f"\n❌ 실행 중 오류 발생: {e!s}")
        import traceback
        traceback.print_exc()

    finally:
        try:
            log_capture.stop_capture()
            log_dir = Path("../../logs/examples/langgraph")
            log_dir.mkdir(parents=True, exist_ok=True)
            log_filename = log_dir / get_log_filename("knowledge_langgraph_log")
            log_capture.save_log(str(log_filename))
            print(f"\n실행 로그가 {log_filename}에 저장되었습니다.")
        except Exception as log_error:
            print(f"\n로그 저장 실패: {log_error}")


if __name__ == "__main__":
    # 비동기 테스트 실행
    asyncio.run(main())
