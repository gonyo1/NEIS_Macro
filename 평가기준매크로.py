# python internal packages
import sys
import time
import os, glob
import win32clipboard


# python external packages
try:
    import pyperclip
except ImportError:
    os.system("pip install pyperclip")
    import pyperclip

try:
    import win32com.client as win32
    import pythoncom
except ImportError:
    os.system("pip install pywin32")
    import win32com.client as win32
    import pythoncom


# Import PyQt5
from PyQt5.QtCore import QThread, pyqtSignal


# Import Local Files
from Nsmc.src.scripts.upload.upload_macro import KeyEvent
from Nsmc.src.scripts.upload.translate_data import set_copied_data_to_list


# NEIS SELECTOR
pythoncom.CoInitialize()
shell = win32.Dispatch('WScript.Shell')
shell.AppActivate("4세대 나이스 시스템")

# MACRO CLASS CALL
key_event = KeyEvent(shell)

# GET DATA FROM CLIPBOARD
data = pyperclip.paste()
data_list = set_copied_data_to_list(selector=1, data=data)
for item in data_list:
    print(item.split("\t"))

def 조회에서_성취기준접근():
    # 성취 기준 접근
    init_tab_count = 8
    key_event.tab(init_tab_count)
    key_event.space()
    key_event.press_enter()
    time.sleep(0.5)

def 평가단계생성():
    key_event.shift_tab_autogui(1, slow=3)
    key_event.press_enter()
    time.sleep(0.3)
    key_event.key_up()
    key_event.tab(8)
    key_event.down(2)
    time.sleep(0.3)

def 평가기준접근():
    key_event.tab(2)
    key_event.press_enter()
    time.sleep(0.3)

def 평가기준입력():
    for num in range(6):
        key_event.copy("상")
        key_event.paste()
        if num < 5:
            key_event.tab(1)

    key_event.shift_tab(8)
    time.sleep(0.3)

def 평가기준저장():
    key_event.press_enter()
    time.sleep(0.3)
    key_event.press_enter()
    time.sleep(0.3)
    key_event.press_enter()

def 성취기준재접근():
    key_event.shift_tab_autogui(6)
    key_event.down()
    key_event.space()
    key_event.press_enter()
    time.sleep(0.3)
    key_event.press_enter()
    time.sleep(0.3)

def 평가생성묶음():
    평가단계생성()
    평가기준접근()
    평가기준입력()
    평가기준저장()

# 조회에서_성취기준접근()
# 평가생성묶음()
# 성취기준재접근()
# 평가생성묶음()



import pyautogui
try:
    import keyboard
except:
    os.system("pip install keyboard")
    import keyboard
try:
    import pygetwindow as gw
except:
    os.system("pip install pygetwindow")
    import pygetwindow as gw
import keyboard
import time


def click_image_in_region(image_path, region, timeout=10):
    """
    주어진 이미지 파일을 화면의 특정 영역에서 찾아 클릭합니다.
    이미지가 화면에 나타날 때까지 기다리며, 주어진 시간(timeout) 동안 이미지를 찾지 못하면 종료합니다.
    """
    image_path = rf'{os.path.abspath(f"Nsmc/src/img/{image_path}")}'

    start_time = time.time()
    while True:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, region=region)
        except:
            print("error")
            continue
        if location is not None:
            pyautogui.click(location)
            return True
        if time.time() - start_time > timeout:
            print(f"Timeout: '{image_path}'를 찾을 수 없습니다.")
            return False
        time.sleep(0.5)


def perform_copy_paste(평가기준):
    """
    지정된 키보드 이벤트 시퀀스를 실행합니다.
    """
    for num in range(6):
        key_event.press_back_space()
        if num % 2 == 0:
            if num == 0:
                key_event.copy("잘함")
                key_event.paste()
            elif num == 2:
                key_event.copy("보통")
                key_event.paste()
            elif num == 4:
                key_event.copy("노력요함")
                key_event.paste()
        else:
            idx = int((num-1)/2)
            key_event.copy(평가기준[idx])
            key_event.paste()
        if num < 5:
            key_event.tab()
    # pyautogui.hotkey('shift', 'tab', presses=8)
    time.sleep(0.3)


def read_xlsx():
    import pandas as pd
    df = pd.read_excel(os.path.abspath("Nsmc/src/2학기_최종평가파일.xlsx"))

    # \n 문자 제거
    columns_to_clean = ["평가요소"]
    for column in columns_to_clean:
        datas = df[column].tolist()
        for idx, data in enumerate(datas):
            datas[idx] = data.replace("\n", "").replace("\r", "")
        df[column] = datas

    return df



def main():
    df = read_xlsx()

    # "4세대 지능형 나이스 시스템" 창을 찾습니다.
    windows = gw.getWindowsWithTitle("4세대 나이스 시스템")
    if not windows:
        print("4세대 지능형 나이스 시스템 창을 찾을 수 없습니다.")
        return

    target_window = windows[0]
    target_window.activate()

    # 창의 위치와 크기를 가져옵니다.
    x, y, width, height = target_window.left, target_window.top, target_window.width, target_window.height
    region = (x, y, width, height)
    index = 0

    while True:
        # 종료 키를 감지합니다.
        if keyboard.is_pressed('shift+esc'):
            print("Shift+Esc가 눌려 프로그램을 종료합니다.")
            break

        # Ctrl+Q를 기다립니다.
        print("A + S 를 누르면 다음 단계로 넘어갑니다.")
        keyboard.wait('a+s')
        _x, _y = pyautogui.position()
        print(_x, _y)


        # NEIS 에서 선택한 평가기준 데이터 얻기
        key_event.press_copy()
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        line = data.split("\t")
        evaluation_point = line[-1].replace("\n", "").replace("\r", "")
        print(f"  ℹ️ 선택한 평가요소는 [ {evaluation_point} ] 입니다. ")

        try:
            idx = df["평가요소"].tolist().index(evaluation_point)
        except ValueError:
            continue

        # 데이터프레임에서 선택한 평가기준 불러오기
        평가기준 = list()
        평가기준.append(df["잘함"].tolist()[idx])
        평가기준.append(df["보통"].tolist()[idx])
        평가기준.append(df["노력요함"].tolist()[idx])

        # Ctrl+Q가 눌리면 단계.png 이미지를 찾아 클릭합니다.
        # position 모를 때
        # while True:
        #   print(pyautogui.position())
        pyautogui.click(1428, 442)
        time.sleep(0.2)

        # 평가단계로 진입
        key_event.tab(2)

        # 잘함/보통/노력요함 맨 앞으로 이동
        key_event.up(5)
        key_event.press_enter()

        # 평가단계 및 평가결과 붙여넣기
        time.sleep(0.1)
        key_event.select_all()
        time.sleep(0.1)
        perform_copy_paste(평가기준)
        print("복사 붙여넣기 완료.")

        # 저장을 찾아 클릭합니다.
        pyautogui.click(1428, 442)
        key_event.shift_tab(2)
        pyautogui.press('enter')
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(0.3)
        pyautogui.press('enter')
        print("엔터 키 입력 완료.")
        pyautogui.click(_x, _y + 40)


if __name__ == "__main__":
    pass
    main()