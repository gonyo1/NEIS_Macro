# python internal packages
import os


# local packages
from Nsmc.src.scripts import macro as mc
from Nsmc.src.scripts.upload.upload_macro import KeyEvent
from Nsmc.src.view.main_ui import Ui_MainApp as mp
from Nsmc.src.scripts.common import open_xlsx_file as xlsx


# python external packages
try:
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QMainWindow, QApplication
except ImportError:
    os.system("pip install pyqt5 pyqt5-tools")
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QMainWindow, QApplication


class NEISMacro(QMainWindow, mp):
    def __init__(self, parent=None):
        super(NEISMacro, self).__init__(parent)
        self.setupUi(self)
        self.mcr_object = mc.MacroThread(self)
        # Initialize Setup
        self.init_setup()

    def init_setup(self):
        self.init_window_setup()
        self.init_set_signal()
        self.init_alter_setup("OFF")

    def init_window_setup(self):
        self.infobox_title.original_stylesheet = self.infobox_title.styleSheet()

    def init_set_signal(self):
        # Macro Part -------------------------------------------
        def mcr_end_event():
            self.init_alter_setup("OFF")

        def mcr_developing_event():
            self.init_alter_setup("ON")
            self.infobox_title.setText("현재 개발 중인 기능 입니다.")
            self.infobox_title.setStyleSheet("color: rgb(52, 120, 245)")
            self.infobox_detail.setText("7월 중에는 업데이트하여 재배포 예정")

        def mcr_developing_event():
            self.init_alter_setup("ON")
            self.infobox_title.setText("업로드가 완료되었습니다.")
            self.infobox_title.setStyleSheet("color: rgb(52, 120, 245)")
            self.infobox_detail.setText("OK 버튼을 눌러 종료하시면 됩니다.")


        # Upload Thread Part -------------------------------------------
        def run_upload_thread(index: int = 0):
            self.infobox_title.setText("데이터를 나이스로 업로드 중입니다.")
            self.infobox_title.setStyleSheet("color: rgb(52, 120, 245)")
            self.infobox_detail.setText("업로드 중에 조작은 오류를 발생시킬 수 있습니다.")

            self.init_alter_setup("ON")
            self.mcr_object.selector = index
            self.mcr_object.start()

        # Get xlsx file Slot
        self.Form_downbar_get.clicked.connect(lambda: xlsx.open_xlsx_file())

        # Tutorial Slot
        self.Tutorial_Push.clicked.connect(lambda: self.open_tutorial_page())

        # Macro Clicked Slot
        self.mcr_object.threadEvent.connect(lambda: mcr_developing_event())  # When Macro Started
        self.infobox_confirm.clicked.connect(mcr_end_event)  # Macro [OK] Button clicked

        # Macro Slots
        self.Macro_push_1.clicked.connect(lambda state, index=1: run_upload_thread(index))
        self.Macro_push_2.clicked.connect(lambda state, index=2: run_upload_thread(index))
        self.Macro_push_3.clicked.connect(lambda state, index=3: run_upload_thread(index))
        self.Macro_push_4.clicked.connect(lambda state, index=4: run_upload_thread(index))
        self.Macro_push_5.clicked.connect(mcr_developing_event)
        # self.Macro_push_5.clicked.connect(lambda state, index=5: self.run_upload_thread(index))

    def init_alter_setup(self, status: str = "OFF"):
        if status == "OFF":
            self.infobox_title.setStyleSheet(self.infobox_title.original_stylesheet)
            self.infobox_title.setText("업로드를 실행할 수 없습니다.")
            self.infobox_detail.setText("나이스가 켜져 있는지 확인해주세요.")
            self.black.setEnabled(False)
            self.black.hide()
        else:
            self.black.setEnabled(True)
            self.black.raise_()
            self.black.show()

    @staticmethod
    def open_tutorial_page():
        path = os.path.realpath("./Nsmc/src/img/howtocopy.png")
        os.startfile(path)
