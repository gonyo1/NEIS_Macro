import os
import random

# local packages
from src.scripts.macro import macro as mc
from src.scripts.gui.gui_common import NEISMacroProgram
from src.scripts.gui.custom.QMacroButton import QMacroButton
from src.views.ui.main_ui import Ui_MainApp as mp

# Import PyQt5 modules
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QWidget, QSizePolicy, QVBoxLayout, QHBoxLayout, \
    QLayout, QLabel, QPushButton, QListWidget, QAbstractScrollArea, QAbstractItemView, QListView, QFrame, \
    QListWidgetItem, QSpacerItem


class MacroPage(NEISMacroProgram, QMainWindow, mp):
    mcr_object = mc.MacroThread()

    def __init__(self):
        # Overload NEISMacroProgram class
        super().__init__()

        # Setup initial function
        self.setupUi(self)
        self.init_setup_signal()
        self.init_gui_setting()

    def init_setup_signal(self):
        def init_stacked_widget_page_signal():
            def turn_stacked_widget_page(add: int = 0):
                pages = self.Form_stackedWidget.count() - 1
                current_page = self.Form_stackedWidget.currentIndex()

                if current_page == pages:
                    self.Form_stackedWidget.setCurrentIndex(0)
                elif current_page == 0:
                    self.Form_stackedWidget.setCurrentIndex(pages)
                else:
                    self.Form_stackedWidget.setCurrentIndex(current_page + add)

            self.prev_page.clicked.connect(lambda: turn_stacked_widget_page(-1))
            self.next_page.clicked.connect(lambda: turn_stacked_widget_page(1))

        def init_window_bar_signal():
            self.window_minimum.clicked.connect(lambda: self.showMinimized())
            self.window_close.clicked.connect(lambda: self.close())

        init_stacked_widget_page_signal()
        init_window_bar_signal()

    def run_upload_thread(self, index: int = 0):
        print(index)
        self.black.raise_()
        self.infobox_title.setText("데이터를 나이스로 업로드 중입니다.")
        self.infobox_title.setStyleSheet("color: rgb(52, 120, 245)")
        self.infobox_detail.setText("업로드 중에 조작은 오류를 발생시킬 수 있습니다.")

        self.init_alter_setup("ON")
        self.mcr_object.selector = index
        self.mcr_object.start()

    def init_gui_setting(self):
        def create_macro_buttons():
            def get_color_tuple(text):
                text = text.replace("rgb", "")
                text = text.replace("(", "")
                text = text.replace(")", "")
                color_list = text.split(",")
                return [str(_color.strip()) for _color in color_list]

            button_index = 0
            button_list = []

            for button_title, button_data in self.MACRO_DATA.items():
                # Create Macro Button
                color = get_color_tuple(button_data["background"])

                button = QMacroButton(parent=self.Macrobar_grid,
                                      layout=self.Macrobar_grid_layout,
                                      index=button_index,
                                      color=tuple(color))
                button.Macro_labels.setText(button_data["title"])
                button.Macro_describes.setText(button_data["description"])
                button.Macro_icon.setStyleSheet(f"border-image: url(:/img/assets/{button_data['icon']});")
                button.Macro_push.clicked.connect(
                    lambda num=int(button.Macro_items.objectName().rstrip("_")[-1]): self.run_upload_thread(index=num))

                button_list.append([button, button_data["title"], button_data["macro"]])
                button_index += 1

            print(button_list)
            spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.Macrobar_grid_layout.addItem(spacerItem, button_index//2 + 1, 0, 1, 1)

        create_macro_buttons()
