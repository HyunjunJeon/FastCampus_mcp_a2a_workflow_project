#!/usr/bin/env python3
"""Supervisor Agent - A2A 프로토콜 호출 예제.

A2A 프로토콜을 통해 Supervisor Agent와 통신하는 예제입니다.
여러 하위 에이전트를 조율하여 복잡한 작업을 처리하는 전체 워크플로우를 보여줍니다.

실행 전제 조건:
1. Supervisor A2A 서버가 실행되어 있어야 함 (포트 8000)
2. 모든 하위 에이전트들이 사용 가능해야 함

>> 강의에서는 실제로 실행하지 않고 a2a-inspector 로 확인하겠습니다.
"""

# import asyncio
# import json
# import os
# import sys

# from pathlib import Path
# from typing import Any


# # 프로젝트 루트를 Python 경로에 추가
# project_root = Path(__file__).parent.parent.parent
# sys.path.insert(0, str(project_root))

# # 공통 모듈 import
# from examples.common.logging import (
#     LogCapture,
#     get_log_filename,
#     get_result_filename,
# )
# from src.a2a_integration.a2a_lg_client_utils import (
#     A2AClientManager,
# )
# from src.base.util import load_env_file


# # 환경 변수 로드
# load_env_file()


# def print_section(title: str) -> None:
#     """섹션 구분선 출력."""
#     print(f"\n{'='*60}")
#     print(f"  {title}")
#     print('='*60)


# async def orchestrate_workflow(
#     request: str,
#     context_id: str = "default",
#     is_debug: bool = False
# ) -> dict[str, Any]:
#     """A2A를 통한 Supervisor Agent 워크플로우 실행.

#     Args:
#         request: 사용자 요청
#         context_id: 컨텍스트 ID
#         is_debug: 디버그 모드 플래그

#     Returns:
#         실행 결과를 포함한 딕셔너리
#     """
#     # 환경에 따른 supervisor URL 결정
#     is_docker = os.getenv('IS_DOCKER', 'false').lower() == 'true'
#     supervisor_url = 'http://supervisor-agent:8000' if is_docker else 'http://localhost:8000'

#     try:
#         # Supervisor Agent용 A2A 클라이언트 생성
#         print("\n[정보] A2A를 통해 Supervisor Agent에 연결 중...")
#         print(f"       URL: {supervisor_url}")

#         client_manager = A2AClientManager(
#             base_url=supervisor_url,
#             streaming=False,
#             retry_delay=5.0
#         )
#         client = await client_manager.initialize()

#         # 입력 데이터 준비
#         input_data = {
#             'messages': [{'role': 'user', 'content': request}]
#         }

#         # A2A를 통한 실행
#         print("[정보] A2A 프로토콜을 통해 워크플로우 실행 중...")
#         print(f"   요청: {request}...")

#         # from a2a.types import Part, DataPart
#         # 최신 API: send_parts 사용 예시
#         result = await client.send_parts(parts=[Part(root=DataPart(data=input_data))])

#         # TODO: 여기서 중간중간 결과가 더 나올 수 있도록 A2A Client 에서 수정 필요.
#         # 결과 처리
#         if result:
#             # 텍스트 내용 추출
#             text_content = result.get('text_content', '')

#             # 데이터 내용 추출
#             data_content = result.get('data_content')
#             if not data_content and 'data_parts' in result:
#                 # data_parts에서 가져오기 시도
#                 data_parts = result.get('data_parts', [])
#                 if data_parts and isinstance(data_parts[-1], dict):
#                     data_content = data_parts[-1]

#             # 오류 확인
#             if result.get('error') or result.get('error_message'):
#                 return {
#                     "success": False,
#                     "request": request,
#                     "error": result.get('error') or result.get('error_message'),
#                     "context_id": context_id
#                 }

#             # 에이전트 실행 정보 추출
#             agents_executed = []
#             if data_content and isinstance(data_content, dict):
#                 workflow_summary = data_content.get('workflow_summary', {})
#                 agents_executed = workflow_summary.get('agents_executed', [])

#             return {
#                 "success": True,
#                 "request": request,
#                 "response": text_content,
#                 "agents_executed": agents_executed,
#                 "data_content": data_content,
#                 "context_id": context_id
#             }

#         return {
#             "success": False,
#             "request": request,
#             "error": "A2A 에이전트로부터 결과 없음",
#             "context_id": context_id
#         }

