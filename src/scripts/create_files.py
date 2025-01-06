import os
from src.scripts.common import common_path


def create_files():
    src_dir_path = os.path.abspath("src")

    os.makedirs(common_path.get_join_path('src/data'), exist_ok=True)
    os.makedirs(common_path.get_join_path('src/img'), exist_ok=True)

    data_dir = common_path.get_join_path("data")
    img_dir = common_path.get_join_path("img")

    if not os.path.isfile(common_path.get_join_path("src/data/특기사항.xlsx")):
        for file in os.listdir(src_dir_path):
            if file.endswith(".xlsx"):
                name = os.path.basename(file)
                file = os.path.join(src_dir_path, f"data/{name}")
                path = os.path.join(data_dir, name)
                os.rename(file, path)
                print(" 샘플 파일이 옮겨졌습니다... ")

            if file.endswith(".png"):
                name = os.path.basename(file)
                file = os.path.join(src_dir_path, f"img/{name}")
                path = os.path.join(img_dir, name)
                os.rename(file, path)
                print(" 이미지 파일이 옮겨졌습니다... ")
