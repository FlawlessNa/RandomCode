import os
import win32gui
import numpy as np
import win32con
import win32api
import time
import pyautogui
import pydirectinput
import random
import ctypes
from ctypes import wintypes

class ClientManager():
    # Pass in the IGN of the client this instance should control
    def __init__(self, config, ign):
        self.config = config
        self.ign = ign
        if eval(self.config.get(section='Startup Config', option='open_clients')):
            username, password, pic = eval(self.config.get(section='Login Credentials', option='credentials'))[self.ign]
            self.open(char_type=self.get_char_type())
            self.login(username, password, pic)
            # When login through python, default channel will be 8 automatically
            self.set_current_channel(8)
        self.client = self.get_window_from_ign(ign)
        self.reposition_client(eval(self.config.get(section='Clients Positioning', option='position_dict'))[self.ign])
        self.hwnd = self.client._hWnd

    def get_char_type(self):
        return eval(self.config.get(section='IGN', option='ign_dict'))[self.ign]

    def open(self, char_type):
        # Apparently, opening the 800x600 doesnt work, but we can instead open the shortcut on the Desktop and it works..
        # Also Interesting Note: using os.system would also cause the client to run, and the client is automatically killed once the execution of the program ends!

        if eval(self.config.get(section='Kill Clients After Execution', option='value')):
            os.system(eval(self.config.get(section='Client Path', option='path'))[self.config.get(section='RESOLUTIONS', option=char_type)])
        else:
            os.startfile(eval(self.config.get(section='Client Path', option='path'))[self.config.get(section='RESOLUTIONS', option=char_type)])
        time.sleep(10)

    def login(self, username, pw, pic):
        # Note: For now, login automatically defaults into channel 8
        pyautogui.keyDown('shiftleft')
        pyautogui.press('tab')
        pyautogui.keyUp('shiftleft')
        pyautogui.write(username)
        pyautogui.press('tab')
        pyautogui.write(pw)
        pyautogui.press('enter')
        time.sleep(3)
        pyautogui.press('enter')
        time.sleep(1)
        x, y = pyautogui.locateCenterOnScreen(self.config.get(section='Login Images', option='channel_to_click'))
        pyautogui.doubleClick(x, y+5)
        time.sleep(1)
        nbr_move_towards_right = eval(self.config.get(section='Login Character Position', option='position_dict'))[self.ign] - 1

        for i in range(nbr_move_towards_right):
            pyautogui.press('right')
            time.sleep(0.05)
        pyautogui.press('enter')
        list_keys = eval(self.config.get(section='Login Images', option='pic_keys'))
        time.sleep(2)

        for key in pic:
            x, y = pyautogui.locateCenterOnScreen(list_keys[[key in i for i in list_keys].index(True)])
            pyautogui.click(x, y)
            # Must move away the cursor such that it doesn't hinder the next call to locateOnScreen
            pyautogui.moveTo(random.randint(1500, 2000), random.randint(1000, 1400), 0.3, pyautogui.easeInQuad)
            time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(4)

    def reposition_client(self, position):
        x, y = position
        self.client.moveTo(x, y)

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
        ign_dict = eval(self.config.get(section='IGN', option='ign_dict'))
        assert ign in ign_dict.keys(), "The IGN provided is not in the configured list"
        char_type = self.get_char_type()

        all_windows = pyautogui.getWindowsWithTitle('MapleRoyals')
        try:
            image = eval(self.config.get(section='IGN Images', option=char_type))[ign]
        except NameError:
            image = self.config.get(section='IGN Images', option=char_type)

        for client in all_windows:

            # pyautogui only handles the primary monitor. It will return an error for a client that is not in primary
            client.show()
            if any([coordinate < 0 for coordinate in client.box]):
                continue
            if pyautogui.locateOnScreen(image=image, region=client.box):
                return client

    def toggle_character_stats(self):

        key, extended_param = eval(self.config.get(section='KEYBINDS - Common', option='characterstatskey'))

        lparam_keydown = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYDOWN, extended_key=extended_param, previous_key_state=0)
        lparam_keyup = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYUP, extended_key=extended_param)

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, key, lparam_keydown)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, key, lparam_keyup)

    def get_char_speed(self):
        # TODO: read in actual speed from the character stats menu
        try:
            return self.char_speed
        except AttributeError:
            self.char_speed = eval(self.config.get(section='Character Speed', option='speed_dict'))[self.ign]
            return self.char_speed


    def move_right_by(self, distance):
        # 1 sec is approximately equal to 200 pixel when character has 140% speed.
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_right_for(time)

    def move_left_by(self, distance):
        # 1 sec is approximately equal to 200 pixel when character has 140% speed.
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_left_for(time)

    def move_up_by(self, distance):
        # 1 sec is approximately equal to 200 pixel when character has 140% speed.
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_up_for(time)

    def move_down_by(self, distance):
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_left_for(time)

    def move_right_for(self, duration):
        self.client.activate()
        pydirectinput.keyDown('right')
        time.sleep(duration)
        pydirectinput.keyUp('right')

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
        pydirectinput.keyDown('up')
        time.sleep(duration)
        pydirectinput.keyUp('up')

    def move_down_for(self, duration):
        self.client.activate()
        pydirectinput.keyDown('down')
        time.sleep(duration)
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

        key, extended_param = eval(self.config.get(section='KEYBINDS - Common', option='jumpkey'))

        lparam_keydown = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_SYSKEYDOWN, extended_key=extended_param, previous_key_state=0)
        lparam_keyup = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_SYSKEYUP, extended_key=extended_param)

        win32api.PostMessage(self.hwnd, win32con.WM_SYSKEYDOWN, key, lparam_keydown)
        win32api.PostMessage(self.hwnd, win32con.WM_SYSKEYUP, key, lparam_keyup)

    def jump_for(self, duration):

        key, extended_param = eval(self.config.get(section='KEYBINDS - Common', option='jumpkey'))

        lparam_keydown_ini = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_SYSKEYDOWN, extended_key=extended_param, previous_key_state=0)

        lparam_keydown = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_SYSKEYDOWN, extended_key=extended_param, previous_key_state=1)
        lparam_keyup = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_SYSKEYUP, extended_key=extended_param)

        now = time.time()

        win32api.PostMessage(self.hwnd, win32con.WM_SYSKEYDOWN, self.config['JumpKey'], lparam_keydown_ini)
        while time.time() - now < duration:
            win32api.PostMessage(self.hwnd, win32con.WM_SYSKEYDOWN, self.config['JumpKey'], lparam_keydown)
            time.sleep(0.05)
        win32api.PostMessage(self.hwnd, win32con.WM_SYSKEYUP, self.config['JumpKey'], lparam_keyup)

    def jump_right(self):
        self.client.activate()
        pydirectinput.keyDown('right')
        pydirectinput.press(self.config.get(section='KEYBINDS - Common - pyautogui', option='jumpkey'))
        pydirectinput.keyUp('right')

    def jump_left(self):
        self.client.activate()
        pydirectinput.keyDown('left')
        pydirectinput.press(self.config.get(section='KEYBINDS - Common - pyautogui', option='jumpkey'))
        pydirectinput.keyUp('left')

    def jump_down(self):
        self.client.activate()
        pydirectinput.keyDown('down')
        pydirectinput.press(self.config.get(section='KEYBINDS - Common - pyautogui', option='jumpkey'))
        pydirectinput.keyUp('down')

    def jump_right_for(self, duration):
        self.client.activate()
        now = time.time()
        pydirectinput.keyDown('right')
        while time.time() - now < duration:
            pydirectinput.press(self.config.get(section='KEYBINDS - Common - pyautogui', option='jumpkey'))
        pydirectinput.keyUp('right')

    def jump_left_for(self, duration):
        self.client.activate()
        now = time.time()
        pydirectinput.keyDown('left')
        while time.time() - now < duration:
            pydirectinput.press(self.config.get(section='KEYBINDS - Common - pyautogui', option='jumpkey'))
        pydirectinput.keyUp('left')

    def jump_down_for(self, duration):
        self.client.activate()
        now = time.time()
        pydirectinput.keyDown('down')
        while time.time() - now < duration:
            pydirectinput.press(self.config.get(section='KEYBINDS - Common - pyautogui', option='jumpkey'))
        pydirectinput.keyUp('down')

    def jump_right_until(self, expression):
        self.client.activate()
        pydirectinput.keyDown('right')
        loop = True
        while loop:
            pydirectinput.press(self.config.get(section='KEYBINDS - Common - pyautogui', option='jumpkey'))
            if eval(expression):
                pydirectinput.keyUp('right')
                loop = False

    def jump_left_until(self, expression):
        self.client.activate()
        pydirectinput.keyDown('left')
        loop = True
        while loop:
            pydirectinput.press(self.config.get(section='KEYBINDS - Common - pyautogui', option='jumpkey'))
            if eval(expression):
                pydirectinput.keyUp('left')
                loop = False

    def jump_down_until(self, expression):
        self.client.activate()
        pydirectinput.keyDown(self.config.get(section='KEYBINDS - Common - pyautogui', option='jumpkey'))
        loop = True
        while loop:
            pydirectinput.press('altleft')
            if eval(expression):
                pydirectinput.keyUp('down')
                loop = False

    def toggle_inventory(self):

        key, extended_param = eval(self.config.get(section='KEYBINDS - Common', option='inventorykey'))

        lparam_keydown = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYDOWN, extended_key=extended_param, previous_key_state=0)
        lparam_keyup = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYUP, extended_key=extended_param)

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, key, lparam_keydown)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, key, lparam_keyup)

    def click(self):
        self.client.activate()
        pydirectinput.click()

    def feed_pet(self):

        key, extended_param = eval(self.config.get(section='KEYBINDS - Common', option='petfoodkey'))

        lparam_keydown = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYDOWN, extended_key=extended_param, previous_key_state=0)
        lparam_keyup = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYUP, extended_key=extended_param)

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, key, lparam_keydown)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, key, lparam_keyup)

    def feed_multiple_pets(self, nbr_press):
        for i in range(nbr_press):
            self.feed_pet()

    def click_at(self, x, y):
        self.client.activate()
        pydirectinput.click(x, y)

    def move_cursor_to(self, x, y):
        pass

    def check_pots_left(self):
        pass

    def type_message(self, message):

        # This assume all characters are "standard" (from A-Z, 0-9)
        for char in message:
            lparam_char = self.construct_lparams(repeat_count=1, key=ord(char), wm_command=win32con.WM_KEYDOWN, extended_key=0, previous_key_state=0)
            win32api.PostMessage(self.hwnd, win32con.WM_CHAR, ord(char), lparam_char)
            time.sleep(0.05)

        lparam_keydown_enter = self.construct_lparams(repeat_count=1, key=win32con.VK_RETURN, wm_command=win32con.WM_KEYDOWN, extended_key=0, previous_key_state=0)
        lparam_keyup_enter = self.construct_lparams(repeat_count=1, key=win32con.VK_RETURN, wm_command=win32con.WM_KEYUP, extended_key=0)

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, lparam_keydown_enter)
        time.sleep(0.05)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, lparam_keyup_enter)

        lparam_keydown_esc = self.construct_lparams(repeat_count=1, key=win32con.VK_ESCAPE, wm_command=win32con.WM_KEYDOWN, extended_key=0, previous_key_state=0)
        lparam_keyup_esc = self.construct_lparams(repeat_count=1, key=win32con.VK_ESCAPE, wm_command=win32con.WM_KEYUP, extended_key=0)

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, win32con.VK_ESCAPE, lparam_keydown_esc)
        time.sleep(0.05)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, win32con.VK_ESCAPE, lparam_keyup_esc)

    def allchat(self):
        key, extended_param = eval(self.config.get(section='KEYBINDS - Common', option='allchatkey'))

        lparam_keydown = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYDOWN, extended_key=extended_param, previous_key_state=0)
        lparam_keyup = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYUP, extended_key=extended_param)

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, key, lparam_keydown)
        time.sleep(0.05)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, key, lparam_keyup)

    def mapowner(self):

        self.allchat()
        self.type_message('~mapowner')


    def get_current_channel(self):
        if self.current_channel is None:
            pass
        else:
            return self.current_channel

    def set_current_channel(self, channel):
        self.current_channel = channel

    def change_channel(self, destination):

        channels_table = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12], [13, 14, 15, 16, 17, 18], [19, 20, np.nan, np.nan, np.nan, np.nan]])
        nbr_keys = self.get_current_channel() - destination

        lparam_keydown_esc = self.construct_lparams(repeat_count=1, key=win32con.VK_ESCAPE, wm_command=win32con.WM_KEYDOWN, extended_key=0, previous_key_state=0)
        lparam_keyup_esc = self.construct_lparams(repeat_count=1, key=win32con.VK_ESCAPE, wm_command=win32con.WM_KEYUP, extended_key=0)
        lparam_keydown_enter = self.construct_lparams(repeat_count=1, key=win32con.VK_RETURN, wm_command=win32con.WM_KEYDOWN, extended_key=0, previous_key_state=0)
        lparam_keyup_enter = self.construct_lparams(repeat_count=1, key=win32con.VK_RETURN, wm_command=win32con.WM_KEYUP, extended_key=0)

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, win32con.VK_ESCAPE, lparam_keydown_esc)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, win32con.VK_ESCAPE, lparam_keyup_esc)
        time.sleep(0.05)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, lparam_keydown_enter)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, lparam_keyup_enter)
        time.sleep(0.05)

        if nbr_keys < 0:
            lparam_keydown = self.construct_lparams(repeat_count=1, key=win32con.VK_RIGHT, wm_command=win32con.WM_KEYDOWN, extended_key=1, previous_key_state=0)
            lparam_keyup = self.construct_lparams(repeat_count=1, key=win32con.VK_RIGHT, wm_command=win32con.WM_KEYUP, extended_key=1)

            for i in range(abs(nbr_keys)):
                win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT, lparam_keydown)
                win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, win32con.VK_RIGHT, lparam_keyup)
                time.sleep(0.05)

        elif nbr_keys > 0:
            lparam_keydown = self.construct_lparams(repeat_count=1, key=win32con.VK_LEFT, wm_command=win32con.WM_KEYDOWN, extended_key=1, previous_key_state=0)
            lparam_keyup = self.construct_lparams(repeat_count=1, key=win32con.VK_LEFT, wm_command=win32con.WM_KEYUP, extended_key=1)

            for i in range(nbr_keys):
                win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, win32con.VK_LEFT, lparam_keydown)
                win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, win32con.VK_LEFT, lparam_keyup)
                time.sleep(0.05)

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, lparam_keydown_enter)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, lparam_keyup_enter)
        self.set_current_channel(destination)

    def leave_party(self):
        # This is to reset the entire party to make sure it is properly set
        self.allchat()
        self.type_message('/leaveparty')

    def remake_party(self):
        pass
