import os
import win32gui
import win32con
import win32api
import time
import pyautogui
import pydirectinput
import ctypes
from ctypes import wintypes

# USE pyautogui -- it has everything we need!
config = {'IGN_LIST': ['Guarding', 'ShyPooper', 'LegalizeIt', 'Goldmine1', 'Goldmine2', 'Goldmine3', 'Buccanoid'],
          'Guarding':'KeyImages/Guarding_IGN.png',
          'LegalizeIt': 'KeyImages/LegalizeIt_IGN.png',
          'Goldmine1': 'KeyImages/Goldmine1_IGN.png'}

class ClientManager():
    # Pass in the IGN of the client this instance should control
    def __init__(self, config):
        self.client = self.get_window_from_ign(config['IGN'])
        self.hwnd = self.client._hWnd
        self.config = config

    def open(self, resolution):
        pass

    def construct_lparams(self, repeat_count, key, wm_command, extended_key, previous_key_state=1, scan_code=None):

        assert repeat_count < 2 ** 16

        if scan_code is None:
            scan_code = win32api.MapVirtualKey(key, 0)

        if wm_command == win32con.WM_KEYDOWN:
            context_code = 0
            transition_state = 0

        elif wm_command == win32con.WM_KEYUP:
            context_code = 0
            transition_state = 1

        elif wm_command == win32con.WM_SYSKEYDOWN:
            if key == win32con.VK_MENU:
                context_code = 1
            else:
                context_code = 0
            transition_state = 0

        elif wm_command == win32con.WM_SYSKEYUP:
            if key == win32con.VK_MENU:
                context_code = 1
            else:
                context_code = 0
            transition_state = 1

        else:
            pass

        return int(format(transition_state, '01b') + format(previous_key_state, '01b') + format(context_code, '01b') + format(0, '04b') + \
               format(extended_key, '01b') + format(scan_code, '08b') + format(repeat_count, '016b'), base=2)

    def get_window_from_ign(self, ign):
        # TODO create actual config file
        assert ign in config['IGN_LIST'], "The IGN provided is not in the configured list"
        all_windows = pyautogui.getWindowsWithTitle('MapleRoyals')

        for client in all_windows:

            # pyautogui only handles the primary monitor. It will return an error for a client that is not in primary
            client.show()
            if any([coordinate < 0 for coordinate in client.box]):
                continue
            if pyautogui.locateOnScreen(image=config[ign], region=client.box):
                return client

    def move_right_by(self, distance):
        pass

    def move_left_by(self, distance):
        pass

    def move_up_by(self, distance):
        pass

    def move_down_by(self, distance):
        pass

    def move_right_for(self, duration):
        self.client.activate()
        pydirectinput.keyDown('right')
        time.sleep(duration)
        pydirectinput.keyUp('right')

        # lparam_keydown = self.construct_lparams(repeat_count=1, key=win32con.VK_RIGHT, wm_command=win32con.WM_KEYDOWN, extended_key=0,
        #                                         previous_key_state=0)
        # lparam_keyup = self.construct_lparams(repeat_count=1, key=win32con.VK_RIGHT, wm_command=win32con.WM_KEYUP, extended_key=0)
        #
        # win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT, lparam_keydown)
        # time.sleep(duration)
        # win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, win32con.VK_RIGHT, lparam_keyup)

    def move_left_for(self, duration):
        self.client.activate()
        pydirectinput.keyDown('left')
        time.sleep(duration)
        pydirectinput.keyUp('left')

    def move_up(self):
        lparam_keydown = self.construct_lparams(repeat_count=1, key=win32con.VK_UP, wm_command=win32con.WM_KEYDOWN, extended_key=1,
                                                previous_key_state=0)
        lparam_keyup = self.construct_lparams(repeat_count=1, key=win32con.VK_UP, wm_command=win32con.WM_KEYUP, extended_key=1)

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, win32con.VK_UP, lparam_keydown)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, win32con.VK_UP, lparam_keyup)


    def move_up_for(self, duration):
        self.client.activate()
        now = time.time()
        pydirectinput.keyDown('up')
        while time.time() - now < duration:
            pass
        pydirectinput.keyUp('up')

    def move_down_for(self, duration):
        self.client.activate()
        now = time.time()
        pydirectinput.keyDown('down')
        while time.time() - now < duration:
            pass
        pydirectinput.keyUp('down')

    def move_right_until(self, expression):
        self.client.activate()
        pydirectinput.keyDown('right')

        loop = True
        while loop:
            if eval(expression):
                pydirectinput.keyUp('right')
                loop = False

    def move_left_until(self, expression):
        self.client.activate()
        pydirectinput.keyDown('left')

        loop = True
        while loop:
            if eval(expression):
                pydirectinput.keyUp('left')
                loop = False

    def move_up_until(self, expression):
        self.client.activate()
        pydirectinput.keyDown('up')

        loop = True
        while loop:
            if eval(expression):
                pydirectinput.keyUp('up')
                loop = False

    def move_down_until(self, expression, stop_when):
        self.client.activate()
        pydirectinput.keyDown('down')

        loop = True
        while loop:
            if eval(expression):
                pydirectinput.keyUp('down')
                loop = False

    def move_right_and_down_until(self, expression):
        self.client.activate()
        pydirectinput.keyDown('right')
        pydirectinput.keyDown('down')

        loop = True
        while loop:
            if eval(expression):
                pydirectinput.keyUp('right')
                pydirectinput.keyUp('down')
                loop = False

    def move_left_and_down_until(self, expression):
        self.client.activate()
        pydirectinput.keyDown('left')
        pydirectinput.keyDown('down')

        loop = True
        while loop:
            if eval(expression):
                pydirectinput.keyUp('left')
                pydirectinput.keyUp('down')
                loop = False

    def jump(self):

        lparam_keydown = self.construct_lparams(repeat_count=1, key=self.config['JumpKey'], wm_command=win32con.WM_SYSKEYDOWN, extended_key=self.config['JumpKeyExt'], previous_key_state=0)
        lparam_keyup = self.construct_lparams(repeat_count=1, key=self.config['JumpKey'], wm_command=win32con.WM_SYSKEYUP, extended_key=self.config['JumpKeyExt'])

        win32api.PostMessage(self.hwnd, win32con.WM_SYSKEYDOWN, self.config['JumpKey'], lparam_keydown)
        win32api.PostMessage(self.hwnd, win32con.WM_SYSKEYUP, self.config['JumpKey'], lparam_keyup)

    def jump_for(self, duration):

        lparam_keydown_ini = self.construct_lparams(repeat_count=1, key=self.config['JumpKey'], wm_command=win32con.WM_SYSKEYDOWN, extended_key=self.config['JumpKeyExt'],
                                                    previous_key_state=0)

        lparam_keydown = self.construct_lparams(repeat_count=1, key=self.config['JumpKey'], wm_command=win32con.WM_SYSKEYDOWN, extended_key=self.config['JumpKeyExt'],
                                                previous_key_state=1)

        lparam_keyup = self.construct_lparams(repeat_count=1, key=self.config['JumpKey'], wm_command=win32con.WM_SYSKEYUP, extended_key=self.config['JumpKeyExt'])

        now = time.time()

        win32api.PostMessage(self.hwnd, win32con.WM_SYSKEYDOWN, self.config['JumpKey'], lparam_keydown_ini)
        while time.time() - now < duration:
            win32api.PostMessage(self.hwnd, win32con.WM_SYSKEYDOWN, self.config['JumpKey'], lparam_keydown)
            time.sleep(0.05)
        win32api.PostMessage(self.hwnd, win32con.WM_SYSKEYUP, self.config['JumpKey'], lparam_keyup)

    def jump_right(self):
        self.client.activate()
        pydirectinput.keyDown('right')
        pydirectinput.press('altleft')
        pydirectinput.keyUp('right')

    def jump_left(self):
        self.client.activate()
        pydirectinput.keyDown('left')
        pydirectinput.press('altleft')
        pydirectinput.keyUp('left')

    def jump_down(self):
        self.client.activate()
        pydirectinput.keyDown('down')
        pydirectinput.press('altleft')
        pydirectinput.keyUp('down')

    def jump_right_for(self, duration):
        self.client.activate()
        now = time.time()
        pydirectinput.keyDown('right')
        while time.time() - now < duration:
            pydirectinput.press('altleft')
        pydirectinput.keyUp('right')

    def jump_left_for(self, duration):
        self.client.activate()
        now = time.time()
        pydirectinput.keyDown('left')
        while time.time() - now < duration:
            pydirectinput.press('altleft')
        pydirectinput.keyUp('left')

    def jump_down_for(self, duration):
        self.client.activate()
        now = time.time()
        pydirectinput.keyDown('down')
        while time.time() - now < duration:
            pydirectinput.press('altleft')
        pydirectinput.keyUp('down')

    def jump_right_until(self, expression):
        self.client.activate()
        pydirectinput.keyDown('right')
        loop = True
        while loop:
            pydirectinput.press('altleft')
            if eval(expression):
                pydirectinput.keyUp('right')
                loop = False

    def jump_left_until(self, expression):
        self.client.activate()
        pydirectinput.keyDown('left')
        loop = True
        while loop:
            pydirectinput.press('altleft')
            if eval(expression):
                pydirectinput.keyUp('left')
                loop = False

    def jump_down_until(self, expression):
        self.client.activate()
        pydirectinput.keyDown('down')
        loop = True
        while loop:
            pydirectinput.press('altleft')
            if eval(expression):
                pydirectinput.keyUp('down')
                loop = False

    def toggle_inventory(self):
        self.client.activate()
        pydirectinput.press('i')

    def click(self):
        self.client.activate()
        pydirectinput.click()

    def feed_pets(self):
        self.client.activate()
        pydirectinput.press('7')

    def click_at(self, x, y):
        self.client.activate()
        pydirectinput.click(x, y)

    def mapowner(self):
        self.client.activate()
        pydirectinput.press('1')
        pydirectinput.keyDown('shiftleft')
        pydirectinput.press('`')
        pydirectinput.keyUp('shiftleft')
        pydirectinput.write('mapowner')
        pydirectinput.press('enter')
        pydirectinput.press('esc')
