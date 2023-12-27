import os, sys
import glob
from Nsmc.src.scripts.common import get_src_path as src_path
from Nsmc.src.scripts.common import get_file_info as file_info


def convert_pyqt_files(config: dict = None):
    def add_resource_py_path(ui: str = None, basename: str = None):
        # Editing <Ui_file_name>_ui.py resource path
        with open(f"{ui}_ui.py", "r", encoding="utf-8") as read_ui_file:
            lines = read_ui_file.readlines()[:-1]
            lines.append(f'from Nsmc.src.views.assets import {basename}_rc')

        with open(f"{ui}_ui.py", "w", encoding="utf-8") as write_ui_file:
            write_ui_file.writelines(lines)

    def remove_ui_stylesheet(ui: str = None):
        # Editing <Ui_file_name>_ui.py stylesheet
        with open(f"{ui}_ui.py", "r", encoding="utf-8") as read_ui_file:
            stylesheet = read_ui_file.read()
            start = stylesheet.find("self.MainWidget.setStyleSheet(")
            end = stylesheet.find("self.MainWidget.setObjectName(")
            stylesheet = stylesheet[:start] + stylesheet[end:]

        with open(f"{ui}_ui.py", "w", encoding="utf-8") as write_ui_file:
            write_ui_file.write(stylesheet)

    def grab_files_paths(ui_file):
        # Grab filename and basedir
        base_dir = os.path.dirname(ui_file)
        filename = os.path.basename(ui_file)
        filename_core = filename.rsplit('.', 1)[0]
        return base_dir, filename, filename_core

    def convert_ui_files(view_dir):
        for ui_file in glob.glob(os.path.join(view_dir, "ui/*.ui")):
            base_dir, filename, filename_core = grab_files_paths(ui_file)
            convert_filename = os.path.join(base_dir, f"{filename_core}")

            # Convert .ui to .py
            os.system(f"pyuic5 {ui_file} -o {convert_filename}_ui.py")
            print(f"--🔥[info] {convert_filename}_ui.py has created. {file_info.get_file_info()}")

            # Append resource path
            add_resource_py_path(ui=convert_filename, basename=filename_core)
            # remove_ui_stylesheet(ui=convert_filename)

    def convert_qrc_files(view_dir):
        for qrc_file in glob.glob(os.path.join(view_dir, "assets/*.qrc")):
            base_dir, filename, filename_core = grab_files_paths(qrc_file)
            convert_filename = os.path.join(base_dir, f"{filename_core}")

            # Convert .qrc to .py
            os.system(f"pyrcc5 {qrc_file} -o {convert_filename}_rc.py")
            print(f"--🔥[info] {convert_filename}_rc.py has created. {file_info.get_file_info()}")

    def init_convert_mode():
        view_dir = src_path.get_join_path("views")

        if (config["Developer"]["Mode"] == "True" and
                config["Developer"]["UI_Designer"] in view_dir):
            print(f"🔥[info] Python converting resource files. Please wait. {file_info.get_file_info()}")

            # convert files
            convert_ui_files(view_dir)
            convert_qrc_files(view_dir)
        else:
            print(f"🥑[info] Python doesn't convert resource files. {file_info.get_file_info()}")

    # Check parameter
    if config is None:
        config = {"DEV_MODE": False, "UI_DESIGNER": None}

    # Convert mode execute
    init_convert_mode()
