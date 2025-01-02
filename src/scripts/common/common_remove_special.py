"""
이 파일은 Windows에서 사용할 수 없는 특수문자를 전각 문자로 변환하는 기능을 제공합니다.

- Windows 파일 시스템에서 허용되지 않는 특수문자(`\ / : * ? " < > |`)를 안전한 전각 문자로 변환합니다.
- 파일 이름이나 경로를 처리할 때 발생하는 오류를 방지하기 위해 사용됩니다.

주요 기능:
- 입력된 문자열에서 허용되지 않는 문자를 전각 문자로 치환합니다.
- 변환된 문자열은 Windows 환경에서 안전하게 파일 이름으로 사용할 수 있습니다.

사용 방법:
1. 변환할 문자열을 함수에 전달합니다.
   ```python
   sanitized_string = convert_special_characters("example:file?.txt")
   print(sanitized_string)  # 출력: example：file？.txt

"""


# Import Packages
import re

replace_map = {
    '\\': '＼',
    '/': '／',
    ':': '：',
    '*': '＊',
    '?': '？',
    '"': '＂',
    '<': '＜',
    '>': '＞',
    '|': '｜'
}


def convert_special_characters(text):
    # 정규식에서 사용하기 위해 매핑된 키들을 파이프(|)로 연결
    pattern = '|'.join(re.escape(char) for char in replace_map.keys())

    # 매칭되는 문자를 대체 문자로 교체
    return re.sub(pattern, lambda m: replace_map[m.group()], text)

