#!/usr/bin/env python3
"""Task Executor Agent A2A 예제.

이 예제는 A2A 프로토콜로 래핑된 Task Executor Agent를 사용하는 방법을 보여줍니다.
A2A 표준 인터페이스를 통해 코드 실행, 문서 작업 등을 수행합니다.
"""

import asyncio
import os
import sys
import traceback

from datetime import datetime
from pathlib import Path
from typing import Any

import pytz


# 프로젝트 루트를 Python 경로에 추가
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.agents.executor.task_executor_agent_a2a import TaskExecutorA2AAgent


async def test_a2a_code_execution() -> dict[str, Any]:
    """A2A 인터페이스를 통한 코드 실행."""
    print("-" * 40)
    print("1. A2A 코드 실행 테스트")
    print("-" * 40)

    # Executor A2A Agent 초기화
    agent = TaskExecutorA2AAgent(is_debug=True)

    # A2A 형식 입력
    code = """
def calculate_factorial(n):
    if n <= 1:
        return 1
    return n * calculate_factorial(n - 1)

# 5! 계산
result = calculate_factorial(5)
print(f"5! = {result}")

# 1부터 5까지의 팩토리얼
for i in range(1, 6):
    print(f"{i}! = {calculate_factorial(i)}")
"""

    input_dict = {
        "messages": [
            {"role": "user", "content": "팩토리얼을 계산하는 Python 코드를 실행해주세요"}
        ],
        "code_to_execute": code,
        "language": "python"
    }

    # 설정
    config = {
        "configurable": {
            "thread_id": f"executor-code-{datetime.now(pytz.UTC).isoformat()}"
        }
    }

    # A2A 실행
    result = await agent.execute_for_a2a(input_dict, config)

    print("A2A 응답:")
    print(f"- 상태: {result['status']}")
    print(f"- 텍스트: {result['text_content']}")
    if result.get('data_content') and result['data_content'].get('code_outputs'):
        print("- 코드 출력:")
        for output in result['data_content']['code_outputs']:
            print(f"  - 언어: {output.get('language')}")
            print(f"  - 결과: {output.get('output')}")
    print(f"- 최종: {result['final']}")

    return result


async def test_a2a_notion_operation() -> dict[str, Any]:
    """A2A 인터페이스를 통한 Notion 작업."""
    print("\n" + "-" * 40)
    print("2. A2A Notion 작업 테스트")
    print("-" * 40)

    # Executor A2A Agent 초기화
    agent = TaskExecutorA2AAgent(is_debug=True)

    # Notion 부모 페이지/데이터베이스 설정 (환경변수 필요)
    parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")
    parent_database_id = os.getenv("NOTION_PARENT_DATABASE_ID")

    if not parent_page_id and not parent_database_id:
        print("[경고] NOTION_PARENT_PAGE_ID 또는 NOTION_PARENT_DATABASE_ID 환경변수를 설정하세요.")
        return {
            "status": "failed",
            "text_content": "Missing Notion parent. Set NOTION_PARENT_PAGE_ID or NOTION_PARENT_DATABASE_ID.",
            "final": True,
            "error_message": "Missing Notion parent",
        }

    parent_obj = (
        {"page_id": parent_page_id} if parent_page_id else {"database_id": parent_database_id}
    )

    # A2A 형식 입력
    input_dict = {
        "messages": [
            {"role": "user", "content": "회의록을 Notion에 작성해주세요"}
        ],
        "notion_config": {
            "title": "2024년 12월 프로젝트 회의록",
            "markdown": """
## 참석자
- 김개발 (PM)
- 이디자인 (Designer)
- 박테스트 (QA)

## 안건
1. 프로젝트 진행 상황 공유
2. 다음 스프린트 계획
3. 이슈 및 리스크 논의

## 결정 사항
- 12월 말 베타 출시
- 성능 최적화 우선순위 높임
- 추가 테스트 기간 확보

## Action Items
- [ ] API 문서 업데이트 (김개발)
- [ ] UI 개선 (이디자인)
- [ ] 테스트 시나리오 작성 (박테스트)
""",
            "parent": parent_obj,
            "properties": {
                "Type": "Meeting Notes",
                "Date": "2024-12-10",
                "Status": "Active"
            }
        }
    }

    # A2A 실행
    result = await agent.execute_for_a2a(input_dict)

    print("A2A 응답:")
    print(f"- 상태: {result['status']}")
    print(f"- 텍스트: {result['text_content']}")
    if result.get('data_content') and result['data_content'].get('notion_operations'):
        print("- Notion 작업:")
        for op in result['data_content']['notion_operations']:
            print(f"  - {op.get('operation_type')} {op.get('resource_type')}")
            print(f"    성공: {op.get('success')}")

    return result