#     except Exception as e:
#         print(f"[오류] A2A 워크플로우 실행 실패: {e!s}")
#         return {
#             "success": False,
#             "request": request,
#             "error": str(e),
#             "context_id": context_id
#         }
#     finally:
#         # 클라이언트 연결 종료
#         if 'client_manager' in locals():
#             await client_manager.close()


# async def test_planning_workflow():
#     """계획 기반 조율 워크플로우 테스트.

#     Planner Agent 중심의 작업 계획 수립과 실행을 테스트합니다.
#     """
#     print_section("테스트 1: 계획 기반 조율 워크플로우")

#     request = """
#     블로그 웹사이트 구축을 위한 상세한 5단계 계획을 수립해주세요:
#     - 사용자 인증 시스템
#     - 포스트 작성 및 편집 기능
#     - 댓글 시스템
#     - 검색 기능
#     각 단계별 구체적인 작업과 의존성을 명시하고 기술 스택을 제안해주세요.
#     """

#     result = await orchestrate_workflow(
#         request=request,
#         context_id="test_planning",
#         is_debug=False
#     )

#     # 결과 출력
#     if result.get("success"):
#         print("[성공] 계획 기반 워크플로우 완료!")
#         print(f"   응답 미리보기: {result.get('response', '')[:300]}...")
#         print(f"   실행된 에이전트: {result.get('agents_executed', [])}")
#     else:
#         print(f"[실패] 오류: {result.get('error')}")

#     return result


# async def test_knowledge_workflow():
#     """지식 관리 통합 워크플로우 테스트.

#     Knowledge Agent 중심의 정보 저장과 검색을 테스트합니다.
#     """
#     print_section("테스트 2: 지식 관리 통합 워크플로우")

#     request = """
#     다음 프로젝트 정보를 저장하고 검증해주세요:
#     - 프로젝트명: FastCampus Multi-Agent System
#     - 기술 스택: Python, LangGraph, MCP, Docker
#     - 팀 구성: Alice (백엔드), Bob (프론트엔드), Charlie (DevOps)
#     - 스프린트 목표: 월말까지 MVP 완성
#     - 핵심 기능: 에이전트 조율, 메모리 지속성, 웹 자동화

#     저장 후 "프로젝트 기술 스택"을 검색하여 정보가 올바르게 저장되었는지 확인해주세요.
#     """

#     result = await orchestrate_workflow(
#         request=request,
#         context_id="test_knowledge",
#         is_debug=False
#     )

#     # 결과 출력
#     if result.get("success"):
#         print("[성공] 지식 관리 워크플로우 완료!")
#         print(f"   응답 미리보기: {result.get('response', '')[:500]}...")
#         print(f"   실행된 에이전트: {result.get('agents_executed', [])}")
#     else:
#         print(f"[실패] 오류: {result.get('error')}")

#     return result


# async def test_data_analysis_pipeline():
#     """데이터 분석 파이프라인 워크플로우 테스트.

#     Executor Agent 중심의 데이터 처리와 분석을 테스트합니다.
#     """
#     print_section("테스트 3: 데이터 분석 파이프라인")

#     request = """
#     완전한 데이터 분석 파이프라인을 구축하고 실행해주세요:
#     1. 지난 30일간의 샘플 판매 데이터 생성 (100개 거래)
#     2. 주요 지표 계산: 총 수익, 평균 주문 가치, 최고 판매일
#     3. 시각화 생성: 판매 트렌드 차트, 일별 수익 막대 차트
#     4. 분석 결과와 인사이트를 메모리에 저장
#     5. 경영진을 위한 요약 보고서 생성

#     Python pandas를 사용하여 데이터 처리를 수행하고 명확한 인사이트를 제공해주세요.
#     해당 인사이트를 Notion에 저장해주세요.
#     """

#     result = await orchestrate_workflow(
#         request=request,
#         context_id="test_data_pipeline",
#         is_debug=False
#     )

#     if result.get("success"):
#         print("[성공] 데이터 분석 파이프라인 완료!")
#         print(f"   파이프라인 결과: {result.get('response', '')[:500]}...")
#         print(f"   실행된 에이전트: {result.get('agents_executed', [])}")
#     else:
#         print(f"[실패] 오류: {result.get('error')}")

#     return result


# async def test_web_research_integration():
#     """웹 리서치 통합 워크플로우 테스트.

#     Browser Agent 중심의 웹 정보 수집과 분석을 테스트합니다.
#     """
#     print_section("테스트 4: 웹 리서치 통합 워크플로우")

