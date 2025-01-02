# python internal packages
import os, sys
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

# Set Initial configuration
config = common_json.load_json_file("config.json")


if __name__ == "__main__":
    # Setup QApplication
    app = QApplication(sys.argv)
    app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)

    for font in glob(common_path.get_join_path("src/views/font/*.ttf")):
        QFontDatabase.addApplicationFont(font)

    # Window에서 Icon 설정하기
    myappid = 'GangwonSWEET.FriendsNetwork.Python.ver1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Setup UI
    main_win = NEISMacro()
    main_win.show()

    # Logger 연결하기
    sys.exit(app.exec_())

"""
pyuic5 ./Nsmc/src/views/main.ui -o ./Nsmc/src/views/main_ui.py
pyrcc5 ./Nsmc/src/views/main.qrc -o ./Nsmc/src/views/main_rc.py
pyinstaller -w -F --log-level=WARN --add-data="./Nsmc/src/data/*.xlsx;." --add-data="./Nsmc/src/img/*.png;." --icon=./Nsmc/src/views/assets/fox.ico main.py
pyinstaller -w -F --add-data="./Nsmc/src/data/*.xlsx;." --add-data="./Nsmc/src/img/*.png;." --icon=./Nsmc/src/views/fox.ico main.py
"""
