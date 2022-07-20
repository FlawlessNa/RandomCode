import os
import time
import win32gui
import win32con
import pyautogui
import random
from PostMessage import pyPostMessage
from ImageDetection import take_screenshot, find_image
import cv2


class BaseClient:
    titlebar_pixels = 30

    # Pass in the IGN of the client this instance should control
    def __init__(self, config, ign):
        self.config = config
        self.ign = ign
        if self.get_window_from_ign(ign) is None:
            username, password, pic = eval(self.config.get(section='Login Credentials', option='credentials'))[self.ign]
            self.open(char_type=self.get_char_type())
            self.login(username, password, pic)
            self.dimensions = {
                'width': self.client.width,
                'height': self.client.height - self.titlebar_pixels,
                'crop_x': 0,
                'crop_y': self.titlebar_pixels
            }
            # When login through python, default channel will be 8 automatically
            self.set_current_channel(8)

        else:
            self.client = self.get_window_from_ign(ign)
            self.hwnd = self.client._hWnd
            self.dimensions = {
                'width': self.client.width,
                'height': self.client.height - self.titlebar_pixels,
                'crop_x': 0,
                'crop_y': self.titlebar_pixels
            }
            self.set_current_channel()

        # self.reposition_client(eval(self.config.get(section='Clients Positioning', option='position_dict'))[self.ign])

    def open(self, char_type):
        # Apparently, opening the 800x600 doesnt work, but we can instead open the shortcut on the Desktop and it works..
        # Also Interesting Note: using os.system would also cause the client to run, and the client is automatically killed once the execution of the program ends!

        if eval(self.config.get(section='Kill Clients After Execution', option='value')):
            os.system(eval(self.config.get(section='Client Path', option='path'))[self.config.get(section='RESOLUTIONS', option=char_type)])
        else:
            os.startfile(eval(self.config.get(section='Client Path', option='path'))[self.config.get(section='RESOLUTIONS', option=char_type)])

        # DO NOT change focus after the client has been opened, otherwise the wrong handles will be retrieved.
        time.sleep(10)
        self.hwnd = win32gui.GetForegroundWindow()
        self.client = pyautogui.getActiveWindow()

    def get_char_type(self):
        return eval(self.config.get(section='IGN', option='ign_dict'))[self.ign]

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
        pyautogui.doubleClick(x, y + 5)
        time.sleep(1)
        nbr_move_towards_right = eval(self.config.get(section='Login Character Position', option='position_dict'))[self.ign] - 1

        for i in range(5):
            # This is to ensure that we always start character selection from the far left
            pyautogui.press('left')
            time.sleep(0.05)

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

    def get_window_from_ign(self, ign):
        ign_dict = eval(self.config.get(section='IGN', option='ign_dict'))
        assert ign in ign_dict.keys(), "The IGN provided is not in the configured list"
        char_type = self.get_char_type()

        all_windows = pyautogui.getWindowsWithTitle('MapleRoyals')
        try:
            ign_image = eval(self.config.get(section='IGN Images', option=char_type))[ign]
        except NameError:
            ign_image = self.config.get(section='IGN Images', option=char_type)

        for client in all_windows:

            haystack = take_screenshot(client, dim={
                'width': client.width,
                'height': client.height - self.titlebar_pixels,
                'crop_x': 0,
                'crop_y': self.titlebar_pixels
            })
            needle = cv2.imread(ign_image, cv2.IMREAD_COLOR)
            result = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val >= 0.99:
                return client

        # if client isn't found
        return None

    def take_screenshot(self, dim=None):
        if dim is None:
            return take_screenshot(self.client, dim=self.dimensions)
        else:
            return take_screenshot(self.client, dim=dim)

    def get_current_channel(self):

        if self.current_channel is None:
            pass
        else:
            return self.current_channel

    def set_current_channel(self, channel=None):

        if channel is None:
            ImageDetectionThreshold = 0.99
            loadColorImage = cv2.IMREAD_COLOR
            gameMenuTitleImage = cv2.imread(self.config.get(section='Login Images', option='game_menu'), loadColorImage)

            while not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Login Images', option='game_menu'), cv2.IMREAD_COLOR), threshold=0.99)):
                pyPostMessage('press', [win32con.VK_ESCAPE, 0], self.hwnd)
                time.sleep(0.2)
            pyPostMessage('press', [win32con.VK_RETURN, 0], self.hwnd)

            haystack = self.take_screenshot()
            listOfChannels = eval(self.config.get(section='Login Images', option='channels'))

            for channel in listOfChannels:
                if find_image(haystack, channel, cv2.IMREAD_COLOR, threshold=0.99):
                    print(channel)
        else:
            self.current_channel = channel
