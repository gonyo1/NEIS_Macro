# python internal packages
import os
import sys
sys.path.append(os.path.dirname(__file__))


# local packages
from src.scripts import setup
from src.scripts.common.common_logger import exception_hook, setup_logger, log_error, about_to_quit


if __name__ == "__main__":
    # 로거 설정
    logger = setup_logger("pyqt_logger", "./logs/pyqt_error.log")
    sys.excepthook = exception_hook

    # App setup
    app = setup.setup_main_app()
    sys.exit(app.exec_())

    # Logger 연결
    pass
