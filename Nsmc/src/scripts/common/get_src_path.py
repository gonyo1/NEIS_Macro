import os, sys


def get_join_path(join_path=None):
    def get_src_path():
        # Get running files path
        path = os.path.abspath(__file__)

        # Get src path
        while True:
            path = os.path.dirname(path)

            # Split directory name by system platform
            if sys.platform == 'win32':
                dirname = path.split('\\')[-1]
            elif sys.platform == 'darwin':
                dirname = path.split('/')[-1]

            # Get src path recursively
            if dirname == "src":
                return os.path.abspath(path)

    # Change relative path if .py files executed from common directory
    target_path = get_src_path()

    if join_path is not None:
        target_path = os.path.abspath(os.path.join(target_path, join_path))

        # Split directory name by system platform
        if sys.platform == 'win32':
            target_path.replace("/", "\\")
        elif sys.platform == 'darwin':
            target_path.replace("\\", "/")


    return target_path