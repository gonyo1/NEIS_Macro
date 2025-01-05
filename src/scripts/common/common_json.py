import os
import json
from . import common_path
from . import common_info


def get_directory(dirname: str) -> str:
    # if darwin system, then add .replace("\\", "/") for linux
    return os.path.join(common_path.get_join_path("src/config"), dirname)


def export_json_file(path: str, data: dict):
    with open(path, 'w', encoding='utf-8') as new_json_file:
        json.dump(data, new_json_file, indent=4, ensure_ascii=False)


def import_json_file(path: str):
    with open(path, 'rt', encoding='utf-8') as file:
        json_data = json.load(file)
        file.close()
    return json_data


def load_json_file(name: str = 'config.json') -> dict:
    def create_json_file(path: str):
        # Make Folders
        if not os.path.isfile(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)

        # Generate json data
        datas = {
            "AppName": "FriendsNetwork",
            "Version": "1.0",
            "Contributors": ["Kim. TaeHa", "Ahn. JongHo", "Park. EunMi"],
            "FontFamily": ["Pretendard", "FontAwesome"],
            "AppDatas": {
                "Theme": "main_light"
            }
        }

        # Save json file
        export_json_file(path, datas)
        print(f"🔥[info] New json file created. {common_info.get_info()}")

    # Get json file path
    json_file = get_directory(name)

    # Generate json file if <name(ex. config.json)> json file is not found
    if not os.path.isfile(json_file):
        create_json_file(json_file)

    # Load json file data
    json_data = import_json_file(json_file)

    return json_data


def edit_json_file(key: str, value: str, name: str = 'config.json'):
    # Get json file path
    json_file = get_directory(name)

    # Load json file data
    json_data = import_json_file(json_file)

    # Change json data
    json_data[key] = value

    # Save json file
    export_json_file(json_file, json_data)

    return json_data



