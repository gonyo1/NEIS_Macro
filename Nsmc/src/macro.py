import os
import win32com
from ctypes import windll
import win32com.client as win32
import pyperclip
import pyautogui
# import pythoncom
import time


def get_form_file():
    path = os.path.realpath("./Nsmc/src/data")
    os.startfile(path)


def show_how_to_use():
    path = os.path.realpath("./Nsmc/src/img/howtocopy.png")
    os.startfile(path)


class run_upload:
    # 기본 데이터
    copy_entire_data_from_xlsx = []
    copy_data_one_student = ''
    web_title = "4세대 지능형 나이스 시스템"
    how_many_Tab = 0
    is_override = 1
    speed = 0.1

    def __init__(self):
        self.shell = None

    def NEIS_activate(self):
        shell = win32.Dispatch('WScript.Shell')
        shell.AppActivate(self.web_title)

        return shell

    @staticmethod
    def get_data_from_clipboard():
        copy_data = pyperclip.paste()
        evaluate_list = [str(i) for i in copy_data.splitlines()]

        return evaluate_list

    def send_tabs(self, how_many_Tab: int = 0):
        for i in range(how_many_Tab):
            self.shell.SendKeys('{TAB}')
            time.sleep(self.speed)
        time.sleep(self.speed * 3)

    def copy_and_paste_data_to_NEIS(self, data):
        # copy
        data = data.strip()
        pyperclip.copy(data)
        time.sleep(self.speed * 3)

        # paste
        pyautogui.keyDown('ctrl')
        pyautogui.press('v')
        pyautogui.keyUp('ctrl')
        pyautogui.press('tab')
        time.sleep(self.speed * 3)

    def run_haengbal_final(self):
        print("행발:종합의견을 업로드 합니다.")
        self.shell = self.NEIS_activate()
        self.copy_entire_data_from_xlsx = self.get_data_from_clipboard()

        for i, data in enumerate(self.copy_entire_data_from_xlsx):
            self.send_tabs(how_many_Tab=1)

            # is_override -> 덮어쓰기 : 1 / 이어쓰기 : 2
            if not self.is_override == 1:
                pyautogui.press('end')
                pyautogui.press('space')

            self.copy_and_paste_data_to_NEIS(data)


    def run_gyogwa_final(self):
        print("교과:학기말종합의견을 업로드 합니다.")
        self.shell = self.NEIS_activate()
        self.copy_entire_data_from_xlsx = self.get_data_from_clipboard()

        for i, data in enumerate(self.copy_entire_data_from_xlsx):
            self.send_tabs(how_many_Tab=2)

            if self.is_override == 1:  # 교과 / 창체 / 덮어쓰기
                pyautogui.keyDown('ctrl')
                pyautogui.press('a')
                pyautogui.keyUp('ctrl')
                pyautogui.press('del')
            else:
                pyautogui.press('end')
                pyautogui.press('space')

            self.copy_and_paste_data_to_NEIS(data)
            
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
