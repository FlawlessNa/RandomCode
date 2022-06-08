import os
import win32gui
import win32con
import time
import pyautogui
import pydirectinput

# USE pyautogui -- it has everything we need!
config = {'IGN_LIST': ['Guarding', 'ShyPooper', 'LegalizeIt', 'Goldmine1', 'Goldmine2', 'Goldmine3', 'Buccanoid'],
          'Guarding':'KeyImages/Guarding_IGN.png'}

class ClientManager():
    # Pass in the IGN of the client this instance should control
    def __init__(self, ign):
        self.client = self.get_window_from_ign(ign)

    def open(self, resolution):
        pass

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
        now = time.time()
        pydirectinput.keyDown('right')
        while time.time() - now < duration:
            pass
        pydirectinput.keyUp('right')

    def move_left_for(self, duration):
        self.client.activate()
        now = time.time()
        pydirectinput.keyDown('left')
        while time.time() - now < duration:
            pass
        pydirectinput.keyUp('left')

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
        self.client.activate()
        pydirectinput.press('altleft')

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
