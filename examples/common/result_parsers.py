"""공통 결과 파싱 모듈.

이 모듈은 examples 폴더 내의 모든 예제에서 사용할 수 있는
결과 파싱 및 포맷팅 기능을 제공합니다.
"""

import json
import re

from typing import Any


def parse_json_result(raw_result: str) -> dict[str, Any] | None:
    """JSON 코드 블록을 파싱하여 딕셔너리로 반환.

    Args:
        raw_result: 원시 결과 문자열

    Returns:
        Optional[Dict[str, Any]]: 파싱된 JSON 데이터 또는 None
    """
    try:
        # JSON 블록 찾기 (```json ... ```)
        json_pattern = r'```json\s*(.*?)\s*```'
        json_match = re.search(json_pattern, raw_result, re.DOTALL)

        if json_match:
            json_str = json_match.group(1)
            return json.loads(json_str)
        return None

    except Exception as e:
        print(f"⚠️ JSON 파싱 실패: {e!s}")
        return None


def parse_analysis_result(raw_analysis: str) -> dict[str, Any] | None:
    """분석 결과를 구조화된 형태로 파싱.

    Args:
        raw_analysis: 원시 분석 결과

    Returns:
        Optional[Dict[str, Any]]: 파싱된 분석 데이터
    """
    analysis_data = parse_json_result(raw_analysis)

    if analysis_data:
        print("\n📊 구조화된 분석 결과:")
        print(f"  - 분석 상태: {analysis_data.get('analysis_status', 'N/A')}")
        print(f"  - 투자 신호: {analysis_data.get('investment_signal', 'N/A')}")
        print(f"  - 통합 점수: {analysis_data.get('integrated_score', 'N/A')}")
        print(f"  - 신뢰도: {analysis_data.get('confidence_level', 'N/A')}")

        # 차원별 분석
        if "dimension_analysis" in analysis_data:
            print("\n📈 차원별 분석:")
            dims = analysis_data["dimension_analysis"]
            for dim_name, dim_data in dims.items():
                if isinstance(dim_data, dict):
                    score = dim_data.get("score", "N/A")
                    print(f"  - {dim_name}: {score}")

        # 핵심 인사이트
        if "key_insights" in analysis_data:
            print("\n💡 핵심 인사이트:")
            insights = analysis_data["key_insights"]
            for insight in insights[:3]:  # 처음 3개만
                print(f"  • {insight}")

        # 리스크 요인
        if "risk_factors" in analysis_data:
            print("\n⚠️ 리스크 요인:")
            risks = analysis_data["risk_factors"]
            for risk in risks[:3]:  # 처음 3개만
                print(f"  • {risk}")

        return analysis_data
    print("\n📝 원시 분석 결과:")
    # 원시 텍스트 출력 (처음 500자만)
    print(raw_analysis[:500])
    if len(raw_analysis) > 500:
        print("... (더 많은 내용은 JSON 파일 참조)")
    return None


def parse_trading_result(raw_trading: str) -> dict[str, Any] | None:
    """거래 결과를 구조화된 형태로 파싱.

    Args:
        raw_trading: 원시 거래 결과

    Returns:
        Optional[Dict[str, Any]]: 파싱된 거래 데이터
    """
    trading_data = parse_json_result(raw_trading)

    if trading_data:
        print("\n🔄 구조화된 거래 결과:")
        print(f"  - 거래 상태: {trading_data.get('trading_status', 'N/A')}")
        print(f"  - 거래 종목: {trading_data.get('symbols_traded', 'N/A')}")
        print(f"  - 전략 타입: {trading_data.get('strategy_type', 'N/A')}")

        # 리스크 평가
        if "risk_assessment" in trading_data:
            risk = trading_data["risk_assessment"]
            print("\n⚠️ 리스크 평가:")
            print(f"  - 리스크 점수: {risk.get('risk_score', 'N/A')}")
            print(f"  - VaR 95%: {risk.get('var_95', 'N/A')}")
            print(f"  - 포지션 한도 확인: {risk.get('position_limit_check', 'N/A')}")

        # 실행된 주문
        if "orders_executed" in trading_data:
            orders = trading_data["orders_executed"]
            print("\n📋 실행된 주문:")
            for order in orders[:3]:  # 처음 3개만
                symbol = order.get('symbol', 'N/A')
                action = order.get('action', 'N/A')
                quantity = order.get('quantity', 'N/A')
                price = order.get('price', 'N/A')
                print(f"  • {symbol}: {action} {quantity}주 @ {price}")

        # Human 승인
        if "human_approval" in trading_data:
            approval = trading_data["human_approval"]
            print("\n👤 Human 승인:")
            print(f"  - 승인 필요: {approval.get('required', 'N/A')}")
            print(f"  - 상태: {approval.get('status', 'N/A')}")
            print(f"  - 사유: {approval.get('reason', 'N/A')}")

        return trading_data
    print("\n📝 원시 거래 결과:")
    # 원시 텍스트 출력 (처음 500자만)
    print(raw_trading[:500])
    if len(raw_trading) > 500:
        print("... (더 많은 내용은 JSON 파일 참조)")
    return None


