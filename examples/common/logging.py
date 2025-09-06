"""공통 로깅 기능 모듈.

이 모듈은 examples 폴더 내의 모든 예제에서 사용할 수 있는
로깅 및 출력 캡처 기능을 제공합니다.
"""

import io
import sys

from datetime import datetime


class LogCapture:
    """콘솔 출력을 캡처하여 파일로 저장하는 클래스.

    사용법:
        log_capture = LogCapture()
        log_capture.start_capture()

        # 여기에 로깅할 코드들

        log_capture.stop_capture()
        log_capture.save_log("output.txt")
    """

    def __init__(self) -> None:
        self.log_buffer = io.StringIO()
        self.original_stdout = sys.stdout

    def start_capture(self) -> None:
        """출력 캡처 시작."""
        sys.stdout = self.TeeOutput(self.original_stdout, self.log_buffer)

    def stop_capture(self) -> None:
        """출력 캡처 종료."""
        sys.stdout = self.original_stdout

    def save_log(self, filename: str, title: str = "테스트 로그") -> None:
        """캡처된 로그를 파일로 저장."""
        log_content = self.log_buffer.getvalue()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"=== {title} ===\n")
            f.write(f"실행 시간: {timestamp}\n")
            f.write("=" * 60 + "\n\n")
            f.write(log_content)

    class TeeOutput:
        """stdout을 원본과 버퍼 양쪽에 출력하는 클래스."""
        def __init__(self, original, buffer) -> None:
            """생성자.

            Args:
                original: 원본 표준 출력 스트림 객체.
                buffer: 캡처 내용을 저장할 ``io.StringIO`` 버퍼.
            """
            self.original = original
            self.buffer = buffer

        def write(self, data) -> None:
            """데이터를 원본과 버퍼 모두에 기록합니다."""
            self.original.write(data)
            self.buffer.write(data)

        def flush(self) -> None:
            """양쪽 스트림의 버퍼를 비웁니다."""
            self.original.flush()
            self.buffer.flush()


def setup_logging_config():
    """로깅 설정을 위한 헬퍼 함수.

    Returns:
        dict: structlog 설정을 위한 설정 딕셔너리
    """
    import structlog

    return {
        'processors': [
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="ISO"),
            structlog.dev.ConsoleRenderer()
        ],
        'context_class': dict,
        'logger_factory': structlog.stdlib.LoggerFactory(),
        'cache_logger_on_first_use': True,
    }


def get_log_filename(prefix: str, suffix: str = "") -> str:
    """표준화된 로그 파일명 생성.

    Args:
        prefix: 파일명 접두사 (예: "analysis_langgraph")
        suffix: 파일명 접미사 (기본값: "")

    Returns:
        str: 생성된 파일명
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    suffix_str = f"_{suffix}" if suffix else ""
    return f"{prefix}{suffix_str}_{timestamp}.txt"


def get_result_filename(prefix: str, suffix: str = "") -> str:
    """표준화된 결과 파일명 생성.

    Args:
        prefix: 파일명 접두사 (예: "analysis_result")
        suffix: 파일명 접미사 (기본값: "")

    Returns:
        str: 생성된 파일명
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    suffix_str = f"_{suffix}" if suffix else ""
    return f"{prefix}{suffix_str}_{timestamp}.json"
