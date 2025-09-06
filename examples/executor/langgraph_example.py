#!/usr/bin/env python3
"""Task Executor Agent - LangGraph 직접 호출 예제.

Task Executor Agent를 직접 import하여 사용하는 예제입니다.
CodeInterpreter와 Notion MCP를 활용하여 코드 실행 및 문서 관리 작업을 수행합니다.

실행 전제 조건:
- CodeInterpreter 서비스가 활성화되어 있어야 함
- Notion MCP 서버가 실행 중이어야 함 (문서 작업 시)
"""

import asyncio
import json
import os
import sys
import traceback

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
from src.agents.executor.task_executor_agent_lg import (  # noqa: E402
    create_executor_agent,
    execute_task,
)


def print_section(title: str) -> None:
    """섹션 구분선 출력."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


async def test_python_execution() -> dict:
    """Python 코드 실행 테스트.

    CodeInterpreter를 사용하여 Python 코드를 실행하고 결과를 확인합니다.
    """
    print("=" * 50)
    print("1. Python 코드 실행 테스트")
    print("=" * 50)

    # Executor Agent 생성
    agent = await create_executor_agent(is_debug=True)

    # 실행할 Python 코드
    python_code = """
# 피보나치 수열 계산
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[-1] + fib[-2])
    return fib

# 처음 15개 피보나치 수 생성
fib_sequence = fibonacci(15)
print(f"처음 15개 피보나치 수: {fib_sequence}")

# 통계 계산
total = sum(fib_sequence)
average = total / len(fib_sequence)
print(f"합계: {total}")
print(f"평균: {average:.2f}")

# 황금비 근사값 계산
ratios = []
for i in range(2, len(fib_sequence)):
    ratio = fib_sequence[i] / fib_sequence[i-1]
    ratios.append(ratio)

print(f"황금비 근사값: {ratios[-1]:.6f}")
"""

    # 코드 실행
    result = await execute_task(
        agent=agent,
        task_description="피보나치 수열 계산 및 분석 실행",
        task_type="code",
        parameters={"code": python_code, "language": "python"},
        context_id="test_python"
    )

    print("실행 결과:")
    print(f"- 상태: {result.get('workflow_status')}")
    print(f"- 성공: {result.get('success')}")

    if result.get('result'):
        output = result['result'].get('output', '')
        print("- 출력 미리보기:")
        print(output[:300])

    return result


async def test_data_processing() -> dict:
    """데이터 처리 테스트.

    pandas를 사용하여 데이터를 처리하고 분석합니다.
    """
    print("\n" + "=" * 50)
    print("2. 데이터 처리 테스트")
    print("=" * 50)

    # Executor Agent 생성
    agent = await create_executor_agent(is_debug=True)

    # 데이터 처리 코드
    data_code = """
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 샘플 판매 데이터 생성
np.random.seed(42)
dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
products = ['제품 A', '제품 B', '제품 C']

data = []
for date in dates:
    for product in products:
        sales = np.random.randint(50, 200)
        revenue = sales * np.random.uniform(10, 50)
        data.append({
            'Date': date,
            'Product': product,
            'Sales': sales,
            'Revenue': revenue
        })

df = pd.DataFrame(data)

# 분석
print("데이터셋 개요:")
print(df.head(10))
print(f"\\n데이터셋 크기: {df.shape}")

# 제품별 그룹화
product_summary = df.groupby('Product').agg({
    'Sales': ['sum', 'mean', 'std'],
    'Revenue': ['sum', 'mean', 'max']
}).round(2)

print("\\n제품 성과 요약:")
print(product_summary)

# 일별 트렌드
daily_sales = df.groupby('Date')['Sales'].sum()
print(f"\\n최고 판매일: {daily_sales.idxmax()} - {daily_sales.max()}개")
print(f"최저 판매일: {daily_sales.idxmin()} - {daily_sales.min()}개")

# 요약 보고서
summary_dict = {
    'total_sales': int(df['Sales'].sum()),
    'total_revenue': float(df['Revenue'].sum()),
    'avg_daily_sales': float(daily_sales.mean()),
    'products_analyzed': len(products)
}

