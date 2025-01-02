"""
이 파일은 'common' 폴더 내 Python 파일의 Import를 지원하기 위해 설계되었습니다.
- 'common' 폴더 내부에서 사용할 경우, 로컬 파일을 상대 경로로 불러올 수 있도록 합니다.
- 외부에서 사용할 경우, 'common' 폴더의 경로를 시스템 경로에 등록하여
  해당 폴더의 모듈을 쉽게 불러올 수 있도록 합니다.

사용 방법:
    1. 'common' 폴더 내부:
       - 같은 디렉토리의 다른 파일을 상대 경로로 불러옵니다.
    2. 'common' 폴더 외부:
       - 'common' 폴더를 시스템 경로에 자동으로 추가하여 파일을 쉽게 불러올 수 있습니다.
"""

# Regist path to system path
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

# Import local packages
from . import *