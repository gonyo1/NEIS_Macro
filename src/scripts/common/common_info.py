"""
이 파일은 Python 코드에서 함수명, 코드가 호출된 라인, 파일명을 손쉽게 확인할 수 있도록 정보를 제공하는 유틸리티입니다.

- 디버깅이나 로깅 시 유용하게 사용할 수 있습니다.
- 호출된 함수의 이름, 실행된 코드의 라인 번호, 파일명을 직관적으로 확인할 수 있도록 지원합니다.

주요 기능:
- 현재 실행 중인 코드의 라인 번호를 가져옵니다.
- 호출된 모듈(함수)의 이름을 반환합니다.
- 코드가 실행된 파일명을 확인합니다.

사용 방법:
1. `get_info()` 함수를 호출하면 함수명, 라인 번호, 파일명을 포함한 문자열이 반환됩니다.
2. 반환된 문자열은 디버깅 로그나 출력 메시지에 활용할 수 있습니다.

예제:
```python
def example_function():
    print(get_info())

example_function()
# 출력 예시: ( line: 12 // module: example_function // file: example_script.py )
"""


# Import Packages
import os
from inspect import currentframe, getmodule, stack, getframeinfo


def get_info():
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
