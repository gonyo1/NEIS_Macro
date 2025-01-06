from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsDropShadowEffect, QSizePolicy, QPushButton
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QSize, QRect


class QMacroButton(QPushButton):
    def __init__(self, parent=None, layout=None, index=0, color: tuple = (230, 111, 85)):
        super().__init__(parent)

        # 기본 Widget 생성
        self.Macro_items = QWidget(parent)
        self.Macro_items.setMinimumSize(QSize(158, 110))
        self.Macro_items.setMaximumSize(QSize(180, 110))
        self.Macro_items.setStyleSheet(f"#Macro_items_{str(index)} "
                                       f"    {{background: rgb({color[0]}, {color[1]}, {color[2]});"
                                       f"}}\n"
                                       f"#Macro_items_{str(index)}:hover "
                                       f"    {{background:  rgba({color[0]}, {color[1]}, {color[2]}, 200);"
                                       f"}}")
        self.Macro_items.setObjectName(f"Macro_items_{str(index)}")

        # PushButton 생성
        self.Macro_push = QPushButton(self.Macro_items)
        self.Macro_push.setGeometry(QRect(0, 0, 158, 110))
        self.Macro_push.setMinimumSize(QSize(158, 110))
        self.Macro_push.setMaximumSize(QSize(180, 110))
        self.Macro_push.setStyleSheet("")
        self.Macro_push.setText("")
        self.Macro_push.setObjectName(f"Macro_push_{str(index)}")

        # Label Text 생성
        self.Macro_labels = QLabel(self.Macro_items)
        self.Macro_labels.setEnabled(False)
        self.Macro_labels.setGeometry(QRect(16, 65, 120, 21))
        self.Macro_labels.setStyleSheet("QLabel {font: 14px; font-weight: bold; color: white;}")
        self.Macro_labels.setIndent(-1)
        self.Macro_labels.setObjectName(f"Macro_labels_{str(index)}")

        # Description Text 생성
        self.Macro_describes = QLabel(self.Macro_items)
        self.Macro_describes.setEnabled(False)
        self.Macro_describes.setGeometry(QRect(16, 80, 120, 21))
        self.Macro_describes.setStyleSheet("QLabel {font: 10px; color: white;}}")
        self.Macro_describes.setIndent(-1)
        self.Macro_describes.setObjectName("Macro_describes")

        # Icon image 생성
        self.Macro_icon = QLabel(self.Macro_items)
        self.Macro_icon.setEnabled(False)
        self.Macro_icon.setGeometry(QRect(16, 16, 28, 30))
        self.Macro_icon.setStyleSheet("border-image: url(:/img/assets/user-solid.svg);")
        self.Macro_icon.setText("")
        self.Macro_icon.setScaledContents(True)
        self.Macro_icon.setIndent(-1)
        self.Macro_icon.setObjectName("Macro_icon")
        self.Macro_labels.raise_()
        self.Macro_describes.raise_()
        self.Macro_icon.raise_()
        self.Macro_push.raise_()

        # Append Macro Button to Macro bar Layout
        layout.addWidget(self.Macro_items, index//2, index % 2, 1, 1)