async def test_a2a_notion_report_only() -> dict[str, Any]:
    """노션 도구만 사용하여 보고서를 추가하는 최소 예제.

    TaskExecutorA2AAgent를 통해 Notion MCP만을 사용해 페이지를 생성합니다.
    """
    print("\n" + "-" * 40)
    print("노션 전용: 보고서 페이지 생성")
    print("-" * 40)

    agent = TaskExecutorA2AAgent(is_debug=True)

    # Notion 부모 페이지/데이터베이스 설정
    parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")
    parent_database_id = os.getenv("NOTION_PARENT_DATABASE_ID")

    if not parent_page_id and not parent_database_id:
        print("[경고] NOTION_PARENT_PAGE_ID 또는 NOTION_PARENT_DATABASE_ID 환경변수를 설정하세요.")
        return {
            "status": "failed",
            "text_content": "Missing Notion parent. Set NOTION_PARENT_PAGE_ID or NOTION_PARENT_DATABASE_ID.",
            "final": True,
            "error_message": "Missing Notion parent",
        }

    parent_obj = (
        {"page_id": parent_page_id} if parent_page_id else {"database_id": parent_database_id}
    )

    input_dict = {
        "messages": [
            {"role": "user", "content": "주간 보고서를 Notion에 추가해줘"}
        ],
        "notion_config": {
            "title": "주간 보고서",
            "markdown": """
# 주간 보고서

## 요약
- 이번 주 핵심 지표 검토
- 주요 이슈 및 대응 현황

## 지표
- 신규 사용자: 1,245명
- 전환율: 4.3%
- 이탈률: 22.1%

## 메모
- 다음 주 실험: 온보딩 퍼널 개선 A/B 테스트 예정
""",
            "parent": parent_obj,
            "properties": {
                "Type": "Report",
                "Status": "Active"
            }
        }
    }

    result = await agent.execute_for_a2a(input_dict)

    print("A2A 응답:")
    print(f"- 상태: {result['status']}")
    print(f"- 텍스트: {result['text_content']}")
    if result.get('data_content') and result['data_content'].get('notion_operations'):
        print("- Notion 작업:")
        for op in result['data_content']['notion_operations']:
            print(f"  - {op.get('operation_type')} {op.get('resource_type')} (성공: {op.get('success')})")

    return result


async def test_a2a_data_processing() -> dict[str, Any]:
    """A2A 인터페이스를 통한 데이터 처리."""
    print("\n" + "-" * 40)
    print("3. A2A 데이터 처리 테스트")
    print("-" * 40)

    # Executor A2A Agent 초기화
    agent = TaskExecutorA2AAgent(is_debug=True)

    # 데이터 처리 코드
    code = """
import json

# 샘플 판매 데이터
sales_data = [
    {"product": "노트북", "quantity": 5, "price": 1200000},
    {"product": "마우스", "quantity": 15, "price": 30000},
    {"product": "키보드", "quantity": 10, "price": 80000},
    {"product": "모니터", "quantity": 8, "price": 400000},
    {"product": "스피커", "quantity": 12, "price": 50000}
]

# 매출 계산
for item in sales_data:
    item["total"] = item["quantity"] * item["price"]

# 총 매출
total_revenue = sum(item["total"] for item in sales_data)

# 베스트셀러 (수량 기준)
bestseller = max(sales_data, key=lambda x: x["quantity"])

# 최고 매출 제품
top_revenue = max(sales_data, key=lambda x: x["total"])

print("판매 분석 보고서")
print("-" * 40)
print(f"총 매출: {total_revenue:,}원")
print(f"베스트셀러: {bestseller['product']} ({bestseller['quantity']}개)")
print(f"최고 매출 제품: {top_revenue['product']} ({top_revenue['total']:,}원)")

print("\\n제품별 매출:")
for item in sorted(sales_data, key=lambda x: x["total"], reverse=True):
    print(f"- {item['product']}: {item['total']:,}원")
"""

    # A2A 형식 입력
    input_dict = {
        "messages": [
            {"role": "user", "content": "판매 데이터를 분석하고 보고서를 생성해주세요"}
        ],
        "code_to_execute": code,
        "language": "python"
    }

    # A2A 실행
    result = await agent.execute_for_a2a(input_dict)

    print("A2A 응답:")
    print(f"- 상태: {result['status']}")
    print(f"- 텍스트: {result['text_content']}")

    return result


