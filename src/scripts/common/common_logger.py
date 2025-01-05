"""
이 모듈은 PyQt 애플리케이션에서 발생하는 예외를 로그로 기록하는 기능을 제공합니다.
로깅은 콘솔 및 지정된 로그 파일에 기록되며, 애플리케이션이 비정상 종료될 때 예외 정보를 캡처합니다.

사용 방법:
    1. `setup_logger(name, log_file, level)` - 로거를 설정하고, 지정된 파일과 콘솔에 로그를 기록할 수 있게 합니다.
    2. `log_error(logger, message, exception=None)` - 에러 메시지를 로깅하고, 예외가 전달되면 예외 정보를 함께 기록합니다.
    3. `log_info(logger, message)` - 정보 메시지를 로깅합니다.
    4. `exception_hook(exctype, value, traceback)` - 처리되지 않은 예외를 캡처하여 로그로 기록하고, PyQt 애플리케이션을 종료합니다.

기본 사용 예시:
    1. 다른 `.py` 파일에서 이 모듈을 import하여 PyQt 애플리케이션에서 발생하는 예외를 기록할 수 있습니다.
    2. `sys.excepthook`을 `exception_hook`으로 설정하면 처리되지 않은 예외가 자동으로 로깅됩니다.

예시:
```
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from common_logger import exception_hook, setup_logger, log_error, about_to_quit

    def main():
        # 로거 설정
        logger = setup_logger("pyqt_logger", "./logs/pyqt_error.log", logging.DEBUG)

        # 예외 훅을 sys.excepthook에 설정
        sys.excepthook = exception_hook

        # PyQt 애플리케이션 시작
        app = QApplication(sys.argv)
        window = QMainWindow()
        window.setWindowTitle("PyQt Error Logging Example")
        window.resize(400, 300)
        window.show()

        # 애플리케이션 종료 직전 로그 설정
        app.aboutToQuit.connect(about_to_quit)

        # 실행
        sys.exit(app.exec_())

    if __name__ == "__main__":
        main()
"""

# Import Packages
import logging
import os
import sys
import traceback as tb
from functools import wraps


# Logger 생성 함수
def setup_logger(name, log_file, level=logging.INFO):
    """
    로거를 설정하는 함수입니다.
    지정된 파일과 콘솔에 로그를 기록하며, 로깅 수준을 설정할 수 있습니다.

    Args:
        name (str): 로거 이름.
        log_file (str): 로그 메시지를 기록할 파일 경로.
        level (int): 로깅 수준. 기본값은 logging.INFO.

    Returns:
        logging.Logger: 설정된 로거 인스턴스.
    """
    logger = logging.getLogger(name)

    # 로깅 수준 설정
    logger.setLevel(level)

    # 파일 핸들러 및 콘솔 핸들러 생성
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    file_handler = logging.FileHandler(log_file)
    stream_handler = logging.StreamHandler()

    # 로그 포맷 설정
    formatter = logging.Formatter("[%(asctime)s | %(levelname)s] - %(message)s")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # 핸들러 추가
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def log_error(logger, message, exception=None):
    """
    에러 메시지를 로깅하는 함수입니다.
    예외가 전달되면 예외의 세부 정보를 로그로 기록합니다.

    Args:
        logger (logging.Logger): 로깅 객체.
        message (str): 로깅할 메시지.
        exception (Exception, optional): 예외 객체. 기본값은 None.

    Returns:
        None
    """
    if exception:
        logger.error(f"{message} - Exception: {exception}", exc_info=True)
    else:
        logger.error(message)


def log_info(logger, message):
    """
    정보 메시지를 로깅하는 함수입니다.

    Args:
        logger (logging.Logger): 로깅 객체.
        message (str): 로깅할 메시지.

    Returns:
        None
    """
    logger.info(message)


def exception_hook(exctype, value, traceback):
    """
    PyQt 애플리케이션에서 예외가 발생할 때 로그를 남기는 커스텀 예외 훅입니다.
    애플리케이션이 비정상 종료되기 전에 예외와 트레이스백 정보를 기록합니다.

    Args:
        exctype (type): 발생한 예외의 타입.
        value (Exception): 발생한 예외 인스턴스.
        traceback (traceback): 예외 발생 시 호출 스택을 나타내는 객체.

    Returns:
        None

    사용방법:
        import common_logger
        sys.excepthook = common_logger.exception_hook
    """
    logger = setup_logger("pyqt_logger", "./logs/pyqt_error.log", logging.ERROR)

    # 예외 정보와 트레이스백을 로그로 기록
    log_error(logger, "Unhandled exception occurred", value)

    # 기본 excepthook을 호출하여 Python의 기본 예외 처리가 실행되도록 합니다.
    sys.__excepthook__(exctype, value, traceback)


def about_to_quit():
    """
    pyqt 애플리케이션 종료 직전에 로그를 기록합니다.
    """
    logger = setup_logger("quit_logger", "./logs/quit_error.log", logging.DEBUG)
    log_error(logger, "Application is about to quit")