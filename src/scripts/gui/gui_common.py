
# Import PyQt5 modules
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QWidget, QSizePolicy, QVBoxLayout, QHBoxLayout, \
    QLayout, QLabel, QPushButton, QListWidget, QAbstractScrollArea, QAbstractItemView, QListView, QFrame, \
    QListWidgetItem, QSpacerItem
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt, QTimer, QSize, QUrl, pyqtSignal, QThread
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.Qt import QPixmap

# local packages
from src.scripts.common import common_json


class NEISMacroProgram(QMainWindow):
    # Set Initial configuration
    APP_DATA = {}
    JSON_DATA = common_json.load_json_file("config.json")
    MACRO_DATA = common_json.load_json_file("shortcuts.json")

    def __init__(self):
        super().__init__()
