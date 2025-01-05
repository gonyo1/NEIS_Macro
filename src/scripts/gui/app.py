# python internal packages
import os


# local packages
from src.scripts.common import common_path
from src.scripts.gui.gui_macro import MacroPage

# python external packages
from PyQt5.QtWidgets import QMainWindow, QApplication, QSizeGrip, QPushButton
from PyQt5.QtCore import Qt, QPoint, QRect, QEvent, QSize, QRectF, pyqtSignal
from PyQt5.Qt import QMouseEvent, QIcon


class NEISMacro(MacroPage):
    is_program_opened = "OFF"
    gripSize = 10
    grip_point = None
    side_grips = list()
    grips = list()

    # MainWindow 전체에서 사용할 시그널 그룹

    def __init__(self, main_app: QApplication = None, config: dict = None):
        # Overloading MainWindow
        super().__init__()

        # Initialize Setup
        self.set_window_flags()
        self.init_gui_setup()
        self.init_set_signal()

    def set_window_flags(self):
        self.setWindowTitle("NEIS Macro")
        self.setWindowIcon(QIcon(":/img/fox.svg"))
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def init_gui_setup(self):
        def init_window_setup():
            self.infobox_title.original_stylesheet = self.infobox_title.styleSheet()

        def init_pushbutton_handler():
            for button in self.findChildren(QPushButton):
                button.setCursor(Qt.PointingHandCursor)

        def init_app_icon_setting():
            self.setWindowIcon(QIcon(os.path.join(common_path.get_join_path("src/views/assets"), "fox.ico")))

        init_window_setup()
        init_pushbutton_handler()
        init_app_icon_setting()

    def init_set_signal(self):
        def open_tutorial_image():
            path = common_path.get_join_path("src/img/howtocopy.png")
            os.startfile(path)

        def open_xlsx_folder():
            origin_dir = common_path.get_join_path("src/data")
            os.startfile(origin_dir)

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
        self.Form_downbar_get.clicked.connect(lambda: open_xlsx_folder())

        # Tutorial Slot
        self.Form_info_get.clicked.connect(lambda: open_tutorial_image())

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

    def mousePressEvent(self, event):
        self.grip_point = event.globalPos()

    def mouseMoveEvent(self, event):
        def is_window_bar():
            return self.grip_point.y() - self.y() < 36

        # 상단 바 제외 MoveEvent 무시
        try:
            if is_window_bar():
                delta = QPoint(event.globalPos() - self.grip_point)
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.grip_point = event.globalPos()
        except (AttributeError, TypeError):
            pass
