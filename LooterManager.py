from ClientManager import ClientManager
import pyautogui
import pydirectinput
import time
import win32api
import win32con
from PostMessage import pyPostMessage


# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
# http://www.kbdedit.com/manual/low_level_vk_list.html

class LooterManager(ClientManager):

    def __init__(self, config, ign):
        super().__init__(config, ign)

    def use_stance(self):

        key_config = eval(self.config.get(section='KEYBINDS - Looter', option='stancekey'))
        pyPostMessage('press', key_config, self.hwnd)
        time.sleep(0.8)

    def chat_feed_is_displayed(self):
        if pyautogui.locateOnScreen(image='KeyImages/Feed_is_Displayed.png', region=self.client.box) is not None:
            return True
        elif pyautogui.locateOnScreen(image='KeyImages/Feed_is_not_Displayed.png', region=self.client.box) is not None:
            return False
        else:
            return None

    def feed_mount(self):

        key_config = eval(self.config.get(section='KEYBINDS - Looter', option='mountfoodkey'))
        if self.ensure_mount_is_used():
            time.sleep(0.4)

        pyPostMessage('press', key_config, self.hwnd)

    def toggle_mount(self):

        key_config = eval(self.config.get(section='KEYBINDS - Looter', option='mountkey'))
        pyPostMessage('press', key_config, self.hwnd)

    def ensure_mount_is_used(self):

        if pyautogui.locateOnScreen(image=self.config.get(section='Mount Image', option='mount_icon'), region=self.client.box, confidence=0.95) is None:
            self.toggle_mount()
            return 1
        return 0

    def map_sequence_1(self):

        cond1 = """pyautogui.locateOnScreen(image=self.config.get(section='Character Images', option='looter_backhead'), region=self.client.box, confidence=0.9) != None"""
        self.jump_right_for(5)
        self.move_right_and_down_until(expression=cond1)

        pydirectinput.keyDown('up')
        time.sleep(0.5)
        pydirectinput.keyUp('up')
        # self.move_up_until(expression=cond2)

    def map_sequence_2(self):

        cond1 = """pyautogui.locateOnScreen(image=self.config.get(section='Map Images', option='target_sequence_2'), region=self.client.box, confidence=0.9) != None"""
        self.jump_left_until(expression=cond1)
        time.sleep(0.2)
        self.jump()
        time.sleep(1.5)

    def map_sequence_3(self):

        cond1 = """pyautogui.locateOnScreen(image=self.config.get(section='Character Images', option='looter_backhead'), region=self.client.box, confidence=0.9) != None"""
        self.jump_right_for(4)
        self.move_right_and_down_until(expression=cond1)
        self.move_down_for(0.4)
        self.jump_left()
        time.sleep(1)

    def map_sequence_4(self):

        cond1 = """pyautogui.locateOnScreen(image=self.config.get(section='Map Images', option='target_sequence_4'), region=self.client.box, confidence=0.9) != None"""
        self.jump_down()
        time.sleep(0.6)
        self.jump_down()
        time.sleep(1)
        self.move_left_until(expression=cond1)
