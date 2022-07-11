from ComplexClient import ComplexClient
import pydirectinput
import pyautogui
import win32con
import win32api
import time
import cv2
from PostMessage import pyPostMessage
from ImageDetection import take_screenshot, find_image


class MageManager(ComplexClient):
    def __init__(self, config, ign):
        super().__init__(config, ign)

    def cast_ult(self):

        key_config = eval(self.config.get(section='KEYBINDS - Mage', option='ultkey'))
        pyPostMessage('press', key_config, self.hwnd)
        time.sleep(0.1)
        pyPostMessage('press', key_config, self.hwnd)

    def teleport_left(self):

        self.client.activate()
        pydirectinput.keyDown('left')
        pydirectinput.press(self.config.get(section='KEYBINDS - Mage - pyautogui', option='teleportkey'))
        pydirectinput.keyUp('left')

    def teleport_right(self):
        self.client.activate()
        pydirectinput.keyDown('right')
        pydirectinput.press(self.config.get(section='KEYBINDS - Mage - pyautogui', option='teleportkey'))
        pydirectinput.keyUp('right')

    def cast_mg(self):

        key_config = eval(self.config.get(section='KEYBINDS - Mage', option='mgkey'))
        pyPostMessage('press', key_config, self.hwnd)
        time.sleep(0.1)
        pyPostMessage('press', key_config, self.hwnd)

    def cast_infinity(self):

        key_config = eval(self.config.get(section='KEYBINDS - Mage', option='infinitykey'))
        pyPostMessage('press', key_config, self.hwnd)
        time.sleep(0.1)
        pyPostMessage('press', key_config, self.hwnd)

    def cast_door(self):

        key_config = eval(self.config.get(section='KEYBINDS - Mage', option='doorkey'))
        pyPostMessage('press', key_config, self.hwnd)
        time.sleep(0.1)
        pyPostMessage('press', key_config, self.hwnd)

    def reposition(self):
        char_pos = self.find_self()
        if len(char_pos):
            needle_left = cv2.imread(self.config.get(section='Map Images', option='target_sequence_2'), cv2.IMREAD_COLOR)
            needle_right = cv2.imread(self.config.get(section='Map Images', option='left_ladder'), cv2.IMREAD_COLOR)
            haystack = self.take_screenshot()
            rects_left = find_image(haystack, needle_left)
            rects_right = find_image(haystack, needle_right)

            if len(rects_left):
                print('{} distance with left target: {}'.format(self.ign, char_pos[0][0] - rects_left[0][0]))
                self.move_right_by(550 - (char_pos[0][0] - rects_left[0][0]))

            elif len(rects_right):
                print('{} distance with right target: {}'.format(self.ign, char_pos[0][0] - rects_right[0][0]))
                self.move_left_by(900 - abs(char_pos[0][0] - rects_right[0][0]))

    def move_to_car(self):
        loop = True
        all_images = eval(self.config.get(section='MOB Images', option='veetron'))
        all_images.extend(eval(self.config.get(section='MOB Images', option='berserkie')))
        while loop:
            self.cast_ult()
            time.sleep(2)
            if self.detect_mobs_multi_image(all_images) == 0:
                self.move_right_for(0.65)
                self.teleport_right()
                time.sleep(0.1)
                self.jump()
            loop = False

    def detect_mobs(self, haystack, mob_image):
        return len(find_image(haystack, cv2.imread(mob_image, cv2.IMREAD_COLOR)))

    def detect_mobs_multi_image(self, haystack, mob_images):
        nbr_mobs = 0
        for image in mob_images:
            nbr_mobs += self.detect_mobs(haystack, image)
        return nbr_mobs

    def find_self(self):
        image = self.config.get(section='Character Images', option='mage_medal')
        return find_image(haystack=self.take_screenshot(), needle=cv2.imread(image, cv2.IMREAD_COLOR))

    def move_to_top(self):
        pass

    def farm_mode(self, pos):

        if pos == 'top':
            self.reposition()

        haystack = self.take_screenshot()
        images = []
        for item in self.config.items(section='MOB Images'):
            imgs = eval(item[1])
            images.extend(imgs)
        if self.detect_mobs_multi_image(haystack, images) >= 4:
            self.cast_ult()
            return True

