#!/usr/bin/env python3
"""Browser Agent - A2A 프로토콜 호출 예제.

A2A 프로토콜을 통해 Browser Agent와 통신하는 예제입니다.
Agent는 별도 프로세스로 실행되며, A2A 클라이언트를 통해 원격 호출합니다.

실행 전제 조건:
1. Playwright MCP 서버가 실행 중이어야 함
2. Browser A2A 서버가 실행되어 있어야 함
"""

import asyncio
import json
import sys
import time

from datetime import datetime
from pathlib import Path
from typing import Any

from a2a.types import DataPart

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.a2a_integration.a2a_lg_client_utils import A2AClientManager


def print_section(title: str) -> None:
    """섹션 구분선 출력."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


# ============== 통합 테스트 기능 ==============

class IntegrationTestResult:
    """통합 테스트 결과 저장 클래스."""
    def __init__(self) -> None:
        self.test_cases: list[dict[str, Any]] = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.start_time = None
        self.end_time = None

    def add_test_result(self, test_name: str, success: bool, details: dict[str, Any]) -> None:
        """테스트 결과 추가."""
        self.test_cases.append({
            "test_name": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        self.total_tests += 1
        if success:
            self.passed_tests += 1
        else:
            self.failed_tests += 1

    def generate_report(self) -> str:
        """테스트 보고서 생성."""
        duration = (self.end_time - self.start_time).total_seconds() if self.end_time and self.start_time else 0

        report = f"""
🧪 Browser A2A 통합 테스트 보고서
{'='*50}
📊 테스트 결과: {self.passed_tests}/{self.total_tests} 성공
⏱️  실행 시간: {duration:.2f}초
📅 실행 시간: {self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else 'N/A'}

