#!/usr/bin/env python3
"""Browser Agent - LangGraph 레벨 직접 호출 예제.

BrowserUseAgent를 직접 import하여 사용하는 예제입니다.
Playwright MCP 도구를 활용하여 웹 브라우저 자동화 작업을 수행합니다.

실행 전제 조건:
- Playwright MCP 서버가 실행 중이어야 함
- 포트 8093에서 활성화되어 있어야 함
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
from src.agents.browser.browser_use_agent_lg import (  # noqa: E402
    browse_web,
    create_browser_agent,
)


def print_section(title: str) -> None:
    """섹션 구분선 출력."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


async def main() -> None:
    """메인 실행 함수."""
    # 로그 캡처 시작
    log_capture = LogCapture()
    log_capture.start_capture()

    try:
        print_section("Browser Agent - LangGraph 예제")
        print("Browser Agent를 직접 사용하여 웹 자동화를 수행합니다.")

        # 1. MCP 서버 상태 확인
        if not await check_mcp_servers("browser"):
            print("\n일부 MCP 서버가 실행되지 않았습니다.")
            print("해결 방법: Playwright MCP 서버 실행 확인")

        # 2. Browser Agent 초기화
        print("Browser Agent 생성 중...")
        agent = await create_browser_agent(is_debug=True)

        if not agent:
            print("❌ Browser Agent 생성 실패")
            return

        # 3. 테스트 케이스 실행
        print_section("브라우저 자동화 실행")

        # 테스트 케이스 목록
        test_cases = [
            # {
            #     "name": "웹 페이지 탐색",
            #     "url": "https://example.com",
            #     "action_type": "navigate",
            #     "task": "페이지에 접속하여 타이틀을 확인해주세요",
            #     "context_id": "test_navigate"
            # },
            # {
            #     "name": "데이터 추출",
            #     "url": "https://example.com",
            #     "action_type": "extract",
            #     "task": "페이지의 메인 헤딩과 본문 텍스트를 추출해주세요",
            #     "context_id": "test_extract"
            # },
            # {
            #     "name": "폼 상호작용",
            #     "url": "https://www.google.com",
            #     "action_type": "form",
            #     "task": "검색창에 'LangGraph tutorial'을 입력하고 검색해주세요",
            #     "context_id": "test_form"
            # },
            {
                "name": "복잡한 워크플로우",
                "url": "https://www.google.com",
                "task": """다음 작업을 순차적으로 수행해주세요:
1. Google 홈페이지 접속
2. 'Python LangGraph' 검색
3. 검색 결과 확인
4. 페이지 타이틀과 주요 내용 추출""",
                "context_id": "test_complex"
            }
        ]

        all_results = []

        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🔄 테스트 {i}: {test_case['name']} 실행 중...")
            print(f"   URL: {test_case['url']}")
            print(f"   작업: {test_case['task'][:100]}...")

            try:
                result = await asyncio.wait_for(
                    browse_web(
                        agent=agent,
                        url=test_case["url"],
                        task=test_case["task"],
                        action_type=test_case.get("action_type"),
                        context_id=test_case["context_id"]
                    ),
                    timeout=60.0
                )

                # 결과 출력
                if result.get("success"):
                    print(f"✅ {test_case['name']} 성공!")
                    if result.get("result"):
                        print(f"   - 도구 호출 횟수: {result['result'].get('tool_calls_made', 0)}")
                        print(f"   - 워크플로우 상태: {result.get('workflow_status')}")

                        # 추출된 데이터가 있는 경우
                        if result['result'].get('data'):
                            data = result['result']['data']
                            print(f"   - 추출된 데이터: {str(data)[:200]}...")
                else:
                    print(f"❌ {test_case['name']} 실패")
                    print(f"   오류: {result.get('error', 'Unknown error')}")

                # 결과 저장
                result['test_name'] = test_case['name']
                all_results.append(result)

            except TimeoutError:
                print(f"❌ {test_case['name']} 타임아웃 (60초)")
                all_results.append({
                    "test_name": test_case['name'],
                    "success": False,
                    "error": "Timeout after 60 seconds"
                })
            except Exception as e:
                print(f"❌ {test_case['name']} 실행 중 오류: {e!s}")
                all_results.append({
                    "test_name": test_case['name'],
                    "success": False,
                    "error": str(e)
                })

        # 4. 결과 요약
        print_section("테스트 결과 요약")

        successful_tests = sum(1 for r in all_results if r.get("success"))
        total_tests = len(all_results)

        print(f"✨ 테스트 성공률: {successful_tests}/{total_tests} ({successful_tests/total_tests*100:.1f}%)")

        for result in all_results:
            status = "✅" if result.get("success") else "❌"
            print(f"{status} {result['test_name']}")

        # 5. 전체 결과를 JSON 파일로 저장
        output_dir = Path("../../logs/examples/langgraph")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / get_result_filename("browser_result")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)

        print(f"\n전체 결과가 {output_file}에 저장되었습니다.")

        print_section("테스트 완료")
        print("\n🌐 Browser Agent 핵심 기능:")
        print("  - 순차적 실행 보장 (version='v1')")
        print("  - Playwright MCP 도구 순차 호출")
        print("  - 각 작업 검증 후 진행")
        print("  - 실패 시 복구 메커니즘")

    except Exception as e:
        print(f"\n실행 중 오류 발생: {e!s}")
        import traceback
        traceback.print_exc()

    finally:
        try:
            log_capture.stop_capture()
            log_dir = Path("../../logs/examples/langgraph")
            log_dir.mkdir(parents=True, exist_ok=True)
            log_filename = log_dir / get_log_filename("browser_langgraph_log")
            log_capture.save_log(str(log_filename))
            print(f"\n실행 로그가 {log_filename}에 저장되었습니다.")
        except Exception as log_error:
            print(f"\n로그 저장 실패: {log_error}")


if __name__ == "__main__":
    asyncio.run(main())
