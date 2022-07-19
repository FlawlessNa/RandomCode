import pydirectinput
import win32con
import time
from PostMessage import pyPostMessage
from BaseClient import BaseClient
from ImageDetection import find_image
import cv2
import win32gui
from pygetwindow import PyGetWindowException


class BasicMovements(BaseClient):

    def __init__(self, config, ign):
        super().__init__(config, ign)

    def get_char_speed(self):
        # TODO: read in actual speed from the character stats menu
        try:
            return self.char_speed
        except AttributeError:
            self.char_speed = eval(self.config.get(section='Character Speed', option='speed_dict'))[self.ign]
            return self.char_speed

    def activate(self):
        try:
            self.client.activate()
        except PyGetWindowException:
            x, y = win32gui.ClientToScreen(self.hwnd, (int(self.client.width/2), int(self.client.height/2)))
            self.click_at(x, y)

    def move_up(self):

        key_config = [win32con.VK_UP, 1]
        pyPostMessage('press', key_config, self.hwnd)

    def move_up_by(self, distance):
        # 1 sec is approximately equal to 200 pixel when character has 170% speed.
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_up_for(time)

    def move_up_for(self, duration):
        self.activate()
        pydirectinput.keyDown('up')
        time.sleep(duration)
        pydirectinput.keyUp('up')

    def click_at(self, x, y):
        pass

    def move_up_until(self, expression, timeout=None):
        self.activate()
        pydirectinput.keyDown('up')
        beginning = time.time()

        while True:
            if eval(expression):
                pydirectinput.keyUp('up')
                time.sleep(0.25)
                if eval(expression):
                    break
                else:
                    pydirectinput.keyDown('up')
            elif timeout:
                if time.time() > beginning + timeout:
                    pydirectinput.keyUp('up')
                    break

    def move_down_by(self, distance):
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_left_for(time)

    def move_down_for(self, duration):
        self.activate()
        pydirectinput.keyDown('down')
        time.sleep(duration)
        pydirectinput.keyUp('down')

    def move_down_until(self, expression, timeout=None):
        self.activate()
        pydirectinput.keyDown('down')
        beginning = time.time()

        while True:
            if eval(expression):
                pydirectinput.keyUp('down')
                time.sleep(0.25)
                if eval(expression):
                    break
                else:
                    pydirectinput.keyDown('down')
            elif timeout:
                if time.time() > beginning + timeout:
                    pydirectinput.keyUp('down')
                    break

    def move_right_by(self, distance):
        # 1 sec is approximately equal to 200 pixel when character has 140% speed. That's actually a bad estimate because the screen is also moving the pixels around
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_right_for(time)

    def move_right_for(self, duration):
        self.activate()
        pydirectinput.keyDown('right')
        time.sleep(duration)
        pydirectinput.keyUp('right')

    def move_right_until(self, expression, timeout=None):
        self.activate()
        pydirectinput.keyDown('right')
        beginning = time.time()

        while True:
            if eval(expression):
                pydirectinput.keyUp('right')
                time.sleep(0.25)
                if eval(expression):
                    break
                else:
                    pydirectinput.keyDown('right')
            elif timeout:
                if time.time() > beginning + timeout:
                    pydirectinput.keyUp('right')
                    break

    def move_right_and_up_by(self, distance):
        # FOR PORTALS, NOT CLIMBING UP ROPES
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_right_and_up_for(time)

    def move_right_and_up_for(self, duration):
        # FOR PORTALS, NOT CLIMBING UP ROPES
        now = time.time()
        self.activate()
        pydirectinput.keyDown('right')
        while time.time() - now < duration:
            pyPostMessage('press', [win32con.VK_UP, 1], self.hwnd)
        pydirectinput.keyUp('right')

    def move_right_and_up_until(self, expression, timeout=None):
        # FOR PORTALS, NOT CLIMBING UP ROPES
        self.activate()
        pydirectinput.keyDown('right')
        beginning = time.time()

        while True:
            pyPostMessage('press', [win32con.VK_UP, 1], self.hwnd)
            if eval(expression):
                pydirectinput.keyUp('right')
                time.sleep(0.25)
                if eval(expression):
                    break
                else:
                    pydirectinput.keyDown('right')
            elif timeout:
                if time.time() > beginning + timeout:
                    pydirectinput.keyUp('right')
                    break

    def move_right_and_down_by(self, distance):
        # FOR CLIMBING DOWN ROPES
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_right_and_down_for(time)

    def move_right_and_down_for(self, duration):
        # FOR CLIMBING DOWN ROPES
        now = time.time()
        self.activate()
        pydirectinput.keyDown('right')
        pydirectinput.keyDown('down')
        while time.time() - now < duration:
            pass
        pydirectinput.keyUp('down')
        pydirectinput.keyUp('right')

    def move_right_and_down_until(self, expression, timeout=None):
        # FOR CLIMBING DOWN ROPES
        self.activate()
        pydirectinput.keyDown('right')
        pydirectinput.keyDown('down')
        beginning = time.time()

        while True:
            if eval(expression):
                pydirectinput.keyUp('right')
                pydirectinput.keyUp('down')
                time.sleep(0.25)
                if eval(expression):
                    break
                else:
                    pydirectinput.keyDown('right')
                    pydirectinput.keyDown('down')
            elif timeout:
                if time.time() > beginning + timeout:
                    pydirectinput.keyUp('down')
                    pydirectinput.keyUp('right')
                    break

    def move_left_by(self, distance):
        # 1 sec is approximately equal to 200 pixel when character has 140% speed.
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_left_for(time)

    def move_left_for(self, duration):
        self.activate()
        pydirectinput.keyDown('left')
        time.sleep(duration)
        pydirectinput.keyUp('left')

    def move_left_until(self, expression, timeout=None):
        self.activate()
        pydirectinput.keyDown('left')
        beginning = time.time()

        while True:
            if eval(expression):
                pydirectinput.keyUp('left')
                time.sleep(0.25)
                if eval(expression):
                    break
                else:
                    pydirectinput.keyDown('left')
            elif timeout:
                if time.time() > beginning + timeout:
                    pydirectinput.keyUp('left')
                    break

    def move_left_and_up_by(self, distance):
        # FOR PORTALS, NOT CLIMBING UP ROPES
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_left_and_up_for(time)

    def move_left_and_up_for(self, duration):
        # FOR PORTALS, NOT CLIMBING UP ROPES
        now = time.time()
        self.activate()
        pydirectinput.keyDown('left')
        while time.time() - now < duration:
            pyPostMessage('press', [win32con.VK_UP, 1], self.hwnd)
        pydirectinput.keyUp('left')

    def move_left_and_up_until(self, expression, timeout=None):
        # FOR PORTALS, NOT CLIMBING UP ROPES
        self.activate()
        pydirectinput.keyDown('left')
        beginning = time.time()

        while True:
            pyPostMessage('press', [win32con.VK_UP, 1], self.hwnd)
            if eval(expression):
                pydirectinput.keyUp('left')
                time.sleep(0.25)
                if eval(expression):
                    break
                else:
                    pydirectinput.keyDown('left')
            elif timeout:
                if time.time() > beginning + timeout:
                    pydirectinput.keyUp('left')
                    break

    def move_left_and_down_by(self, distance):
        # FOR CLIMBING DOWN ROPES
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_left_and_down_for(time)

    def move_left_and_down_for(self, duration):
        # FOR CLIMBING DOWN ROPES
        now = time.time()
        self.activate()
        pydirectinput.keyDown('left')
        pydirectinput.keyDown('down')
        while time.time() - now < duration:
            pass
        pydirectinput.keyUp('down')
        pydirectinput.keyUp('left')

    def move_left_and_down_until(self, expression, timeout=None):
        # FOR CLIMBING DOWN ROPES
        self.activate()
        pydirectinput.keyDown('left')
        pydirectinput.keyDown('down')
        beginning = time.time()

        while True:
            if eval(expression):
                pydirectinput.keyUp('left')
                pydirectinput.keyUp('down')
                time.sleep(0.25)
                if eval(expression):
                    break
                else:
                    pydirectinput.keyDown('left')
                    pydirectinput.keyDown('down')
            elif timeout:
                if time.time() > beginning + timeout:
                    pydirectinput.keyUp('down')
                    pydirectinput.keyUp('left')
                    break

    def jump(self):

        key_config = eval(self.config.get(section='KEYBINDS - Common', option='jumpkey'))
        pyPostMessage('press', key_config, self.hwnd)

    def jump_for(self, duration):

        key_config = eval(self.config.get(section='KEYBINDS - Common', option='jumpkey'))
        pyPostMessage('hold', key_config, self.hwnd, duration=duration)

    def jump_right(self):
        self.activate()
        pydirectinput.keyDown('right')
        pydirectinput.press(self.config.get(section='KEYBINDS - Common - pyautogui', option='jumpkey'))
        pydirectinput.keyUp('right')

    def jump_left(self):
        self.activate()
        pydirectinput.keyDown('left')
        pydirectinput.press(self.config.get(section='KEYBINDS - Common - pyautogui', option='jumpkey'))
        pydirectinput.keyUp('left')

    def jump_down(self):
        self.activate()
        pydirectinput.keyDown('down')
        pydirectinput.press(self.config.get(section='KEYBINDS - Common - pyautogui', option='jumpkey'))
        pydirectinput.keyUp('down')

    def jump_right_for(self, duration):
        self.activate()
        now = time.time()
        pydirectinput.keyDown('right')
        while time.time() - now < duration:
            pydirectinput.press(self.config.get(section='KEYBINDS - Common - pyautogui', option='jumpkey'))
        pydirectinput.keyUp('right')

    def jump_left_for(self, duration):
        self.activate()
        now = time.time()
        pydirectinput.keyDown('left')
        while time.time() - now < duration:
            pydirectinput.press(self.config.get(section='KEYBINDS - Common - pyautogui', option='jumpkey'))
        pydirectinput.keyUp('left')

    def jump_down_for(self, duration):
        self.activate()
        now = time.time()
        pydirectinput.keyDown('down')
        while time.time() - now < duration:
            pydirectinput.press(self.config.get(section='KEYBINDS - Common - pyautogui', option='jumpkey'))
        pydirectinput.keyUp('down')

    def jump_right_until(self, expression, timeout=None):
        self.activate()
        pydirectinput.keyDown('right')
        beginning = time.time()

        while True:
            pydirectinput.press(self.config.get(section='KEYBINDS - Common - pyautogui', option='jumpkey'))
            if eval(expression):
                pydirectinput.keyUp('right')
                time.sleep(0.25)
                if eval(expression):
                    break
                else:
                    pydirectinput.keyDown('right')
            elif timeout:
                if time.time() > beginning + timeout:
                    pydirectinput.keyUp('right')
                    break

    def jump_left_until(self, expression, timeout=None):
        self.activate()
        pydirectinput.keyDown('left')
        beginning = time.time()

        while True:
            pydirectinput.press(self.config.get(section='KEYBINDS - Common - pyautogui', option='jumpkey'))
            if eval(expression):
                pydirectinput.keyUp('left')
                time.sleep(0.25)
                if eval(expression):
                    break
                else:
                    pydirectinput.keyDown('left')
            elif timeout:
                if time.time() > beginning + timeout:
                    pydirectinput.keyUp('left')
                    break

    def jump_down_until(self, expression, timeout=None):
        self.activate()
        pydirectinput.keyDown('down')
        beginning = time.time()

        while True:
            pydirectinput.press('altleft')
            if eval(expression):
                pydirectinput.keyUp('down')
                time.sleep(0.25)
                if eval(expression):
                    break
                else:
                    pydirectinput.keyDown('down')
            elif timeout:
                if time.time() > beginning + timeout:
                    pydirectinput.keyUp('down')
                    break