print(f"\\n요약 보고서:")
for key, value in summary_dict.items():
    print(f"  {key}: {value:,.2f}" if isinstance(value, float) else f"  {key}: {value}")
"""

    # 데이터 처리 실행
    result = await execute_task(
        agent=agent,
        task_description="pandas를 사용한 판매 데이터 처리 및 분석",
        task_type="data_processing",
        parameters={"code": data_code},
        context_id="test_data"
    )

    print("처리 결과:")
    print(f"- 상태: {result.get('workflow_status')}")
    print(f"- 성공: {result.get('success')}")

    return result


async def test_notion_page_creation() -> dict:
    """Notion 페이지 생성 테스트.

    Notion MCP를 사용하여 문서를 생성합니다.
    """
    print("\n" + "=" * 50)
    print("3. Notion 페이지 생성 테스트")
    print("=" * 50)

    # Executor Agent 생성
    agent = await create_executor_agent(is_debug=True)

    # Notion 부모 페이지/데이터베이스 설정 (환경변수 필요)
    parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")
    parent_database_id = os.getenv("NOTION_PARENT_DATABASE_ID")

    if not parent_page_id and not parent_database_id:
        print("[경고] NOTION_PARENT_PAGE_ID 또는 NOTION_PARENT_DATABASE_ID 환경변수를 설정하세요.")
        return {
            "success": False,
            "result": None,
            "error": "Missing Notion parent. Set NOTION_PARENT_PAGE_ID or NOTION_PARENT_DATABASE_ID.",
            "workflow_status": "failed",
        }

    parent_obj = (
        {"page_id": parent_page_id} if parent_page_id else {"database_id": parent_database_id}
    )

    # Notion 페이지 내용
    notion_content = {
        "title": "멀티 에이전트 시스템 문서",
        "markdown": """
# 멀티 에이전트 시스템 문서

## 개요
LangGraph와 MCP 도구를 사용한 멀티 에이전트 시스템의 아키텍처와 구현을 설명합니다.

## 에이전트 유형

### 1. Planner Agent
- OpenAI o3-mini 추론 모델 사용
- 복잡한 작업을 원자적 단계로 분해
- 작업 의존성과 병렬 실행 관리

### 2. Knowledge Agent
- Docker 기반 MCP Memory Service 활용
- 벡터 임베딩을 통한 시맨틱 검색
- 자연어 시간 쿼리 지원
- 태그 기반 조직화

### 3. Executor Agent
- 이중 기능:
  - ** CodeInterpreter**: Python/JavaScript 실행
  - **Notion MCP**: 문서 및 데이터베이스 관리
- 코드와 문서를 결합한 복잡한 워크플로우 처리

### 4. Browser Agent
- 웹 자동화를 위한 Playwright MCP
- 순차적 도구 실행 (version="v1")
- 탐색, 추출, 폼 작성, 상호작용 지원

## 기술 스택

| 구성 요소 | 기술 |
|-----------|------|
| 프레임워크 | create_react_agent 패턴의 LangGraph |
| LLM | GPT-4 계열 모델 |
| 메모리 | sentence transformers와 SQLite-vec |
| 코드 실행 |  CodeInterpreter 샌드박스 |
| 웹 자동화 | Playwright MCP |
| 문서화 | Notion MCP |

## 주요 특징

✅ **단순화된 아키텍처**: create_react_agent 패턴으로 70% 코드 감소
✅ **MCP 통합**: 모든 에이전트에서 표준화된 도구 로딩
✅ **프로덕션 준비**: 상태 모니터링을 갖춘 Docker 기반 서비스
✅ **타입 안전성**: 완전한 타입 힌트와 검증

## 구현 상태

- [x] create_react_agent로 에이전트 리팩토링
- [x] MCP 도구 통합
- [x] 영어로 된 포괄적인 프롬프트
- [x] 함수 기반 API 패턴
- [x] 테스트 시나리오가 포함된 예제 파일

