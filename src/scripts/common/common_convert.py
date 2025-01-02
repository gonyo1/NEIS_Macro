"""
이 파일은 PyQt로 작성된 UI 파일(.ui)을 Python 코드(.py)로 변환하기 위해 설계되었습니다.

- UI 파일은 반드시 `src/views/ui` 폴더에 위치해야 합니다.
- 변환 작업은 `src/config/config.json` 파일에 설정된 개발자 모드 및 UI 디자이너 정보를 기반으로 수행됩니다.

전제 조건:
1. `src/views/ui` 폴더에 .ui 파일이 있어야 합니다.
2. `src/config/config.json` 파일에 아래 형식의 항목이 포함되어 있어야 합니다:
   ```json
   {
       "Developer": {
           "Mode": "True",
           "UI_Designer": "user"
       }
   }
"""


# Import Packages
import os
import glob
from . import common_path
from . import common_json
from . import common_info

# src 폴더 내 경로 설정
view_dir = 'src/views'
view_path = common_path.get_join_path(view_dir)

config_path = "src/config/config.json"
config = common_json.load_json_file(common_path.get_join_path(config_path))


def grab_files_paths(ui_file):
    # Grab filename and basedir
    base_dir = os.path.dirname(ui_file)
    filename = os.path.basename(ui_file)
    filename_core = filename.rsplit('.', 1)[0]
    return base_dir, filename, filename_core


def convert_ui2py():
    def add_resource_py_path(ui: str = None, basename: str = None):
        # Editing <Ui_file_name>_ui.py resource path
        with open(f"{ui}_ui.py", "r", encoding="utf-8") as read_ui_file:
            lines = read_ui_file.readlines()[:]  # -1] if basename != 'main' else basename
            lines = lines[:-1] if 'import' in lines[-1] else lines
            basename = 'main' if basename != 'main' else basename
            lines.append(f'from {view_dir.replace("/", ".")}.ui import {basename}_rc')

        with open(f"{ui}_ui.py", "w", encoding="utf-8") as write_ui_file:
            write_ui_file.writelines(lines)

    def remove_ui_stylesheet(ui: str = None, objects: list = None):
        for obj in objects:
            # Editing <Ui_file_name>_ui.py stylesheet
            with open(f"{ui}_ui.py", "r", encoding="utf-8") as read_ui_file:
                stylesheet = read_ui_file.read()
                start = stylesheet.find(f"self.{obj}.setStyleSheet(")
                end = stylesheet.find(f"self.{obj}.setObjectName(")
                stylesheet = stylesheet[:start] + stylesheet[end:]

            with open(f"{ui}_ui.py", "w", encoding="utf-8") as write_ui_file:
                write_ui_file.write(stylesheet)

    def check_config_data(data):
        try:
            return data
        except Exception as e:
            # TODO: print(e) 를 get_info 와 연결하기
            return True

    def convert_ui_files():
        # Stylesheet 를 지울 objects 리스트 선언
        remove_stylesheet_objects = []

        # 모든 UI 파일 변환
        for ui_file in glob.glob(os.path.join(view_path, "ui/*.ui")):
            base_dir, filename, filename_core = grab_files_paths(ui_file)
            convert_filename = os.path.join(base_dir, f"{filename_core}")

            # Convert .ui to .py
            os.system(f"pyuic5 {ui_file} -o {convert_filename}_ui.py")
            print(f"  🔥[info] {convert_filename}_ui.py has created. {common_info.get_info()}")

            # Append resource path
            add_resource_py_path(ui=convert_filename, basename=filename_core)
            remove_ui_stylesheet(ui=convert_filename, objects=remove_stylesheet_objects)

    def convert_qrc_files():
        # 모든 RESOURCE 파일 변환
        for qrc_file in glob.glob(os.path.join(view_path, "ui/*.qrc")):
            base_dir, filename, filename_core = grab_files_paths(qrc_file)
            convert_filename = os.path.join(base_dir, f"{filename_core}")

            # Convert .qrc to .py
            os.system(f"pyrcc5 {qrc_file} -o {convert_filename}_rc.py")
            print(f"  🔥[info] {convert_filename}_rc.py has created. {common_info.get_info()}")

    mode = check_config_data(config["Developer"]["Mode"])
    designer = check_config_data(config["Developer"]["UI_Designer"])

    # Convert 활성화 모드 여부 확인
    if not (mode == "True" and designer in view_path):
        print(f"🥑[info] Python doesn't convert resource files. {common_info.get_info()}")
        return

    print(f"🔥[info] Python converting resource files. Please wait. {common_info.get_info()}")
    convert_ui_files()
    convert_qrc_files()


# Convert mode execute
convert_ui2py()