def validate_analysis_quality(raw_analysis: str) -> dict[str, bool]:
    """분석 품질 검증.

    Args:
        raw_analysis: 원시 분석 결과

    Returns:
        Dict[str, bool]: 검증 결과
    """
    analysis_lower = raw_analysis.lower()

    # 지표 언급 여부 확인
    technical_indicators = ['rsi', 'macd', '이동평균', 'moving average']
    fundamental_indicators = ['per', 'pbr', 'roe', '재무']
    signals = ['strong_buy', 'buy', 'hold', 'sell', 'strong_sell',
               '매수', '매도', '보유', '중립']

    has_technical = any(ind in analysis_lower for ind in technical_indicators)
    has_fundamental = any(ind in analysis_lower for ind in fundamental_indicators)
    has_signal = any(sig in analysis_lower for sig in signals)

    return {
        'has_technical': has_technical,
        'has_fundamental': has_fundamental,
        'has_signal': has_signal
    }


def validate_data_collection_quality(raw_response: str) -> dict[str, bool]:
    """데이터 수집 품질 검증.

    Args:
        raw_response: 원시 응답

    Returns:
        Dict[str, bool]: 검증 결과
    """
    response_lower = raw_response.lower()

    # 수치 데이터 포함 여부
    has_numbers = any(char.isdigit() for char in raw_response)

    # 도구 이름 언급 여부
    tool_names = ['get_current_price', 'get_stock_info', 'get_news']
    has_tool_names = any(tool in response_lower for tool in tool_names)

    # 추측성 표현 검출
    speculation_words = ['아마도', '추정', '예상', '것 같', '일 것', '추측']
    has_speculation = any(word in raw_response for word in speculation_words)

    return {
        'has_numbers': has_numbers,
        'has_tool_names': has_tool_names,
        'has_speculation': has_speculation
    }


def print_quality_validation(agent_type: str, raw_content: str) -> None:
    """품질 검증 결과를 출력.

    Args:
        agent_type: Agent 타입
        raw_content: 검증할 원시 내용
    """
    if agent_type == "analysis":
        quality = validate_analysis_quality(raw_content)
        print("\n📝 분석 품질 검증:")
        print("  ✅ 기술적 지표 포함" if quality['has_technical'] else "  ⚠️ 기술적 지표 미포함")
        print("  ✅ 기본적 지표 포함" if quality['has_fundamental'] else "  ⚠️ 기본적 지표 미포함")
        print("  ✅ 명확한 투자 신호 제시" if quality['has_signal'] else "  ⚠️ 투자 신호가 불명확함")

    elif agent_type == "data_collector":
        quality = validate_data_collection_quality(raw_content)
        print("\n📝 응답 품질 검증:")
        print("  ✅ 수치 데이터 포함됨" if quality['has_numbers'] else "  ⚠️ 수치 데이터가 없음 - 실제 도구 호출 확인 필요")
        print("  ✅ 도구 이름 언급됨" if quality['has_tool_names'] else "  ⚠️ 도구 이름이 언급되지 않음")
        print("  ✅ 추측성 표현 없음" if not quality['has_speculation'] else "  ⚠️ 추측성 표현 발견 - 실제 데이터 사용 확인 필요")


def format_workflow_result(workflow_state: dict[str, Any]) -> str:
    """워크플로우 결과를 보기 좋게 포맷팅.

    Args:
        workflow_state: 워크플로우 상태 딕셔너리

    Returns:
        str: 포맷팅된 결과 문자열
    """
    lines = ["\n📊 **워크플로우 실행 결과**:"]
    lines.append("=" * 40)

    # 각 단계별 결과 확인
    steps = {
        "collected_data": ("데이터 수집", "📈"),
        "analysis_result": ("분석 실행", "📊"),
        "trading_result": ("거래 실행", "💹")
    }

    for key, (label, _icon) in steps.items():
        if workflow_state.get(key):
            lines.append(f"  ✅ {label}: 완료")
        else:
            lines.append(f"  ⏸️ {label}: 미실행")

    return "\n".join(lines)
