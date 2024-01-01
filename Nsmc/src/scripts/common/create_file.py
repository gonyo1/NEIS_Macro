import os, sys
from Nsmc.src.scripts.common import get_src_path


def create_files():
    src_dir_path = get_src_path.get_join_path()

    os.makedirs('Nsmc/src/data', exist_ok=True)
    os.makedirs('Nsmc/src/img', exist_ok=True)

    data_dir = get_src_path.get_join_path("data")
    img_dir = get_src_path.get_join_path("img")

    if not os.path.isfile("Nsmc/src/data/특기사항.xlsx"):
        for file in os.listdir(src_dir_path):
            if file.endswith(".xlsx"):
                name = os.path.basename(file)
                file = os.path.join(src_dir_path, name)
                path = os.path.join(data_dir, name)
                os.rename(file, path)

            if file.endswith(".png"):
                name = os.path.basename(file)
                file = os.path.join(src_dir_path, name)
                path = os.path.join(img_dir, name)
                os.rename(file, path)
