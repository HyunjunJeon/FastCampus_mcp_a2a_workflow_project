#!/usr/bin/env python3
"""Memory Agent A2A 예제.

이 예제는 A2A 프로토콜로 래핑된 Memory Agent를 사용하는 방법을 보여줍니다.
A2A 표준 인터페이스를 통해 메모리 작업을 수행합니다.
"""

import asyncio
import sys

from datetime import datetime
from pathlib import Path

import pytz


# 프로젝트 루트를 Python 경로에 추가
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.agents.knowledge.knowledge_agent_a2a import KnowledgeA2AAgent


async def test_a2a_save_knowledge():
    """A2A 인터페이스를 통한 메모리 저장."""
    print("=" * 50)
    print("1. A2A 메모리 저장 테스트")
    print("=" * 50)

    # Memory A2A Agent 초기화
    agent = KnowledgeA2AAgent(is_debug=True)

    # A2A 형식 입력
    input_dict = {
        "messages": [
            {"role": "user", "content": "중요 정보: 프로젝트명은 AI Assistant, 기술 스택은 Python, LangChain, FastAPI"}
        ]
    }

    # 설정 (선택사항)
    config = {
        "configurable": {
            "thread_id": f"memory-save-{datetime.now(pytz.UTC).isoformat()}"
        }
    }

    # A2A 실행
    result = await agent.execute_for_a2a(input_dict, config)

    print("A2A 응답:")
    print(f"- 상태: {result['status']}")
    print(f"- 텍스트: {result['text_content']}")
    if result.get('data_content'):
        print(f"- 데이터: {result['data_content']}")
    print(f"- 최종: {result['final']}")

    return result


async def test_a2a_retrieve_knowledge():
    """A2A 인터페이스를 통한 메모리 조회."""
    print("\n" + "=" * 50)
    print("2. A2A 메모리 조회 테스트")
    print("=" * 50)

    # Memory A2A Agent 초기화
    agent = KnowledgeA2AAgent(is_debug=True)

    # A2A 형식 입력
    input_dict = {
        "messages": [
            {"role": "user", "content": "프로젝트 정보를 조회해주세요"}
        ]
    }

    # A2A 실행
    result = await agent.execute_for_a2a(input_dict)

    print("A2A 응답:")
    print(f"- 상태: {result['status']}")
    print(f"- 텍스트: {result['text_content']}")
    if result.get('data_content') and result['data_content'].get('retrieved_memories'):
        print(f"- 검색된 메모리 수: {len(result['data_content']['retrieved_memories'])}")

    return result


async def test_a2a_complex_workflow() -> None:
    """A2A 복잡한 워크플로우."""
    print("\n" + "=" * 50)
    print("5. A2A 복잡한 워크플로우 테스트")
    print("=" * 50)

    # Memory A2A Agent 초기화
    agent = KnowledgeA2AAgent(is_debug=True)

    # 여러 작업을 순차적으로 실행
    workflows = [
        {
            "description": "회의 내용 저장",
            "messages": [
                {"role": "user", "content": "오늘 회의: 새로운 AI 기능 추가, 담당자는 김개발, 마감일은 다음 주 금요일"}
            ]
        },
        {
            "description": "담당자 정보 조회",
            "messages": [
                {"role": "user", "content": "김개발이 담당하는 작업이 뭐였죠?"}
            ]
        },
        {
            "description": "마감일 업데이트",
            "messages": [
                {"role": "user", "content": "AI 기능 추가 마감일을 다다음 주 월요일로 변경합니다"}
            ]
        }
    ]

    for workflow in workflows:
        print(f"\n작업: {workflow['description']}")

        input_dict = {"messages": workflow['messages']}
        result = await agent.execute_for_a2a(input_dict)

        print(f"- 상태: {result['status']}")
        print(f"- 응답: {result['text_content'][:100]}...")


async def test_a2a_final_output() -> None:
    """A2A 최종 출력 추출."""
    print("\n" + "=" * 50)
    print("6. A2A 최종 출력 추출 테스트")
    print("=" * 50)

    # Memory A2A Agent 초기화
    agent = KnowledgeA2AAgent(is_debug=True)

    # 샘플 최종 상태
    final_state = {
        "workflow_phase": "completed",
        "messages": [],
        "active_memories": [
            {
                "id": "mem_123",
                "content": "테스트 메모리",
                "category": "test",
                "importance": "high"
            }
        ],
        "retrieved_memories": [
            {
                "id": "mem_456",
                "content": "검색된 메모리",
                "category": "search",
                "importance": "medium"
            }
        ],
        "operation_history": [
            {
                "operation_type": "save",
                "success": True,
                "timestamp": datetime.now(pytz.UTC).isoformat()
            }
        ]
    }

    # 최종 출력 추출
    final_output = agent.extract_final_output(final_state)

    print("최종 출력:")
    print(f"- 상태: {final_output['status']}")
    print(f"- 텍스트: {final_output['text_content']}")
    print("- 데이터 포함 항목:")
    if final_output.get('data_content'):
        for key in final_output['data_content']:
            print(f"  - {key}")
    print(f"- 메타데이터: {final_output['metadata']}")


async def main() -> None:
    """메인 실행 함수."""
    print("\n" + "🧠 Knowledge Agent A2A 예제 시작")
    print("=" * 60)

    try:
        # 1. 메모리 저장
        await test_a2a_save_knowledge()

        # 2. 메모리 조회
        await test_a2a_retrieve_knowledge()

        # 3. 복잡한 워크플로우
        await test_a2a_complex_workflow()

        # 4. 최종 출력 추출
        await test_a2a_final_output()

        print("\n" + "=" * 60)
        print("✅ 모든 A2A 테스트 완료!")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 비동기 실행
    asyncio.run(main())