📋 상세 결과:
"""
        for test_case in self.test_cases:
            status = "✅ 성공" if test_case["success"] else "❌ 실패"
            report += f"   {status} - {test_case['test_name']}\n"
            if not test_case["success"] and "error" in test_case["details"]:
                report += f"     오류: {test_case['details']['error']}\n"

        return report


def validate_a2a_output(response: dict[str, Any], expected_agent_type: str = "browser") -> dict[str, Any]:
    """A2AOutput 표준 형식 검증."""
    validation_result = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "found_fields": []
    }

    # 필수 필드 확인
    required_fields = ["agent_type", "status"]
    for field in required_fields:
        if field in response:
            validation_result["found_fields"].append(field)
        else:
            validation_result["valid"] = False
            validation_result["errors"].append(f"필수 필드 '{field}' 누락")

    # agent_type 검증
    if "agent_type" in response:
        actual_agent_type = response.get("agent_type")
        if actual_agent_type != expected_agent_type:
            validation_result["warnings"].append(
                f"예상 agent_type: '{expected_agent_type}', 실제: '{actual_agent_type}'"
            )

    # status 필드 검증
    valid_statuses = ["working", "completed", "failed", "input_required"]
    if "status" in response:
        status = response.get("status")
        if status not in valid_statuses:
            validation_result["warnings"].append(f"알 수 없는 status 값: '{status}'")

    # 선택적 필드 확인
    optional_fields = ["text_content", "data_content", "final", "stream_event"]
    for field in optional_fields:
        if field in response:
            validation_result["found_fields"].append(field)

    return validation_result


async def test_streaming_vs_polling(
    url: str,
    task: str,
    browser_url: str = "http://localhost:8005"
) -> dict[str, Any]:
    """스트리밍 vs 폴링 모드 비교 테스트."""
    input_data = {
        "messages": [{"role": "user", "content": task}],
        "target_url": url
    }

    results = {"streaming": None, "polling": None, "comparison": {}}

    print("  🔄 스트리밍 모드 테스트...")
    start_time = time.time()
    try:
        async with A2AClientManager(
            base_url=browser_url,
            streaming=True,
            retry_delay=2.0
        ) as client_manager:
            streaming_result = await client_manager.send_data_with_full_messages(input_data)

        streaming_duration = time.time() - start_time
        results["streaming"] = {
            "success": True,
            "duration": streaming_duration,
            "result": streaming_result if isinstance(streaming_result, list) else [streaming_result]
        }
        print(f"    ✅ 스트리밍 완료 ({streaming_duration:.2f}초)")

    except Exception as e:
        results["streaming"] = {
            "success": False,
            "duration": time.time() - start_time,
            "error": str(e)
        }
        print(f"    ❌ 스트리밍 실패: {e!s}")

    print("  🔄 폴링 모드 테스트...")
    start_time = time.time()
    try:
        async with A2AClientManager(
            base_url=browser_url,
            streaming=False
        ) as client_manager:
            polling_result = await client_manager.send_data_with_full_messages(input_data)

        polling_duration = time.time() - start_time
        results["polling"] = {
            "success": True,
            "duration": polling_duration,
            "result": polling_result if isinstance(polling_result, list) else [polling_result]
        }
        print(f"    ✅ 폴링 완료 ({polling_duration:.2f}초)")

    except Exception as e:
        results["polling"] = {
            "success": False,
            "duration": time.time() - start_time,
            "error": str(e)
        }
        print(f"    ❌ 폴링 실패: {e!s}")

    # 결과 비교
    if results["streaming"]["success"] and results["polling"]["success"]:
        streaming_final = results["streaming"]["result"][-1] if results["streaming"]["result"] else {}
        polling_final = results["polling"]["result"][-1] if results["polling"]["result"] else {}

        results["comparison"] = {
            "both_successful": True,
            "speed_difference": results["polling"]["duration"] - results["streaming"]["duration"],
            "content_consistency": streaming_final.get("status") == polling_final.get("status")
        }
        print(f"    📊 성능 차이: 스트리밍이 {results['comparison']['speed_difference']:.2f}초 더 {'빠름' if results['comparison']['speed_difference'] > 0 else '느림'}")
        print(f"    🔍 결과 일관성: {'일관됨' if results['comparison']['content_consistency'] else '불일치'}")

    return results


async def run_a2a_interface_tests(
    url: str,
    task: str,
    browser_url: str = "http://localhost:8005"
) -> dict[str, Any]:
    """A2A 인터페이스 핵심 메서드 테스트."""
    test_results = {
        "execute_for_a2a": {"tested": False, "success": False},
        "format_stream_event": {"tested": False, "success": False},
        "extract_final_output": {"tested": False, "success": False},
        "a2a_output_format": {"tested": False, "success": False}
    }

    input_data = {
        "messages": [{"role": "user", "content": task}],
        "target_url": url
    }

    print("  🧪 A2A 인터페이스 메서드 테스트...")

    try:
        # execute_for_a2a 간접 테스트 (A2A 호출을 통해)
        async with A2AClientManager(base_url=browser_url) as client_manager:
            response = await client_manager.send_data_with_full_messages(input_data)

        test_results["execute_for_a2a"]["tested"] = True
        test_results["execute_for_a2a"]["success"] = response is not None

        # A2AOutput 형식 검증
        if isinstance(response, list) and response:
            final_response = response[-1]
        else:
            final_response = response

        validation = validate_a2a_output(final_response, "browser")
        test_results["a2a_output_format"]["tested"] = True
        test_results["a2a_output_format"]["success"] = validation["valid"]
        test_results["a2a_output_format"]["details"] = validation

        # format_stream_event 검증 (스트리밍 응답에서)
        if isinstance(response, list) and len(response) > 1:
            test_results["format_stream_event"]["tested"] = True
            test_results["format_stream_event"]["success"] = True
            print("    ✅ format_stream_event: 스트리밍 이벤트 감지됨")

        # extract_final_output 검증 (최종 결과 추출)
        if final_response and "status" in final_response:
            test_results["extract_final_output"]["tested"] = True
            test_results["extract_final_output"]["success"] = final_response.get("status") in ["completed", "failed"]
            print(f"    ✅ extract_final_output: 최종 상태 = {final_response.get('status')}")

        print("    ✅ A2A 인터페이스 테스트 완료")

    except Exception as e:
        print(f"    ❌ A2A 인터페이스 테스트 실패: {e!s}")
        for test_name in test_results:
            if not test_results[test_name]["tested"]:
                test_results[test_name]["error"] = str(e)

    return test_results


async def check_a2a_server() -> bool:
    """A2A 서버 상태 확인."""
    import httpx

    # Agent Card 엔드포인트로 상태 확인
    server_url = "http://localhost:8005/.well-known/agent-card.json"

    print_section("A2A 서버 상태 확인")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(server_url, timeout=5.0)
            if response.status_code == 200:
                agent_card = response.json()
                print("✅ Browser A2A 서버: 정상 작동")
                print(f"   Agent: {agent_card.get('name', 'Unknown')}")
                print(f"   설명: {agent_card.get('description', 'No description')}")
                print(f"   스트리밍 지원: {agent_card.get('capabilities', {}).get('streaming', False)}")
                return True
            print(f"⚠️ Browser A2A 서버: 응답 이상 (status: {response.status_code})")
            return False
        except Exception as e:
            print("❌ Browser A2A 서버: 연결 실패")
            print(f"   오류: {str(e)[:100]}")
            print("\n💡 해결 방법:")
            print("   1. Browser A2A 서버 실행:")
            print("      python -m src.agents.browser.browser_use_agent_a2a")
            print("   2. 서버가 포트 8005에서 실행 중인지 확인")
            return False


async def call_browser_via_a2a(
    url: str,
    task: str
) -> dict[str, Any]:
    """A2A 프로토콜을 통해 Browser Agent 호출."""
    # Browser A2A 서버 URL
    browser_url = "http://localhost:8005"

    # 입력 데이터 준비
    input_data = {
        "messages": [{"role": "user", "content": task}],
        "target_url": url
    }

    print("\n📤 요청 전송:")
    print(f"   - URL: {url}")
    print(f"   - 작업: {task}")

    # 폴링 모드 사용
    async with A2AClientManager(base_url=browser_url) as client_manager:
        try:
            response_data = await client_manager.send_parts(parts=[DataPart(data=input_data)])

            if isinstance(response_data, list) and response_data:
                return response_data[-1]
            return response_data

        except Exception as e:
            print(f"❌ A2A 호출 실패: {e!s}")
            raise


def format_browser_result(result: dict[str, Any]) -> None:
    """브라우저 작업 결과 포맷팅 및 출력."""
    if "data_parts" in result:
        data_parts = result.get("data_parts", [])
        if data_parts:
            main_result = data_parts[0] if isinstance(data_parts, list) else data_parts
        else:
            print("❌ 브라우저 작업 실패: DataPart가 없습니다.")
            return
    else:
        main_result = result

    if not main_result.get("success", False):
        print(f"❌ 브라우저 작업 실패: {main_result.get('error', 'Unknown error')}")
        return

    print("✅ 브라우저 작업 성공!")

    # 수집된 데이터 파싱
    browser_data = main_result.get("browser_data", {})

    # 처리된 URL
    if "final_url" in browser_data:
        print(f"\n📌 최종 URL: {browser_data['final_url']}")

    # 도구 호출 통계
    if "tool_calls_made" in browser_data:
        print(f"🔧 도구 호출 횟수: {browser_data['tool_calls_made']}")

    # 추출된 데이터
    if "extracted_data" in browser_data:
        print("\n📝 추출된 데이터:")
        print("-" * 50)
        for data_item in browser_data["extracted_data"][:5]:  # 처음 5개만
            data_type = data_item.get("data_type", "unknown")
            content = data_item.get("content", "")
            print(f"  [{data_type}] {content[:100]}...")

    # 스크린샷
    if "screenshots" in browser_data:
        print(f"\n📸 스크린샷 수: {len(browser_data['screenshots'])}")

    # 메타데이터
    print("\n📊 메타데이터:")
    print(f"  - 워크플로우 상태: {main_result.get('workflow_status', 'N/A')}")
    print(f"  - Agent 타입: {main_result.get('agent_type', 'N/A')}")
    print(f"  - 성공 여부: {main_result.get('success', False)}")


async def main() -> None:
    """메인 실행 함수."""
    print_section("Browser Agent - A2A 프로토콜 예제")
    print("A2A 프로토콜을 통해 원격 Browser Agent와 통신합니다.")

    # 1. A2A 서버 상태 확인
    if not await check_a2a_server():
        print("\n⚠️ A2A 서버가 실행되지 않았습니다.")
        print("위의 해결 방법을 따라 서버를 먼저 실행해주세요.")
        return None

    # 2. 통합 테스트 초기화
    test_result = IntegrationTestResult()
    test_result.start_time = datetime.now()

    # 3. 테스트 케이스 준비
    print_section("브라우저 자동화 요청 준비")

    test_cases: list[dict[str, Any]] = [
        # {
        #     "name": "웹 페이지 탐색 및 데이터 추출",
        #     "url": "https://example.com",
        #     "task": "페이지에 접속하여 제목과 본문을 추출해주세요",
        #     "test_type": "standard"
        # },
        # {
        #     "name": "스트리밍 vs 폴링 모드 비교 테스트",
        #     "url": "https://example.com",
        #     "task": "페이지 정보를 수집해주세요",
        #     "test_type": "streaming_vs_polling"
        # },
        # {
        #     "name": "A2A 인터페이스 메서드 검증 테스트",
        #     "url": "https://example.com",
        #     "task": "페이지 타이틀을 가져와주세요",
        #     "test_type": "a2a_interface"
        # },
        # {
        #     "name": "A2AOutput 표준 형식 검증 테스트",
        #     "url": "https://example.com",
        #     "task": "페이지 메타 정보를 수집해주세요",
        #     "test_type": "output_validation"
        # },
        {
            "name": "복잡한 워크플로우 테스트",
            "url": "https://www.google.com",
            "task": "Google에서 'LangGraph'를 검색하고 첫 번째 결과를 확인해주세요",
            "test_type": "complex_workflow"
        }
    ]

    # 4. 각 테스트 케이스 실행
    for i, test_case in enumerate(test_cases, 1):
        print_section(f"테스트 {i}: {test_case['name']}")
        test_type = test_case.get("test_type", "standard")

        try:
            if test_type in {"standard", "complex_workflow"}:
                # 기본 브라우저 작업 테스트
                print("\n🔄 A2A 프로토콜을 통해 브라우저 작업 중...")
                result = await call_browser_via_a2a(
                    url=test_case["url"],
                    task=test_case["task"]
                )

                # 결과 출력
                print_section("작업 결과")
                format_browser_result(result)

                # 테스트 성공 기록
                test_result.add_test_result(
                    test_case["name"],
                    True,
                    {"result_type": test_type, "status": "completed"}
                )

            elif test_type == "streaming_vs_polling":
                # 스트리밍 vs 폴링 비교 테스트
                comparison_result = await test_streaming_vs_polling(
                    url=test_case["url"],
                    task=test_case["task"]
                )

                # 테스트 결과 기록
                both_successful = (
                    comparison_result["streaming"] and comparison_result["streaming"]["success"] and
                    comparison_result["polling"] and comparison_result["polling"]["success"]
                )
                test_result.add_test_result(
                    test_case["name"],
                    both_successful,
                    comparison_result
                )

                result = comparison_result  # 저장을 위해

            elif test_type == "a2a_interface":
                # A2A 인터페이스 메서드 검증 테스트
                interface_test_result = await run_a2a_interface_tests(
                    url=test_case["url"],
                    task=test_case["task"]
                )

                # 모든 핵심 메서드가 성공적으로 테스트되었는지 확인
                all_tests_passed = all(
                    test_info.get("success", False) or not test_info.get("tested", False)
                    for test_info in interface_test_result.values()
                )

                test_result.add_test_result(
                    test_case["name"],
                    all_tests_passed,
                    interface_test_result
                )

                result = interface_test_result  # 저장을 위해

            elif test_type == "output_validation":
                # A2AOutput 표준 형식 검증 테스트
                result = await call_browser_via_a2a(
                    url=test_case["url"],
                    task=test_case["task"]
                )

                # A2AOutput 형식 검증
                if isinstance(result, list) and result:
                    final_result = result[-1]
                else:
                    final_result = result

                validation = validate_a2a_output(final_result, "browser")

                print("  📋 A2AOutput 검증 결과:")
                print(f"    - 유효성: {'✅ 통과' if validation['valid'] else '❌ 실패'}")
                print(f"    - 발견된 필드: {', '.join(validation['found_fields'])}")
                if validation['errors']:
                    print(f"    - 오류: {', '.join(validation['errors'])}")
                if validation['warnings']:
                    print(f"    - 경고: {', '.join(validation['warnings'])}")

                test_result.add_test_result(
                    test_case["name"],
                    validation['valid'],
                    validation
                )

            # JSON 파일로 저장
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_dir = Path("logs/examples/a2a")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"browser_a2a_{test_type}_result_{timestamp}.json"

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            print(f"\n💾 전체 결과가 {output_file}에 저장되었습니다.")

        except Exception as e:
            print(f"\n❌ 테스트 실행 중 오류 발생: {e!s}")
            import traceback
            traceback.print_exc()

            # 실패한 테스트 기록
            test_result.add_test_result(
                test_case["name"],
                False,
                {"error": str(e), "traceback": traceback.format_exc()}
            )

    # 5. 통합 테스트 보고서 생성
    test_result.end_time = datetime.now()

    print_section("통합 테스트 보고서")
    report = test_result.generate_report()
    print(report)

    # 6. 보고서 파일 저장
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = Path("logs/examples/a2a")
    output_dir.mkdir(parents=True, exist_ok=True)
    report_file = output_dir / f"browser_integration_test_report_{timestamp}.txt"

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n📄 통합 테스트 보고서가 {report_file}에 저장되었습니다.")

    print_section("Browser A2A 통합 테스트 완료")
    print("✨ 모든 통합 테스트가 완료되었습니다.")
    print(f"🎯 테스트 성공률: {test_result.passed_tests}/{test_result.total_tests} ({test_result.passed_tests/test_result.total_tests*100:.1f}%)")

    # 테스트 실패 시 종료 코드 반환
    return test_result.failed_tests == 0


if __name__ == "__main__":
    # 이벤트 루프 실행
    asyncio.run(main())
