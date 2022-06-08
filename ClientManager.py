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

    def move_right_for(self, duration):
        self.client.activate()
        pydirectinput.keyDown('right')
        time.sleep(duration)
        pydirectinput.keyUp('right')

    def move_right_to(self, destination):
        pass

    def move_left_by(self, distance):
        pass

    def move_left_for(self, duration):
        self.client.activate()
        pydirectinput.keyDown('left')
        time.sleep(duration)
        pydirectinput.keyUp('left')

    def move_left_to(self, destination):
        pass

    def move_up_by(self, distance):
        pass

    def move_up_for(self, duration):
        self.client.activate()
        pydirectinput.keyDown('up')
        time.sleep(duration)
        pydirectinput.keyUp('up')

    def move_up_to(self, destination):
        pass

    def move_down_by(self, distance):
        pass

    def move_down_for(self, duration):
        self.client.activate()
        pydirectinput.keyDown('down')
        time.sleep(duration)
        pydirectinput.keyUp('down')

    def move_down_to(self, destination):
        pass

    def jump(self):
        self.client.activate()
        pydirectinput.press('altright')

    def jump_right(self):
        self.client.activate()
        pydirectinput.keyDown('right')
        pydirectinput.press('altright')
        pydirectinput.keyUp('right')

    def jump_left(self):
        self.client.activate()
        pydirectinput.keyDown('left')
        pydirectinput.press('altright')
        pydirectinput.keyUp('left')

    def toggle_inventory(self):
        self.client.activate()
        pydirectinput.press('i')

    def click(self):
        self.client.activate()
        pydirectinput.click()

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