async def test_a2a_stream_events() -> None:
    """A2A 스트림 이벤트 처리."""
    print("\n" + "-" * 40)
    print("4. A2A 스트림 이벤트 테스트")
    print("-" * 40)

    # Executor A2A Agent 초기화
    agent = TaskExecutorA2AAgent(is_debug=True)

    # 샘플 스트림 이벤트들
    events = [
        {
            "event": "on_chain_start",
            "name": "analyze_task",
            "metadata": {}
        },
        {
            "event": "code_execution",
            "language": "python",
            "code": "print('Hello, World!')"
        },
        {
            "event": "on_tool_start",
            "name": "codeinterpreter_execute",
        },
        {
            "event": "notion_operation",
            "operation_type": "create",
            "resource_type": "page"
        },
        {
            "event": "on_chain_end",
            "name": "__end__",
        }
    ]

    print("스트림 이벤트 처리:")
    for event in events:
        formatted = agent.format_stream_event(event)
        if formatted:
            print(f"\n이벤트 타입: {event.get('event', 'unknown')}")
            print(f"- 상태: {formatted['status']}")
            print(f"- 텍스트: {formatted.get('text_content', 'N/A')}")
            if formatted.get('data_content'):
                print(f"- 데이터: {formatted['data_content']}")
            print(f"- 스트림: {formatted['stream_event']}")
            print(f"- 최종: {formatted['final']}")


async def test_a2a_multi_tool() -> dict[str, Any]:
    """A2A 다중 도구 사용."""
    print("\n" + "-" * 40)
    print("5. A2A 다중 도구 사용 테스트")
    print("-" * 40)

    # Executor A2A Agent 초기화
    agent = TaskExecutorA2AAgent(is_debug=True)

    # Notion 부모 페이지/데이터베이스 설정 (환경변수 필요)
    parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")
    parent_database_id = os.getenv("NOTION_PARENT_DATABASE_ID")

    if not parent_page_id and not parent_database_id:
        print("[경고] NOTION_PARENT_PAGE_ID 또는 NOTION_PARENT_DATABASE_ID 환경변수를 설정하세요.")
        return {
            "status": "failed",
            "text_content": "Missing Notion parent. Set NOTION_PARENT_PAGE_ID or NOTION_PARENT_DATABASE_ID.",
            "final": True,
            "error_message": "Missing Notion parent",
        }

    parent_obj = (
        {"page_id": parent_page_id} if parent_page_id else {"database_id": parent_database_id}
    )

    # 여러 도구를 사용하는 요청
    input_dict = {
        "messages": [
            {"role": "user", "content": "데이터를 분석하고 결과를 Notion에 저장해주세요"}
        ],
        "required_tools": ["codeinterpreter", "notion"],
        "code_to_execute": """
# 분석 수행
data = [10, 20, 30, 40, 50]
average = sum(data) / len(data)
print(f"평균: {average}")
""",
        "notion_config": {
            "title": "분석 결과",
            "markdown": "데이터 평균값 계산 완료",
            "parent": parent_obj
        }
    }

    # A2A 실행
    result = await agent.execute_for_a2a(input_dict)

    print("A2A 응답:")
    print(f"- 상태: {result['status']}")
    print(f"- 텍스트: {result['text_content']}")
    if result.get('data_content') and result['data_content'].get('tool_usage'):
        print(f"- 사용된 도구: {list(result['data_content']['tool_usage'].keys())}")

    return result


async def test_a2a_error_handling() -> dict[str, Any]:
    """A2A 오류 처리."""
    print("\n" + "-" * 40)
    print("6. A2A 오류 처리 테스트")
    print("-" * 40)

    # Executor A2A Agent 초기화
    agent = TaskExecutorA2AAgent(is_debug=True)

    # 오류가 있는 코드
    input_dict = {
        "messages": [
            {"role": "user", "content": "오류가 있는 코드를 실행해주세요"}
        ],
        "code_to_execute": """
# 오류 발생 코드
print("시작")
result = 10 / 0  # ZeroDivisionError
print("끝")  # 실행되지 않음
""",
        "language": "python"
    }

    # A2A 실행
    result = await agent.execute_for_a2a(input_dict)

    print("오류 처리 결과:")
    print(f"- 상태: {result['status']}")
    print(f"- 텍스트: {result['text_content']}")
    if result['status'] == 'failed' and result.get('data_content'):
        print(f"- 실패한 단계 수: {result['data_content'].get('failed_steps_count', 0)}")
        for step in result['data_content'].get('failed_steps', []):
            print(f"  - {step.get('step_id')}: {step.get('error_message')}")
    print(f"- 오류 메시지: {result.get('error_message', 'None')}")

    return result


