import pandas as pd
import os
import time
import win32clipboard

try:
    import win32com.client as win32
    import pythoncom
except ImportError:
    os.system("pip install pywin32")
    import win32com.client as win32
    import pythoncom
try:
    import pygetwindow as gw
except:
    os.system("pip install pygetwindow")
    import pygetwindow as gw
try:
    import pyperclip
except ImportError:
    os.system("pip install pyperclip")
    import pyperclip


# Import Local Files
from Nsmc.src.scripts.upload.upload_macro import KeyEvent
from Nsmc.src.scripts.upload.translate_data import set_copied_data_to_list



# NEIS SELECTOR
pythoncom.CoInitialize()
shell = win32.Dispatch('WScript.Shell')
shell.AppActivate("4세대 나이스 시스템")

# MACRO CLASS CALL
key_event = KeyEvent(shell)

학년 = 5
과목 = ["국어", "수학", "사회", "과학", "음악", "미술", "체육", "영어", "실과", "도덕", "바른생활슬기로운생활즐거운생활"]
최종평가파일 = os.path.abspath("../../src/2학기_최종평가파일.xlsx")
데이터프레임 = pd.read_excel(최종평가파일)


def upload():
    # "4세대 지능형 나이스 시스템" 창을 찾습니다.
    windows = gw.getWindowsWithTitle("4세대 나이스 시스템")
    if not windows:
        print("4세대 나이스 시스템 창을 찾을 수 없습니다.")
        return

    target_window = windows[0]
    target_window.activate()

    key_event.tab(5)
    key_event.press_enter()
    key_event.tab(9)
    key_event.press_enter()


    pyperclip.copy("upload_template.xlsx")
    key_event.paste()

    key_event.tab(2)
    key_event.press_enter()

    key_event.tab(1)
    key_event.press_enter()

    key_event.sleep_seconds(0.2)
    key_event.press_enter()

    key_event.sleep_seconds(0.2)
    key_event.press_enter()


while True:
    # 과목 출력
    print(f"0. 학년은 {학년} 학년으로 설정되어있습니다.")
    print("1. 파일로 생성할 과목을 선택해주세요.")
    for index, item in enumerate(과목, start=1):
        print(f"    {index}. {item}")

    # 과목 선택
    타겟과목 = 과목[int(input("번호를 입력해주세요: ")) - 1]
    print(타겟과목)
    타겟학년데이터 = 데이터프레임[(데이터프레임["학년"] == 학년) & (데이터프레임["과목"] == 타겟과목)]

    영역명 = 타겟학년데이터.iloc[:, [2, 3, 4]]
    영역명.to_excel(os.path.abspath("../../src/upload_template.xlsx"), index=False)

    upload()