## 다음 단계

1. 프로덕션 환경 배포
2. 모니터링 및 로깅 구현
3. 더 많은 MCP 도구 통합 추가
4. 성능 최적화

---
*생성일: {datetime.now().isoformat()}*
""",
        "parent": parent_obj,
        "properties": {
            "Type": "Documentation",
            "Status": "Active",
            "Version": "2.0"
        }
    }

    # Notion 페이지 생성
    result = await execute_task(
        agent=agent,
        task_description="Notion에 포괄적인 문서 페이지 생성",
        task_type="notion",
        parameters=notion_content,
        context_id="test_notion"
    )

    print("Notion 생성 결과:")
    print(f"- 상태: {result.get('workflow_status')}")
    print(f"- 성공: {result.get('success')}")

    return result


async def test_notion_report_only() -> dict:
    """노션 도구만 사용하여 보고서를 추가하는 최소 예제.

    Executor Agent를 통해 Notion MCP만 사용해 페이지를 생성합니다.
    """
    print("\n" + "=" * 50)
    print("노션 전용: 보고서 페이지 생성")
    print("=" * 50)

    agent = await create_executor_agent(is_debug=True)

    # Notion 부모 페이지/데이터베이스 설정 (환경변수 필요)
    parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")
    parent_database_id = os.getenv("NOTION_PARENT_DATABASE_ID")

    if not parent_page_id and not parent_database_id:
        print("[경고] NOTION_PARENT_PAGE_ID 또는 NOTION_PARENT_DATABASE_ID 환경변수를 설정하세요.")
        return {
            "success": False,
            "result": None,
            "error": "Missing Notion parent. Set NOTION_PARENT_PAGE_ID or NOTION_PARENT_DATABASE_ID.",
            "workflow_status": "failed",
        }

    parent_obj = (
        {"page_id": parent_page_id} if parent_page_id else {"database_id": parent_database_id}
    )

    notion_params = {
        "title": "LangGraph 주간 보고서",
        "markdown": """
# LangGraph 주간 보고서

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
        "properties": {"Type": "Report", "Status": "Active"},
    }

    result = await execute_task(
        agent=agent,
        task_description="Notion에 주간 보고서 페이지 생성",
        task_type="notion",
        parameters=notion_params,
        context_id="notion_only",
    )

    print("생성 결과:")
    print(f"- 상태: {result.get('workflow_status')}")
    print(f"- 성공: {result.get('success')}")

    return result


async def test_combined_workflow() -> dict:
    """통합 워크플로우 테스트.

    CodeInterpreter와 Notion을 결합한 워크플로우를 실행합니다.
    """
    print("\n" + "=" * 50)
    print("4. 통합 워크플로우 테스트 (CodeInterpreter + Notion)")
    print("=" * 50)

    # Executor Agent 생성
    agent = await create_executor_agent(is_debug=True)

    # 워크플로우: 데이터 분석 → 보고서 생성 → Notion에 저장
    workflow_description = """
    다단계 워크플로우 실행:
    1. 지난 30일간 랜덤 성과 지표 생성 (100개 거래)
    2. 주요 지표 계산: 총 수익, 평균 주문 가치, 최고 판매일
    3. 시각화 생성: 판매 트렌드 차트, 일별 수익 막대 차트
    4. 분석 결과와 인사이트를 메모리에 저장
    5. 경영진 요약 보고서 생성

    데이터 처리에는 Python pandas를 사용하고 명확한 인사이트를 제공한뒤
    Notion API MCP 를 활용하여 결과를 Notion에 저장해주세요
    """

    workflow_params = {
        "steps": [
            {
                "name": "지표 생성",
                "tool": "codeinterpreter",
                "code": """
import random
import json

# 성과 지표 생성
metrics = {
    'response_time': [random.uniform(50, 200) for _ in range(10)],
    'error_rate': [random.uniform(0, 5) for _ in range(10)],
    'throughput': [random.randint(1000, 5000) for _ in range(10)],
    'cpu_usage': [random.uniform(20, 80) for _ in range(10)]
}

# 통계 계산
stats = {}
for metric, values in metrics.items():
    stats[metric] = {
        'avg': sum(values) / len(values),
        'min': min(values),
        'max': max(values)
    }

print("성과 분석 보고서")
print("=" * 30)
for metric, stat in stats.items():
    print(f"\\n{metric.upper()}:")
    print(f"  평균: {stat['avg']:.2f}")
    print(f"  최소: {stat['min']:.2f}")
    print(f"  최대: {stat['max']:.2f}")
"""
            }
        ]
    }

    # 통합 워크플로우 실행
    result = await execute_task(
        agent=agent,
        task_description=workflow_description,
        task_type="workflow",
        parameters=workflow_params,
        context_id="test_workflow"
    )

    print("워크플로우 결과:")
    print(f"- 상태: {result.get('workflow_status')}")
    print(f"- 성공: {result.get('success')}")

    return result

