# python internal packages
import os


# local packages
from src.scripts.macro import macro as mc
from src.views.ui.main_ui import Ui_MainApp as mp
from src.scripts.gui.custom.QSideGrip import QSideGrip
# from src.scripts.common import open_xlsx_file as xlsx


# python external packages
from PyQt5.QtWidgets import QMainWindow, QApplication, QSizeGrip
from PyQt5.QtCore import Qt, QPoint, QRect, QEvent, QSize, QRectF
from PyQt5.Qt import QMouseEvent, QIcon


class NEISMacro(QMainWindow, mp):
    is_program_opened = "OFF"
    gripSize = 10
    grip_point = None
    side_grips = list()
    grips = list()

    def __init__(self, main_app: QApplication = None, config: dict = None):
        # Overloading MainWindow
        super().__init__()

        # Macro Class
        self.mcr_object = mc.MacroThread(self)

        # Initialize Setup
        self.setupUi(self)
        self.set_grip_points()
        self.set_window_flags()
        self.init_gui_setup()
        self.init_set_signal()

    def set_grip_points(self):
        self.side_grips = [
            QSideGrip(self, Qt.LeftEdge),
            QSideGrip(self, Qt.TopEdge),
            QSideGrip(self, Qt.RightEdge),
            QSideGrip(self, Qt.BottomEdge),
        ]

        for i in range(4):
            grip = QSizeGrip(self)
            grip.resize(self.gripSize, self.gripSize)
            self.grips.append(grip)

    def set_window_flags(self):
        self.setWindowTitle("NEIS Macro")
        self.setWindowIcon(QIcon(":/img/fox.svg"))
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def mousePressEvent(self, event):
        self.grip_point = event.globalPos()

    def mouseMoveEvent(self, event):
        def is_window_bar():
            return self.grip_point.y() - self.y() < 36

        def is_maximized():
            return self.isMaximized()

        # 상단 바 제외 MoveEvent 무시
        try:
            if is_window_bar():
                if is_maximized():
                    self.showNormal()
                    self.maximize.setText("")
                    self.setGeometry(self.maximized_geometry)
                delta = QPoint(event.globalPos() - self.grip_point)
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.grip_point = event.globalPos()
        except (AttributeError, TypeError):
            pass


    def init_gui_setup(self):
        def init_window_setup():
            self.infobox_title.original_stylesheet = self.infobox_title.styleSheet()

        init_window_setup()

    def init_set_signal(self):
        # Macro Part -------------------------------------------
        def mcr_end_event():
            self.init_alter_setup("OFF")

        def mcr_developing_event():
            self.init_alter_setup("ON")
            self.infobox_title.setText("현재 개발 중인 기능 입니다.")
            self.infobox_title.setStyleSheet("color: rgb(52, 120, 245)")
            self.infobox_detail.setText("7월 중에는 업데이트하여 재배포 예정")

        # def mcr_developing_event():
        #     self.init_alter_setup("ON")
        #     self.infobox_title.setText("업로드가 완료되었습니다.")
        #     self.infobox_title.setStyleSheet("color: rgb(52, 120, 245)")
        #     self.infobox_detail.setText("OK 버튼을 눌러 종료하시면 됩니다.")

        # Upload Thread Part -------------------------------------------
        def run_upload_thread(index: int = 0):
            self.infobox_title.setText("데이터를 나이스로 업로드 중입니다.")
            self.infobox_title.setStyleSheet("color: rgb(52, 120, 245)")
            self.infobox_detail.setText("업로드 중에 조작은 오류를 발생시킬 수 있습니다.")

            self.init_alter_setup("ON")
            self.mcr_object.selector = index
            self.mcr_object.start()

        # Get xlsx file Slot
        # self.Form_downbar_get.clicked.connect(lambda: xlsx.open_xlsx_file())

        # Tutorial Slot
        self.Tutorial_Push.clicked.connect(lambda: self.open_tutorial_page())

        # Macro Clicked Slot
        self.mcr_object.threadEvent.connect(lambda: mcr_developing_event())  # When Macro Started
        self.infobox_confirm.clicked.connect(mcr_end_event)  # Macro [OK] Button clicked

        # Macro Slots
        # self.Macro_push_1.clicked.connect(lambda state, index=1: run_upload_thread(index))
        # self.Macro_push_2.clicked.connect(lambda state, index=2: run_upload_thread(index))
        # self.Macro_push_3.clicked.connect(lambda state, index=3: run_upload_thread(index))
        # self.Macro_push_4.clicked.connect(lambda state, index=4: run_upload_thread(index))
        # self.Macro_push_5.clicked.connect(lambda state, index=5: run_upload_thread(index))
        # self.Macro_push_6.clicked.connect(lambda state, index=6: run_upload_thread(index))

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