#     request = """
#     Python asyncio에 대한 포괄적인 리서치를 수행해주세요:
#     1. Python 공식 문서에서 asyncio 정보 수집
#     2. 핵심 개념과 주요 기능 추출
#     3. async/await 패턴의 코드 예제 정리
#     4. Python 비동기 프로그래밍 모범 사례 요약
#     5. 구조화된 asyncio 학습 가이드 문서 작성

#     전체 리서치 프로세스를 체계적으로 진행하고 실용적인 가이드를 제공해주세요.
#     """

#     result = await orchestrate_workflow(
#         request=request,
#         context_id="test_web_research",
#         is_debug=False
#     )

#     # 결과 출력
#     if result.get("success"):
#         print("[성공] 웹 리서치 워크플로우 완료!")
#         print(f"   리서치 결과: {result.get('response', '')[:500]}...")
#         print(f"   실행된 에이전트: {result.get('agents_executed', [])}")
#     else:
#         print(f"[실패] 오류: {result.get('error')}")

#     return result


# async def test_full_integration_workflow():
#     """전체 통합 워크플로우 테스트.

#     모든 에이전트가 협력하는 복합적인 업무 처리를 테스트합니다.
#     """
#     print_section("테스트 5: 전체 통합 워크플로우")

#     request = """
#     REST API 기반 할일 관리 애플리케이션 개발 프로젝트를 완전히 진행해주세요:

#     1. [Planner] 할일 관리 REST API 구축을 위한 상세한 계획 수립
#     2. [Browser] FastAPI 문서에서 모범 사례와 인증 방법 리서치
#     3. [Executor] 사용자 인증이 포함된 기본 CRUD API Python 코드 작성
#     4. [Knowledge] API 엔드포인트 문서와 사용 예제 저장
#     5. [Executor] API 엔드포인트를 위한 단위 테스트 생성
#     6. [Knowledge] 향후 참조를 위한 프로젝트 구조와 설정 지침 저장

#     모든 에이전트를 조율하여 이 워크플로우를 완료하고 포괄적인 최종 보고서를 제공하고 Notion에 저장해주세요.
#     """

#     result = await orchestrate_workflow(
#         request=request,
#         context_id="test_full_integration",
#         is_debug=False
#     )

#     # 결과 출력
#     if result.get("success"):
#         print("[성공] 전체 통합 워크플로우 완료!")
#         print(f"   통합 결과: {result.get('response', '')[:600]}...")
#         print(f"   실행된 에이전트: {result.get('agents_executed', [])}")
#     else:
#         print(f"[실패] 오류: {result.get('error')}")

#     return result


# async def main() -> None:
#     """메인 실행 함수."""
#     # 로그 캡처 시작
#     log_capture = LogCapture()
#     log_capture.start_capture()

#     try:
#         print_section("Supervisor Agent - A2A 프로토콜 예제")
#         print("A2A 프로토콜을 통해 Supervisor Agent를 사용하여 복잡한 워크플로우를 조율합니다.")
#         print("\n[중요] Supervisor Agent가 포트 8000에서 실행 중인지 확인하세요")
#         print("       실행: python src/agents/supervisor/supervisor_agent_a2a.py")

#         # 1. MCP 서버 상태 확인 (선택사항)
#         # print("\n[정보] MCP 서버 상태 확인...")
#         # await check_mcp_servers("all")

#         # 2. 테스트 케이스 실행
#         all_results = []

#         # # 테스트 1: 계획 기반 워크플로우
#         # result1 = await test_planning_workflow()
#         # all_results.append(result1)
#         # await asyncio.sleep(2)  # 서버 과부하 방지

#         # # 테스트 2: 지식 관리 워크플로우
#         # result2 = await test_knowledge_workflow()
#         # all_results.append(result2)
#         # await asyncio.sleep(2)

#         # # 테스트 3: 데이터 분석 파이프라인
#         # result3 = await test_data_analysis_pipeline()
#         # all_results.append(result3)
#         # await asyncio.sleep(2)

#         # # 테스트 4: 웹 리서치 통합
#         # result4 = await test_web_research_integration()
#         # all_results.append(result4)
#         # await asyncio.sleep(2)

#         # 테스트 5: 전체 통합 워크플로우
#         result5 = await test_full_integration_workflow()
#         all_results.append(result5)

#         print_section("테스트 완료")

#     except Exception as e:
#         print(f"\n❌ 실행 중 오류 발생: {e!s}")
#         import traceback
#         traceback.print_exc()


# if __name__ == "__main__":
#     asyncio.run(main())
