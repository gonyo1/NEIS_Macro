# python internal packages
import sys
import time
import os, glob



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


class MacroThread(QThread):
    threadEvent = pyqtSignal()
    uploader = None

    def __init__(self, parent=None):
        super().__init__()
        # 기본 데이터
        self.main = parent
        self.copy_entire_data_from_xlsx = []
        self.copy_data_one_student = ''
        self.web_title = "4세대 나이스 시스템"
        self.init_tab_count = 0
        self.is_override = "ON"
        self.speed = 0.1
        self.evaluate_step = 3
        self.eval_step_list = [1, 2, 3, 4, 5]
        self.selector = 0
        self._check_name = None

    @staticmethod
    def delete_double_space(text: str = ""):
        text = text.strip()

        while True:
            if "  " in text:
                text = text.replace("  ", " ")
            else:
                break
        return text

    def run(self):
        # NEIS SELECTOR
        pythoncom.CoInitialize()
        shell = win32.Dispatch('WScript.Shell')

        # MACRO CLASS CALL
        self.key_event = KeyEvent(shell)

        # GET DATA FROM CLIPBOARD
        data = pyperclip.paste()
        data_list = [self.delete_double_space(text) for text in set_copied_data_to_list(self.selector, data)]
        print(data_list)

        # SET INIT TAB COUNT
        self.init_tab_count = self.set_init_tab_count(self.selector)

        # UPLOAD ONE BY ONE
        for index, data in enumerate(data_list):
            # PRESS AS NEED AS INITALIZE
            shell.AppActivate("4세대 나이스 시스템")
            self.key_event.tab(repeat_count=self.init_tab_count)

            # DO TASKS BY SELECTOR NUMBER
            if (self.selector == 1) or (self.selector == 2):
                # SET WRITING TYPE
                self.key_event.writing_type(mode=self.is_override)

                # DO TASKS
                self.key_event.copy(data=data)
                self.key_event.paste()
                self.key_event.move_to_next_row()

            elif self.selector == 3:

                while True:
                    # Web name check
                    self.key_event.press_copy()
                    name = pyperclip.paste()
                    name = str(name.split("\t")[1]).split("\n")[0].replace("\r", '')

                    # data name check
                    check_name = str(data[1].split(" ")[-1].strip())
                    print("web nams is ", name, "data name is", check_name)

                    if name == check_name:
                        if self._check_name == check_name:
                            print("go further")
                            self.key_event.tab(repeat_count=1)

                        print("누가기록 업로드를 시작합니다.")
                        # [행추가] 클릭하기
                        self.key_event.tab(repeat_count=6)
                        self.key_event.space()
                        self.key_event.tab(repeat_count=1)

                        # DATE COPY
                        self.key_event.copy(data[0])
                        self.key_event.paste()
                        self.key_event.tab(repeat_count=2)

                        # SCRIPT COPY
                        self.key_event.copy(data[3])
                        self.key_event.paste()

                        # CHECK IF REGISTERED ALREADY
                        self.key_event.shift_tab(repeat_count=7, slow=3)
                        self.key_event.press_copy()
                        line = str(pyperclip.paste())

                        try:
                            how_many = int(line.split("\t")[1])
                        except Exception as e:
                            print(e)
                            self.key_event.tab(repeat_count=5)
                            how_many = 1

                        # GO TO SAVE BUTTON
                        for i in range(how_many):
                            self.key_event.shift_tab(repeat_count=4, slow=3)

                        # SAVE CLICK
                        self.key_event.space()
                        self.key_event.sleep_seconds(0.3)
                        self.key_event.space()
                        self.key_event.sleep_seconds(0.3)
                        self.key_event.shift_tab(repeat_count=7, slow=3)

                        self._check_name = check_name[:]
                        break
                    else:
                        self.key_event.down(slow=2)

            elif self.selector == 4:
                self.key_event.down(repeat_count=int(data + 1), slow=3)
                self.key_event.tab(repeat_count=2)

            elif self.selector == 5:
                self.key_event.copy(data=data)
                self.key_event.paste()
                self.key_event.move_to_next_row()

            elif self.selector == 6:
                self.key_event.copy(data=data)
                self.key_event.paste()
                self.key_event.tab()
                self.key_event.move_to_next_row()


        self.threadEvent.emit()

    @staticmethod
    def set_init_tab_count(selector):
        if selector == 1:
            print("Success101:행발:종합의견 업로드를 시작합니다.")
            return 1

        elif selector == 2:
            print("Success102:교과:학기말종합의견 업로드를 시작합니다.")
            return 2

        elif selector == 3:
            print("Error103:행발:누가기록 업로드를 시작합니다.")
            return 0

        elif selector == 4:
            print("Success104:교과:영역별 교과평가 업로드를 시작합니다.")
            return 1

        elif selector == 5:
            print("Success105:창체:학생부자료기록 업로드를 시작합니다.")
            return 1

        elif selector == 6:
            print("Success106:창체:5-6진로특기사항 업로드를 시작합니다.")
            return 1


"""
class remove:       
    def run_gyogwa_step(self, step: int = 3):
        print("교과:영역별 교과평가를 업로드 합니다.")
        evaluate_step = list(range(step + 1))

        self.shell = self.NEIS_activate()
        self.copy_entire_data_from_xlsx = self.get_data_from_clipboard()
        
        for i, data in enumerate(self.copy_entire_data_from_xlsx):
            self.send_tabs(set_init_tab_count=1)

            for j in range(evaluate_step[data]):
                self.shell.SendKeys('{DOWN}')
                time.sleep(self.speed * 2)

            if i == len(self.copy_entire_data_from_xlsx) - 1:
                break
            else:
                self.send_tabs(set_init_tab_count=3)
            
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