"""
이 파일은 Python 코드가 exe로 컴파일된 경우에도 경로 관련 오류 없이 py 파일들을 불러올 수 있도록 지원하기 위해 설계되었습니다.

- exe로 컴파일된 환경에서도 파일 경로를 정확히 찾을 수 있도록 경로를 처리합니다.
- 상대 경로를 기반으로 실제 경로를 계산하여 안정적인 파일 접근을 보장합니다.

사용법:
- `get_join_path` 함수에 초기 경로부터의 상대 경로를 전달하여 파일의 실제 경로를 얻을 수 있습니다.
- 예시:
    ```python
        src/views/main_ui.py 파일의 경로를 가져오려면
        get_join_path("src/views/main_ui.py")
"""


# Import Packages
import os, sys
from . import common_info


def get_join_path(join_path=None):
    def get_parent_path(path: str) -> str:
        parent = os.path.dirname(path)
        # print(f"📌 Parent directory: \033[4m{parent}\033[0m")
        return os.path.abspath(parent)

    def get_main_path() -> str:
        # Get executed files path
        path = os.path.abspath(__file__)
        basename = None
        directory_name = None

        # Get path of [.exe] file
        if getattr(sys, 'frozen', False):
            # if ("data" in join_path) or ("config" in join_path):
            path = os.path.abspath(sys.executable)
            basename = os.path.basename(sys.executable)

        # Get [src] directory path recursively
        while True:
            # Get parent directory name
            path = os.path.dirname(path)

            # Split directory name by system platform
            if sys.platform == 'win32':
                directory_name = path.split('\\')[-1]
            elif sys.platform == 'darwin':
                directory_name = path.split('/')[-1]

            # Find if requests start from .exe file
            if basename is not None:
                path = os.path.join(path, "program")
                return get_parent_path(path)

            # Find
            elif directory_name == "src":
                return get_parent_path(path)

    # Change relative path if .py files executed from common directory
    target_path: str = get_main_path()

    # Check if user requested joined path
    if join_path is not None:
        target_path = os.path.abspath(os.path.join(target_path, join_path))

        # Split directory name by system platform
        if sys.platform == 'win32':
            target_path.replace("/", "\\")
        elif sys.platform == 'darwin' or sys.platform == "linux":
            target_path.replace("\\", "/")

    return target_path
