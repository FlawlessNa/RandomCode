from ClientManager import ClientManager
import pyautogui
import pydirectinput
import time
import win32api
import win32con


# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
# http://www.kbdedit.com/manual/low_level_vk_list.html

class LooterManager(ClientManager):

    def __init__(self, config, ign):
        super().__init__(config, ign)

    def use_stance(self):

        key, extended_param = eval(self.config.get(section='KEYBINDS - Looter', option='stancekey'))

        lparam_keydown = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYDOWN, extended_key=extended_param, previous_key_state=0)
        lparam_keyup = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYUP, extended_key=extended_param)

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, key, lparam_keydown)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, key, lparam_keyup)

        time.sleep(0.8)

    def chat_feed_is_displayed(self):
        if pyautogui.locateOnScreen(image='KeyImages/Feed_is_Displayed.png', region=self.client.box) is not None:
            return True
        elif pyautogui.locateOnScreen(image='KeyImages/Feed_is_not_Displayed.png', region=self.client.box) is not None:
            return False
        else:
            return None

    def feed_mount(self):

        key, extended_param = eval(self.config.get(section='KEYBINDS - Looter', option='mountfoodkey'))
        if self.ensure_mount_is_used():
            time.sleep(0.4)

        lparam_keydown = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYDOWN, extended_key=extended_param, previous_key_state=0)
        lparam_keyup = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYUP, extended_key=extended_param)

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, key, lparam_keydown)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, key, lparam_keyup)

    def toggle_mount(self):

        key, extended_param = eval(self.config.get(section='KEYBINDS - Looter', option='mountkey'))

        lparam_keydown = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYDOWN, extended_key=extended_param, previous_key_state=0)
        lparam_keyup = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYUP, extended_key=extended_param)

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, key, lparam_keydown)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, key, lparam_keyup)

    def ensure_mount_is_used(self):

        if pyautogui.locateOnScreen(image=self.config.get(section='Mount Image', option='mount_icon'), region=self.client.box, confidence=0.99) is None:
            self.toggle_mount()
            return 1
        return 0

    def map_sequence_1(self):

        cond1 = """pyautogui.locateOnScreen(image='KeyImages/MapNavigation/BackHead.png',
                                        region=self.client.box,
                                        confidence=0.9) != None"""

        self.jump_right_for(5)
        self.move_right_and_down_until(expression=cond1)

        pydirectinput.keyDown('up')
        time.sleep(0.3)
        pydirectinput.keyUp('up')
        # self.move_up_until(expression=cond2)

    def map_sequence_2(self):

        cond1 = """pyautogui.locateOnScreen(image='KeyImages/MapNavigation/Target_Sequence2_Pole.png',
                                        region=self.client.box,
                                        confidence=0.9) != None"""
        self.jump_left_until(expression=cond1)
        time.sleep(0.2)
        self.jump()
        time.sleep(1.5)

    def map_sequence_3(self):

        cond1 = """pyautogui.locateOnScreen(image='KeyImages/MapNavigation/BackHead.png',
                                        region=self.client.box,
                                        confidence=0.9) != None"""
        self.jump_right_for(5)
        self.move_right_and_down_until(expression=cond1)
        self.move_down_for(0.4)
        self.jump_left()
        time.sleep(1)

    def map_sequence_4(self):

        cond1 = """pyautogui.locateOnScreen(image='KeyImages/MapNavigation/Target_Sequence4_Portal.png',
                                        region=self.client.box,
                                        confidence=0.9) != None"""
        # self.jump_down_until(expression=cond1)
        self.jump_down()
        time.sleep(0.6)
        self.jump_down()
        time.sleep(1)
        self.move_left_until(expression=cond1)


# Guarding = LooterManager(config=configurations)
# Guarding.use_stance()
# Guarding.ensure_mount_is_used()
# Guarding.map_sequence_1()
# Guarding.map_sequence_2()
# Guarding.map_sequence_3()
# Guarding.map_sequence_4()
# print('ok')
