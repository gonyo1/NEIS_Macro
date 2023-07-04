# pip install pyqt5 pywin32 pillow pyinstaller tinyaes
import os.path
import sys
from glob import glob
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget
from Nsmc.src.view.main_ui import Ui_MainApp as mp
# from AutoSigner.sub_ui import Ui_Form as sp
import Nsmc.src.macro as macro
import Nsmc.src.view.main_rc

AUTO_DICT = dict()


class MainWindow(QMainWindow, mp):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self.setWindowTitle("  NEIS Macro by Gonyo (Released 2023.7.5.)")
        self.setWindowIcon(QIcon(":/img/fox.svg"))

        self.set_signal()


    def set_signal(self):
        self.Form_downbar_get.clicked.connect(macro.get_form_file)
        self.Tutorial_Push.clicked.connect(macro.show_how_to_use)
        self.Macro_push_1.clicked.connect(lambda state, index=1: macro.run_macro(index))
        self.Macro_push_2.clicked.connect(lambda state, index=2: macro.run_macro(index))
        self.Macro_push_3.clicked.connect(lambda state, index=3: macro.run_macro(index))
        self.Macro_push_4.clicked.connect(lambda state, index=4: macro.run_macro(index))
        self.Macro_push_5.clicked.connect(lambda state, index=5: macro.run_macro(index))
        self.Macro_push_6.clicked.connect(lambda state, index=6: macro.run_macro(index))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # sub_win = SubWindow()
    main_win = MainWindow()
    # main_win.M_info.clicked.connect(sub_win.show)
    sys.exit(app.exec_())


"""
pyuic5 ./AutoSigner/sub.ui -o ./AutoSigner/sub_ui.py
pyuic5 ./AutoSigner/main.ui -o ./AutoSigner/main_ui.py
pyrcc5 ./AutoSigner/main.qrc -o ./AutoSigner/main_rc.py
pyinstaller -w -F --log-level=WARN --hidden-import AutoSigner/main_ui.py --hidden-import AutoSigner/main_rc.py --icon=./AutoSigner/icon.ico "AutoSig.exe" ./AutoSigner/main.py
pyinstaller -w -F --log-level=WARN --hidden-import ./AutoSigner/main_ui.py --hidden-import ./AutoSigner/main_rc.py --icon=./AutoSigner/icon.ico main.py
pyinstaller -w -F --log-level=WARN --hidden-import AutoSigner/main_ui.py --hidden-import AutoSigner/main_rc.py --icon=./AutoSigner/icon.ico main.py
pyinstaller -w -F --log-level=WARN --hidden-import AutoSigner/main_ui.py --icon=./AutoSigner/icon.ico main.py
pyinstaller -w -F --log-level=WARN --hidden-import ./AutoSigner/main_ui --icon=./AutoSigner/icon.ico main.py
"""