async def main() -> None:
    """메인 실행 함수."""
    # 로그 캡처 시작
    log_capture = LogCapture()
    log_capture.start_capture()

    try:
        print_section("Task Executor Agent - LangGraph 예제")
        print("Task Executor Agent를 직접 사용하여 코드 실행 및 문서 작업을 수행합니다.")

        # 1. MCP 서버 상태 확인 (선택사항)
        print("\n[정보] MCP 서버 상태 확인...")
        await check_mcp_servers("executor")

        # 2. 테스트 케이스 실행
        all_results = []

        # 테스트 1: Python 실행
        result1 = await test_python_execution()
        all_results.append(result1)

        # 테스트 2: 데이터 처리
        result2 = await test_data_processing()
        all_results.append(result2)

        # 테스트 3: Notion 페이지 생성
        result3 = await test_notion_page_creation()
        all_results.append(result3)

        # 테스트 4: 통합 워크플로우
        result4 = await test_combined_workflow() # Quiz: 꼭 이 부분을 Notion 에 저장해주세요!
        all_results.append(result4)

        # 3. 결과 요약
        print_section("테스트 결과 요약")

        successful_tests = sum(1 for r in all_results if r.get("success"))
        total_tests = len(all_results)

        print(f"✨ 테스트 성공률: {successful_tests}/{total_tests} ({successful_tests/total_tests*100:.1f}%)")

        test_names = [
            "Python 코드 실행",
            "데이터 처리",
            "Notion 페이지 생성",
            "통합 워크플로우",
            "오류 처리"
        ]

        for i, result in enumerate(all_results):
            status = "✅" if result.get("success") else "❌"
            print(f"{status} {test_names[i]}")

        # 4. 전체 결과를 JSON 파일로 저장
        output_dir = Path("../../logs/examples/langgraph")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / get_result_filename("executor_result")

        with output_file.open("w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)

        print(f"\n전체 결과가 {output_file}에 저장되었습니다.")

        print_section("테스트 완료")
        print("\nTask Executor Agent 핵심 기능:")
        print("  - CodeInterpreter로 Python/JavaScript 실행")
        print("  - Notion MCP로 문서 관리")
        print("  - 코드와 문서 간 원활한 통합")
        print("  - 자동 패키지 설치")
        print("  - 다중 도구를 사용한 통합 워크플로우")

    except Exception as e:
        print(f"\n❌ 실행 중 오류 발생: {e!s}")
        traceback.print_exc()

    finally:
        try:
            log_capture.stop_capture()
            log_dir = Path("../../logs/examples/langgraph")
            log_dir.mkdir(parents=True, exist_ok=True)
            log_filename = log_dir / get_log_filename("executor_langgraph_log")
            log_capture.save_log(str(log_filename))
            print(f"\n실행 로그가 {log_filename}에 저장되었습니다.")
        except Exception as log_error:
            print(f"\n로그 저장 실패: {log_error}")


if __name__ == "__main__":
    asyncio.run(main())
    # 노션 전용 보고서 예제만 실행하려면 아래 라인을 사용하세요.
    # asyncio.run(test_notion_report_only())
