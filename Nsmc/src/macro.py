import os, glob
import sys
import win32com.client as win32
import pyperclip
import pyautogui
import pythoncom
import time
from PyQt5.QtCore import QThread, pyqtSignal


def get_file():
    try:
        base_dir = sys._MEIPASS
    except AttributeError:
        base_dir = os.path.abspath(".")

    os.makedirs('./Nsmc/src/data', exist_ok=True)
    os.makedirs('./Nsmc/src/img', exist_ok=True)

    data_dir = os.path.realpath("./Nsmc/src/data")
    img_dir = os.path.realpath("./Nsmc/src/img")

    if not os.path.isfile("./Nsmc/src/data/특기사항.xlsx"):
        for file in os.listdir(base_dir):
            if file.endswith(".xlsx"):
                name = os.path.basename(file)
                file = os.path.join(base_dir, name)
                path = os.path.join(data_dir, name)
                os.rename(file, path)

            if file.endswith(".png"):
                name = os.path.basename(file)
                file = os.path.join(base_dir, name)
                path = os.path.join(img_dir, name)
                os.rename(file, path)


def open_form_file():
    origin_dir = os.path.realpath("./Nsmc/src/data")
    os.startfile(origin_dir)


def show_how_to_use():
    path = os.path.realpath("./Nsmc/src/img/howtocopy.png")
    os.startfile(path)


class MacroThread(QThread):
    threadEvent = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        # 기본 데이터
        self.main = parent
        self.copy_entire_data_from_xlsx = []
        self.copy_data_one_student = ''
        self.web_title = "4세대 지능형 나이스 시스템"
        self.how_many_Tab = 0
        self.is_override = 1
        self.speed = 0.1
        self.evaluate_step = 3
        self.eval_step_list = [1, 2, 3, 4, 5]
        self.selector = 0

    def run(self):

        # NEIS SELECTOR
        pythoncom.CoInitialize()
        shell = win32.Dispatch('WScript.Shell')
        shell.AppActivate("4세대 지능형 나이스 시스템")

        # get_data_from_clipboard
        copy_data = pyperclip.paste()
        evaluate_list = [str(i) for i in copy_data.splitlines()]

        # Select which course to go
        if self.selector == 0:
            print("Error100:index id does not given")
        elif self.selector == 1:
            print("Success101:행발:종합의견 업로드를 시작합니다.")
            self.how_many_Tab = 1
        elif self.selector == 2:
            print("Success102:교과:학기말종합의견 업로드를 시작합니다.")
            self.how_many_Tab = 2
        elif self.selector == 3:
            print("Error103:행발:누가기록 업로드를 시작합니다.")
        elif self.selector == 4:
            print("Success103:교과:영역별 교과평가 업로드를 시작합니다.")
            self.how_many_Tab = 1
            evaluate_list = self.is_grade_Korean(evaluate_list)[:]

        # do something by one data
        for i, data in enumerate(evaluate_list):
            for tab in range(self.how_many_Tab):
                shell.SendKeys('{TAB}')
                time.sleep(self.speed)

            if (self.selector == 1) or (self.selector == 2):
                # do override or addride
                if self.is_override == 1:
                    # 덮어쓰기
                    pyautogui.keyDown('ctrl')
                    pyautogui.press('a')
                    pyautogui.keyUp('ctrl')
                    pyautogui.press('del')
                else:
                    # 이어쓰기
                    pyautogui.press('end')
                    pyautogui.press('space')
                time.sleep(self.speed)

                # copy
                data = data.strip()
                pyperclip.copy(data)
                time.sleep(self.speed)

                # paste
                pyautogui.keyDown('ctrl')
                pyautogui.press('v')
                pyautogui.keyUp('ctrl')
                time.sleep(self.speed)

                # move to next row
                shell.SendKeys('{TAB}')
                time.sleep(self.speed)
            elif self.selector == 4:
                for grade in range(self.eval_step_list[int(data)]):
                    shell.SendKeys('{DOWN}')
                    time.sleep(self.speed * 3)

                shell.SendKeys('{TAB}')
                time.sleep(self.speed)
                shell.SendKeys('{TAB}')
                time.sleep(self.speed)

        self.threadEvent.emit()

    @staticmethod
    def is_grade_Korean(data: list = None) -> list:
        grade_data = []
        grade_dict = {'상': 0,
                      '중': 1,
                      '하': 2}
        if ("최상" in data):
            for item in data:
                try:
                    if item == '최상':
                        grade_data.append(0)
                    else:
                        grade_data.append(grade_dict[item] + 1)
                except (KeyError, ValueError):
                    grade_data.append(0)

        elif ("상" in data) or ("중" in data) or ("하" in data):
            try:
                for item in data:
                    grade_data.append(grade_dict[item])
            except (KeyError, ValueError):
                grade_data.append(0)
        else:
            try:
                for item in data:
                    grade_data.append(int(item))
            except (KeyError, ValueError):
                grade_data.append(0)

        return grade_data


