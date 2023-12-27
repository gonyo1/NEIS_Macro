import os
from pprint import pprint
from inspect import currentframe, getmodule, stack, getframeinfo

def get_file_info():
    logger = []

    # Get current frame
    current_frame = currentframe()
    current_line = current_frame.f_back.f_lineno

    # Get Caller module
    frame = stack()[1]
    module = getmodule(frame[0])
    filename = os.path.basename(module.__file__)

    # Get module Name
    module = stack()[1][3]

    return f" ( \033[4mline: {current_line} // module: {module} // file: {filename}\033[0m )"
