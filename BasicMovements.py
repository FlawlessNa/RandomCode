import pydirectinput
import win32con
import time
from PostMessage import pyPostMessage
from BaseClient import BaseClient


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

    def move_up(self):

        key_config = [win32con.VK_UP, 1]
        pyPostMessage('press', key_config, self.hwnd)

    def move_up_by(self, distance):
        # 1 sec is approximately equal to 200 pixel when character has 170% speed.
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_up_for(time)

    def move_up_for(self, duration):
        self.client.activate()
        pydirectinput.keyDown('up')
        time.sleep(duration)
        pydirectinput.keyUp('up')

    def move_up_until(self, expression):
        self.client.activate()
        pydirectinput.keyDown('up')

        loop = True
        while loop:
            if eval(expression):
                pydirectinput.keyUp('up')
                loop = False

    def move_down_by(self, distance):
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_left_for(time)

    def move_down_for(self, duration):
        self.client.activate()
        pydirectinput.keyDown('down')
        time.sleep(duration)
        pydirectinput.keyUp('down')

    def move_down_until(self, expression):
        self.client.activate()
        pydirectinput.keyDown('down')

        loop = True
        while loop:
            if eval(expression):
                pydirectinput.keyUp('down')
                loop = False

    def move_right_by(self, distance):
        # 1 sec is approximately equal to 200 pixel when character has 140% speed. That's actually a bad estimate because the screen is also moving the pixels around
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_right_for(time)

    def move_right_for(self, duration):
        self.client.activate()
        pydirectinput.keyDown('right')
        time.sleep(duration)
        pydirectinput.keyUp('right')

    def move_right_until(self, expression):
        self.client.activate()
        pydirectinput.keyDown('right')

        loop = True
        while loop:
            if eval(expression):
                pydirectinput.keyUp('right')
                loop = False

    def move_right_and_up_by(self, distance):
        # FOR PORTALS, NOT CLIMBING UP ROPES
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_right_and_up_for(time)

    def move_right_and_up_for(self, duration):
        # FOR PORTALS, NOT CLIMBING UP ROPES
        now = time.time()
        self.client.activate()
        pydirectinput.keyDown('right')
        while time.time() - now < duration:
            pyPostMessage('press', [win32con.VK_UP, 1], self.hwnd)
        pydirectinput.keyUp('right')

    def move_right_and_up_until(self, expression):
        # FOR PORTALS, NOT CLIMBING UP ROPES
        self.client.activate()
        pydirectinput.keyDown('right')

        loop = True
        while loop:
            pyPostMessage('press', [win32con.VK_UP, 1], self.hwnd)
            if eval(expression):
                pydirectinput.keyUp('right')
                loop = False

    def move_right_and_down_by(self, distance):
        # FOR CLIMBING DOWN ROPES
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_right_and_down_for(time)

    def move_right_and_down_for(self, duration):
        # FOR CLIMBING DOWN ROPES
        now = time.time()
        self.client.activate()
        pydirectinput.keyDown('right')
        pydirectinput.keyDown('down')
        while time.time() - now < duration:
            pass
        pydirectinput.keyUp('down')
        pydirectinput.keyUp('right')

    def move_right_and_down_until(self, expression):
        # FOR CLIMBING DOWN ROPES
        self.client.activate()
        pydirectinput.keyDown('right')
        pydirectinput.keyDown('down')

        loop = True
        while loop:
            if eval(expression):
                pydirectinput.keyUp('right')
                pydirectinput.keyUp('down')
                loop = False

    def move_left_by(self, distance):
        # 1 sec is approximately equal to 200 pixel when character has 140% speed.
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_left_for(time)

    def move_left_for(self, duration):
        self.client.activate()
        pydirectinput.keyDown('left')
        time.sleep(duration)
        pydirectinput.keyUp('left')

    def move_left_until(self, expression):
        self.client.activate()
        pydirectinput.keyDown('left')

        loop = True
        while loop:
            if eval(expression):
                pydirectinput.keyUp('left')
                loop = False

    def move_left_and_up_by(self, distance):
        # FOR PORTALS, NOT CLIMBING UP ROPES
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_left_and_up_for(time)

    def move_left_and_up_for(self, duration):
        # FOR PORTALS, NOT CLIMBING UP ROPES
        now = time.time()
        self.client.activate()
        pydirectinput.keyDown('left')
        while time.time() - now < duration:
            pyPostMessage('press', [win32con.VK_UP, 1], self.hwnd)
        pydirectinput.keyUp('left')

    def move_left_and_up_until(self, expression):
        # FOR PORTALS, NOT CLIMBING UP ROPES
        self.client.activate()
        pydirectinput.keyDown('left')

        loop = True
        while loop:
            pyPostMessage('press', [win32con.VK_UP, 1], self.hwnd)
            if eval(expression):
                pydirectinput.keyUp('left')
                loop = False

    def move_left_and_down_by(self, distance):
        # FOR CLIMBING DOWN ROPES
        time = distance / ((200 / 1.4) * self.get_char_speed())
        self.move_left_and_down_for(time)

    def move_left_and_down_for(self, duration):
        # FOR CLIMBING DOWN ROPES
        now = time.time()
        self.client.activate()
        pydirectinput.keyDown('left')
        pydirectinput.keyDown('down')
        while time.time() - now < duration:
            pass
        pydirectinput.keyUp('down')
        pydirectinput.keyUp('left')

    def move_left_and_down_until(self, expression):
        # FOR CLIMBING DOWN ROPES
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

        key_config = eval(self.config.get(section='KEYBINDS - Common', option='jumpkey'))
        pyPostMessage('press', key_config, self.hwnd)

    def jump_for(self, duration):

        key_config = eval(self.config.get(section='KEYBINDS - Common', option='jumpkey'))
        pyPostMessage('hold', key_config, self.hwnd, duration=duration)

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