async def test_a2a_complex_workflow() -> None:
    """A2A 복잡한 워크플로우."""
    print("\n" + "-" * 40)
    print("7. A2A 복잡한 워크플로우 테스트")
    print("-" * 40)

    # Executor A2A Agent 초기화
    agent = TaskExecutorA2AAgent(is_debug=True)

    # Notion 부모 페이지/데이터베이스 설정 (환경변수 필요)
    parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")
    parent_database_id = os.getenv("NOTION_PARENT_DATABASE_ID")

    if not parent_page_id and not parent_database_id:
        print("[경고] NOTION_PARENT_PAGE_ID 또는 NOTION_PARENT_DATABASE_ID 환경변수를 설정하세요.")
        return

    parent_obj = (
        {"page_id": parent_page_id} if parent_page_id else {"database_id": parent_database_id}
    )

    # 복잡한 작업 시퀀스
    workflows = [
        {
            "description": "데이터 생성",
            "messages": [
                {"role": "user", "content": "랜덤 데이터를 생성해주세요"}
            ],
            "code_to_execute": """
import random
data = [random.randint(1, 100) for _ in range(10)]
print(f"생성된 데이터: {data}")
"""
        },
        {
            "description": "통계 계산",
            "messages": [
                {"role": "user", "content": "통계를 계산해주세요"}
            ],
            "code_to_execute": """
import statistics
data = [45, 67, 23, 89, 12, 56, 78, 34, 90, 21]
mean = statistics.mean(data)
median = statistics.median(data)
stdev = statistics.stdev(data)
print(f"평균: {mean:.2f}, 중앙값: {median}, 표준편차: {stdev:.2f}")
"""
        },
        {
            "description": "보고서 작성",
            "messages": [
                {"role": "user", "content": "분석 보고서를 Notion에 작성해주세요"}
            ],
            "notion_config": {
                "title": "데이터 분석 보고서",
                "markdown": "통계 분석 완료",
                "parent": parent_obj
            }
        }
    ]

    for workflow in workflows:
        print(f"\n작업: {workflow['description']}")

        input_dict = {
            "messages": workflow['messages'],
            **{k: v for k, v in workflow.items() if k not in ['description', 'messages']}
        }

        result = await agent.execute_for_a2a(input_dict)

        print(f"- 상태: {result['status']}")
        print(f"- 응답: {result['text_content'][:100]}...")


async def test_a2a_final_output() -> None:
    """A2A 최종 출력 추출."""
    print("\n" + "-" * 40)
    print("8. A2A 최종 출력 추출 테스트")
    print("-" * 40)

    # Executor A2A Agent 초기화
    agent = TaskExecutorA2AAgent(is_debug=True)

    # 샘플 최종 상태
    final_state = {
        "workflow_phase": "completed",
        "task_completed": True,
        "task_type": "code_execution",
        "final_result": {
            "total_steps": 3,
            "successful_steps": 3,
            "failed_steps": 0,
            "code_outputs": [
                {
                    "language": "python",
                    "output": "계산 완료: 42",
                    "execution_time": 0.5
                }
            ],
            "notion_results": [
                {
                    "operation_type": "create",
                    "resource_type": "page",
                    "success": True
                }
            ],
            "summary": "작업 완료: 3/3 단계 성공"
        },
        "completed_steps": [
            {
                "step_id": "step_1",
                "tool_name": "codeinterpreter",
                "success": True
            },
            {
                "step_id": "step_2",
                "tool_name": "notion",
                "success": True
            }
        ],
        "tool_usage_stats": {
            "codeinterpreter": {"calls": 2, "success": 2},
            "notion": {"calls": 1, "success": 1}
        }
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
    print("\n" + " Task Executor Agent A2A 예제 시작")
    print("-" * 40)

    try:
        # 1. 코드 실행
        await test_a2a_code_execution()

        # 2. Notion 작업
        await test_a2a_notion_operation()

        # 3. 데이터 처리
        await test_a2a_data_processing()

        # 4. 스트림 이벤트
        await test_a2a_stream_events()

        # 5. 다중 도구 사용
        await test_a2a_multi_tool()

        # 6. 오류 처리
        await test_a2a_error_handling()

        # 7. 복잡한 워크플로우
        await test_a2a_complex_workflow()

        # 8. 최종 출력 추출
        await test_a2a_final_output()

        print("\n" + "-" * 40)
        print("[성공] 모든 A2A 테스트 완료!")

    except Exception as e:
        print(f"\n[오류] 오류 발생: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    # 기본: 전체 예제 실행
    # asyncio.run(main())

    # 노션 전용 보고서 예제만 실행하려면 아래 라인을 사용하세요.
    asyncio.run(test_a2a_notion_report_only())
