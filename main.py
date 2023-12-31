# python internal packages
import os, sys
import ctypes

# python external packages
try:
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
except ImportError:
    os.system("pip install pyqt5 pyqt5-tools")
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt


# local packages
from Nsmc.src.scripts.common import create_file
from Nsmc.app import NEISMacro
from Nsmc.src.scripts.common import get_json
from Nsmc.src.scripts.common import convert


# Set Initial configuration
config = get_json.load_json_file("config.json")


def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    # sys.exit(1)


if __name__ == "__main__":
    # Convert .ui/.qrc files to .py files
    convert.convert_pyqt_files(config)
    create_file.create_files()

    # Application 구성하기
    app = QApplication(sys.argv)
    app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # Window에서 Icon 설정하기
    myappid = 'GangwonSWEET.FriendsNetwork.Python.ver1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Setup UI
    main_win = NEISMacro()
    main_win.setWindowTitle("  NEIS Macro by Gonyo (Released 2023. 12. 20.)")
    main_win.setWindowIcon(QIcon(":/img/fox.svg"))
    main_win.show()

    # Logger 연결하기
    sys._excepthook = sys.excepthook
    sys.excepthook = my_exception_hook
    sys.exit(app.exec_())

"""
pyuic5 ./Nsmc/src/views/main.ui -o ./Nsmc/src/views/main_ui.py
pyrcc5 ./Nsmc/src/views/main.qrc -o ./Nsmc/src/views/main_rc.py
pyinstaller -w -F --log-level=WARN --add-data="./Nsmc/src/data/*.xlsx;." --add-data="./Nsmc/src/img/*.png;." --icon=./Nsmc/src/views/fox.ico main.py
pyinstaller -w -F --add-data="./Nsmc/src/data/*.xlsx;." --add-data="./Nsmc/src/img/*.png;." --icon=./Nsmc/src/views/fox.ico main.py
"""
