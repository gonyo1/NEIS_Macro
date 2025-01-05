import os
from src.scripts.common import common_path

# os.system("pip install pyinstaller==4.10")


def execute_compile(path, args):
    os.system(f"cd {path}")
    os.system(f"pyinstaller {args}")


def set_compile_option(no_console: bool = True, one_file: bool = True, log_level: str = "WARN"):
    option = {
        "no_console": no_console,
        "oneFile": one_file,
        "logLevel": log_level
    }
    return option


def setup_program_args(_type: str = "launcher"):
    def main_program_compile_setting():
        app_name = "index"
        option = set_compile_option()
        app_path = common_path.get_join_path(f"{app_name}.py")
        args = " ".join(['-w' if option["no_console"] is True else '',
                         '-F' if option["oneFile"] is True else '',
                         f'--name={app_name}',
                         f'--log-level={option["logLevel"]}',
                         '--add-data="./src/data;./src/data"',
                         '--add-data="./src/img;./src/img"',
                         '--icon="./src/views/assets/fox.ico"',
                         app_path
                         ])
        return args

    # def launcher_program_compile_setting():
    #     app_name = "launcher"
    #     option = set_compile_option()
    #     app_path = common_path.get_join_path(f"{app_name}.py")
    #     args = " ".join(['-w' if option["no_console"] is True else '',
    #                      '-F' if option["oneFile"] is True else '',
    #                      f'--name={app_name}',
    #                      f'--log-level={option["logLevel"]}',
    #                      '--icon="./src/static/media/image/Munk.ico"',
    #                      app_path
    #                      ])
    #     return args

    compile_args = None

    if _type == "main":
        compile_args = main_program_compile_setting()
    elif _type == "launcher":
        pass
        # comile_args = launcher_program_compile_setting()

    return compile_args


# 컴파일 변수 설정
compile_path = common_path.get_join_path("program")
PyinstallerArgs = setup_program_args("main")
execute_compile(compile_path, PyinstallerArgs)

