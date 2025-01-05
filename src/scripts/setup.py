import os
import sys
import ctypes
from glob import glob


# python external packages
try:
    from PyQt5.QtGui import QIcon, QFontDatabase
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt, QCoreApplication
except ImportError:
    os.system("pip install pyqt5 pyqt5-tools")
    from PyQt5.QtGui import QIcon, QFontDatabase
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt, QCoreApplication


# local packages
# from src.scripts.common import create_file
from src.scripts.common import common_json
from src.scripts.common import common_path
from src.scripts.common import common_convert
from src.scripts.gui.app import NEISMacro


def setup_main_app():
    def set_display_mode():
        # Make QtApplication fit to user screen size
        """
        Qt 환경 변수 설명:

        QT_AUTO_SCREEN_SCALE_FACTOR:
        디스플레이의 DPI(인치당 도트 수)에 따라 화면 스케일링을 자동으로 활성화하거나 비활성화합니다.
        "1"로 설정하면 Qt가 DPI를 기준으로 적절한 스케일링 비율을 자동 계산하여 적용합니다.

        QT_ENABLE_HIGHDPI_SCALING:
        Qt 애플리케이션에서 고해상도(High DPI) 지원을 활성화하거나 비활성화합니다.
        "1"로 설정하면 고해상도 디스플레이에서 더 나은 UI 렌더링을 보장하는 High DPI 스케일링을 활성화합니다.

        QT_SCALE_FACTOR:
        애플리케이션 UI의 스케일링 비율을 수동으로 지정합니다.
        "1"로 설정하면 추가적인 스케일링 없이 기본 크기(100%)로 유지됩니다.
        "1.5", "2.0" 등의 값을 사용하면 특정 배율로 UI 크기를 강제로 조정할 수 있습니다.
        """
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
        os.environ["QT_SCALE_FACTOR"] = "1"

    def set_app_object():
        # Setup QApplication
        app = QApplication(sys.argv)
        app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

        # Setup UI
        main_win = NEISMacro()
        main_win.show()

        return app

    def set_font_cache():
        # PyQT 에 font cache 등록
        for font in glob(common_path.get_join_path("src/views/font/*.ttf")):
            QFontDatabase.addApplicationFont(font)

    def set_process_id():
        # Window app id 설정
        myappid = 'GangwonSWEET.FriendsNetwork.Python.ver2'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Setup display mode
    set_display_mode()

    # Setup application
    app = set_app_object()
    set_font_cache()
    set_process_id()

    return app