"""
class remove:       
    def run_gyogwa_step(self, step: int = 3):
        print("교과:영역별 교과평가를 업로드 합니다.")
        evaluate_step = list(range(step + 1))

        self.shell = self.NEIS_activate()
        self.copy_entire_data_from_xlsx = self.get_data_from_clipboard()
        
        for i, data in enumerate(self.copy_entire_data_from_xlsx):
            self.send_tabs(how_many_Tab=1)

            for j in range(evaluate_step[data]):
                self.shell.SendKeys('{DOWN}')
                time.sleep(self.speed * 2)

            if i == len(self.copy_entire_data_from_xlsx) - 1:
                break
            else:
                self.send_tabs(how_many_Tab=3)
            
# -----------------------------------------------------------------------------
        # 행발:종합의견 업로드
        if index == 1:

            # 교과별 상중하 입력 -> select = 1 : 3단계 / select = 2 : 4단계
            if select == 1 or select == 2:
                if select == 1:
                    inputCount = [0, 1, 2, 3]
                else:
                    inputCount = [0, 1, 2, 3, 4]

                for i, data in enumerate(self.copy_entire_data_from_xlsx):
                    shell.SendKeys('{TAB}')
                    time.sleep(self.speed * 3)

                    for j in range(inputCount[data]):
                        shell.SendKeys('{DOWN}')
                        time.sleep(self.speed * 2)

                    if i == len(self.copy_entire_data_from_xlsx) - 1:
                        break
                    else:
                        shell.SendKeys('{TAB}')
                        shell.SendKeys('{TAB}')
                        shell.SendKeys('{TAB}')
                        time.sleep(self.speed * 3)

            # 행발/교과/창체 학기말 입력 -> 
            # select = 3 : 행발 / 
            # select = 4 : 교과 / 
            # select = 5,15 : 자동봉진 /
            # select = 7,17 : 청소년단체 /

            # ---------------------------------------------------------------
            for i in range(4):
                shell.sendKeys("{TAB}")
                time.sleep(self.speed * 3)

            for i, data in enumerate(inputdate):
                shell.sendKeys("{ENTER}")
                time.sleep(self.speed * 3)

                # 마지막 요소는 이거 하면 안됨.
                if i != (len(inputdate) - 1):
                    backtab = i * 3 + 6
                    for j in range(backtab):
                        shell.sendKeys("+{TAB}")
                        time.sleep(self.speed * 3)
                elif len(inputdate) == 1:
                    shell.sendKeys("{TAB}")
                    time.sleep(self.speed * 3)
                else:
                    for i in range(len(inputdate) * 3 - 3):
                        shell.sendKeys("+{TAB}")
                        time.sleep(self.speed * 3)

            # print("    Tab 클릭완료: ", i)
            for i, data in enumerate(inputdate):
                date = str(inputdate[i])
                copytext = copy_data_one_student[i].strip()

                #  DATE INPUT
                pyperclip.copy(date)

                time.sleep(self.speed * 3)

                pyautogui.keyDown('ctrl')
                pyautogui.press('v')
                pyautogui.keyUp('ctrl')
                time.sleep(self.speed * 3)

                # 자율 등 창체 누가 혹시나 하게 되면 추가
                # if self.is_override == 1 or self.is_override == 2:
                #     shell.SendKeys('{TAB}')
                #     shell.SendKeys('{ENTER}')
                #     if self.is_override == 2:
                #         shell.SendKeys('{TAB}')
                # elif self.is_override == 3:
                #     shell.SendKeys('{TAB}')
                #     pyautogui.keyDown('ctrl')
                #     pyautogui.press('v')
                #     pyautogui.keyUp('ctrl')
                #     shell.SendKeys('{TAB}')
                #     for j in range(3):
                #         shell.SendKeys('{DOWN}')
                #     shell.SendKeys('{TAB}')
                # elif self.is_override == 10:

                shell.SendKeys('{TAB}')
                time.sleep(self.speed)
                shell.SendKeys('{TAB}')
                time.sleep(self.speed)

                #  TEXT INPUT
                pyperclip.copy(copytext)
                time.sleep(self.speed * 3)
                pyautogui.keyDown('ctrl')
                pyautogui.press('v')
                pyautogui.keyUp('ctrl')

                time.sleep(self.speed * 5)

                shell.SendKeys('{TAB}')
                time.sleep(self.speed)
                shell.SendKeys('{TAB}')
                time.sleep(self.speed)
"""