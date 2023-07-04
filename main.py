# pip install pyqt5 pywin32 pillow pyinstaller tinyaes
import os.path
import sys
from glob import glob
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget
from Nsmc.src.view.main_ui import Ui_MainApp as mp
import Nsmc.src.macro as mc
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
        self.show_alter("off")


    def set_signal(self):
        mc_run = mc.run_upload()

        self.Form_downbar_get.clicked.connect(mc.get_form_file)
        self.Tutorial_Push.clicked.connect(mc.show_how_to_use)
        self.Macro_push_1.clicked.connect(mc_run.run_haengbal_final)
        self.Macro_push_2.clicked.connect(mc_run.run_gyogwa_final)
        self.Macro_push_3.clicked.connect(mc_run.run_gyogwa_final)
        self.Macro_push_4.clicked.connect(mc_run.run_gyogwa_step)
        self.Macro_push_5.clicked.connect(mc_run.run_gyogwa_final)
        self.Macro_push_6.clicked.connect(mc_run.run_gyogwa_final)

    def show_alter(self, status: str = "off"):
        if status == "off":
            self.black.setEnabled(False)
            self.black.hide()
        else:
            self.black.setEnabled(True)
            self.black._raise()
            self.black.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # sub_win = SubWindow()
    main_win = MainWindow()
    # main_win.M_info.clicked.connect(sub_win.show)
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