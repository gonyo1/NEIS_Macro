import os
import time

# python external packages
try:
    import pyperclip
except ImportError:
    os.system("pip install pyperclip")
    import pyperclip

try:
    import cv2
except ImportError:
    os.system("pip install cv2")
    import cv2

try:
    import numpy as np
except ImportError:
    os.system("pip install numpy")
    import numpy as np
    import cv2

try:
    import pyautogui
except ImportError:
    os.system("pip install pyautogui")
    import pyautogui


class KeyEvent:
    def __init__(self, shell=None, speed: float = 0.1):
        self.shell = shell
        self.speed = speed

    def copy(self, data: str = None):
        # copy
        data = data.strip()
        pyperclip.copy(data)
        time.sleep(self.speed)

    def press_copy(self):
        # paste
        pyautogui.keyDown('ctrl')
        pyautogui.press('c')
        pyautogui.keyUp('ctrl')
        time.sleep(self.speed)

    def paste(self):
        # paste
        pyautogui.keyDown('ctrl')
        pyautogui.press('v')
        pyautogui.keyUp('ctrl')
        time.sleep(self.speed)

    def down(self, repeat_count: int = 1, slow: int = 1):
        for count in range(repeat_count):
            # press tab button
            self.shell.SendKeys('{DOWN}')
            time.sleep(self.speed * slow)

    def tab(self, repeat_count: int = 1):
        for count in range(repeat_count):
            # press tab button
            self.shell.SendKeys('{TAB}')
            time.sleep(self.speed)

    def select_all(self):
        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')
        time.sleep(self.speed)

    def end(self):
        pyautogui.press('end')
        pyautogui.press('space')
        time.sleep(self.speed)

    def delete(self):
        pyautogui.press('del')
        time.sleep(self.speed)

    def space(self):
        pyautogui.press('space')
        time.sleep(self.speed * 3)

    def move_to_next_row(self):
        # move to next row // 속도 늦추기
        self.shell.SendKeys('{TAB}')
        time.sleep(self.speed * 3)

    def writing_type(self, mode: str = "ON"):
        if (mode == "ON") or (mode == "on"):
            self.select_all()
            self.delete()
        else:
            self.end()

    def click_add_button(self):
        path = os.path.abspath("Nsmc/src/img/asset/add.png")
        n = np.fromfile(path, np.uint8)
        img = cv2.imdecode(n, cv2.IMREAD_COLOR)
        add_button = pyautogui.locateOnScreen(img)

        time.sleep(self.speed * 3)
        pyautogui.click(add_button)
        time.sleep(self.speed * 3)

    def click_save_button(self):
        path = os.path.abspath("Nsmc/src/img/asset/save.png")
        n = np.fromfile(path, np.uint8)
        img = cv2.imdecode(n, cv2.IMREAD_COLOR)
        add_button = pyautogui.locateOnScreen(img)

        time.sleep(self.speed * 3)
        pyautogui.click(add_button)
        time.sleep(self.speed * 3)

    def sleep_seconds(self, second=1):
        time.sleep(self.speed * 10 * second)
