# pip install pyqt5 pywin32 pyinstaller pyautogui pyperclip tinyaes

import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication
from Nsmc.src.view.main_ui import Ui_MainApp as mp
import Nsmc.src.macro as mc
import Nsmc.src.view.main_rc


class MainWindow(QMainWindow, mp):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self.setWindowTitle("  NEIS Macro by Gonyo (Released 2023.7.5.)")
        self.setWindowIcon(QIcon(":/img/fox.svg"))
        self.infobox_title.original_stylesheet = self.infobox_title.styleSheet()
        self.show_alter("off")
        self.mcr_object = mc.MacroThread(self)
        self.mcr_object.threadEvent.connect(self.mcr_end_event)

        self.set_signal()

    def set_signal(self):

        self.Form_downbar_get.clicked.connect(mc.open_form_file)
        self.Tutorial_Push.clicked.connect(mc.show_how_to_use)
        self.Macro_push_1.clicked.connect(lambda state, index=1: self.run_upload_thread(index))
        self.Macro_push_2.clicked.connect(lambda state, index=2: self.run_upload_thread(index))
        self.Macro_push_3.clicked.connect(self.mcr_developing_event)
        # self.Macro_push_3.clicked.connect(lambda state, index=3: self.run_upload_thread(index))
        self.Macro_push_4.clicked.connect(lambda state, index=4: self.run_upload_thread(index))
        self.Macro_push_5.clicked.connect(self.mcr_developing_event)
        # self.Macro_push_5.clicked.connect(lambda state, index=5: self.run_upload_thread(index))

        self.infobox_confirm.clicked.connect(self.mcr_end_event)

    def run_upload_thread(self, index: int = 0):
        self.show_alter("on")
        self.mcr_object.selector = index
        self.mcr_object.start()

        self.infobox_title.setText("데이터를 나이스로 업로드 중입니다.")
        self.infobox_title.setStyleSheet("color: rgb(52, 120, 245)")
        self.infobox_detail.setText("업로드 중에 조작은 오류를 발생시킬 수 있습니다.")

    def mcr_end_event(self):
        self.show_alter("off")

    def mcr_developing_event(self):
        self.show_alter("on")
        self.infobox_title.setText("현재 개발 중인 기능 입니다.")
        self.infobox_title.setStyleSheet("color: rgb(52, 120, 245)")
        self.infobox_detail.setText("7월 중에는 업데이트하여 재배포 예정")

    def show_alter(self, status: str = "off"):
        if status == "off":
            self.infobox_title.setStyleSheet(self.infobox_title.original_stylesheet)
            self.infobox_title.setText("업로드를 실행할 수 없습니다.")
            self.infobox_detail.setText("나이스가 켜져 있는지 확인해주세요.")
            self.black.setEnabled(False)
            self.black.hide()
        else:
            self.black.setEnabled(True)
            self.black.raise_()
            self.black.show()


def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    # sys.exit(1)


if __name__ == "__main__":
    mc.get_file()
    app = QApplication(sys.argv)
    main_win = MainWindow()
    sys._excepthook = sys.excepthook
    sys.excepthook = my_exception_hook
    sys.exit(app.exec_())

"""
pyuic5 ./Nsmc/src/view/main.ui -o ./Nsmc/src/view/main_ui.py
pyrcc5 ./Nsmc/src/view/main.qrc -o ./Nsmc/src/view/main_rc.py
pyinstaller -w -F --log-level=WARN --add-data="./Nsmc/src/data/*.xlsx;." --add-data="./Nsmc/src/img/*.png;." --icon=./Nsmc/src/view/fox.ico main.py
pyinstaller -w -F --add-data="./Nsmc/src/data/*.xlsx;." --add-data="./Nsmc/src/img/*.png;." --icon=./Nsmc/src/view/fox.ico main.py

"""
