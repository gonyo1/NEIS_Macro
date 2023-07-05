# pip install pyqt5 pywin32 pillow pyinstaller tinyaes
import os.path
import sys
from glob import glob
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget
from Nsmc.src.view.main_ui import Ui_MainApp as mp
import Nsmc.src.macro as mc
import Nsmc.src.view.main_rc
from PyQt5.QtCore import QThread, pyqtSignal



class MainWindow(QMainWindow, mp):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self.setWindowTitle("  NEIS Macro by Gonyo (Released 2023.7.5.)")
        self.setWindowIcon(QIcon(":/img/fox.svg"))
        self.show_alter("off")
        self.mcr_object = mc.MacroThread(self)
        self.mcr_object.threadEvent.connect(self.mcr_end_event)

        self.set_signal()

    def set_signal(self):

        self.Form_downbar_get.clicked.connect(mc.get_form_file)
        self.Tutorial_Push.clicked.connect(mc.show_how_to_use)
        self.Macro_push_1.clicked.connect(lambda state, index=1: self.run_upload_thread(index))
        self.Macro_push_2.clicked.connect(lambda state, index=2: self.run_upload_thread(index))

    def run_upload_thread(self, index: int = 0):
        print("clicked")
        self.show_alter("on")
        self.mcr_object.selector = index
        self.mcr_object.start()

    def mcr_end_event(self):
        self.show_alter("off")

    def show_alter(self, status: str = "off"):
        if status == "off":
            self.black.setEnabled(False)
            self.black.hide()
        else:
            self.black.setEnabled(True)
            self.black.raise_()
            self.black.show()


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    # sys.exit(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # sub_win = SubWindow()
    main_win = MainWindow()
    # main_win.M_info.clicked.connect(sub_win.show)
    sys._excepthook = sys.excepthook
    sys.excepthook = my_exception_hook
    sys.exit(app.exec_())

"""
pyuic5 ./Nsmc/src/view/main.ui -o ./Nsmc/src/view/main_ui.py
pyuic5 ./AutoSigner/main.ui -o ./AutoSigner/main_ui.py
pyrcc5 ./AutoSigner/main.qrc -o ./AutoSigner/main_rc.py
pyinstaller -w -F --log-level=WARN --hidden-import AutoSigner/main_ui.py --hidden-import AutoSigner/main_rc.py --icon=./AutoSigner/icon.ico "AutoSig.exe" ./AutoSigner/main.py
pyinstaller -w -F --log-level=WARN --hidden-import ./AutoSigner/main_ui.py --hidden-import ./AutoSigner/main_rc.py --icon=./AutoSigner/icon.ico main.py
pyinstaller -w -F --log-level=WARN --hidden-import AutoSigner/main_ui.py --hidden-import AutoSigner/main_rc.py --icon=./AutoSigner/icon.ico main.py
pyinstaller -w -F --log-level=WARN --hidden-import AutoSigner/main_ui.py --icon=./AutoSigner/icon.ico main.py
pyinstaller -w -F --log-level=WARN --hidden-import ./AutoSigner/main_ui --icon=./AutoSigner/icon.ico main.py
"""
