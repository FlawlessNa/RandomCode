from ComplexClient import ComplexClient
import pydirectinput
import random
import time
import cv2
from PostMessage import pyPostMessage
from ImageDetection import find_image, midpoint
import math
import win32gui


class MageManager(ComplexClient):
    def __init__(self, config, ign, position):
        super().__init__(config, ign)
        self.left_positioning_target = None
        self.right_positioning_target = None

        self.desired_left_target_dist = None
        self.left_target_threshold = None

        self.desired_right_target_dist = None
        self.right_target_threshold = None

        self.position = position
        self.logo = eval(self.config.get(section='IGN Images', option='mage_logo'))[ign]

        self.set_targets()

    def set_targets(self):

        if self.position == 'bot':
            self.left_positioning_target = cv2.imread(self.config.get(section='Map Images', option='above_car'), cv2.IMREAD_COLOR)
            self.right_positioning_target = cv2.imread(self.config.get(section='Map Images', option='right_ladder'), cv2.IMREAD_COLOR)

            self.desired_left_target_dist = 100
            self.left_target_threshold = 75

            self.desired_right_target_dist = -50
            self.right_target_threshold = 150

        elif self.position == 'top':
            self.left_positioning_target = cv2.imread(self.config.get(section='Map Images', option='target_sequence_2'), cv2.IMREAD_COLOR)
            self.right_positioning_target = cv2.imread(self.config.get(section='Map Images', option='top_floor_right_target'), cv2.IMREAD_COLOR)

            self.desired_left_target_dist = 50
            self.left_target_threshold = 200

            self.desired_right_target_dist = -50
            self.right_target_threshold = 150

    def cast_ult(self):

        key_config = eval(self.config.get(section='KEYBINDS - Mage', option='ultkey'))
        pyPostMessage('press', key_config, self.hwnd)
        time.sleep(0.2)
        pyPostMessage('press', key_config, self.hwnd)

    def cast_hs(self):

        key_config = eval(self.config.get(section='KEYBINDS - Mage', option='hskey'))
        pyPostMessage('press', key_config, self.hwnd)
        time.sleep(0.2)
        pyPostMessage('press', key_config, self.hwnd)

    def teleport_left(self):

        self.activate()
        pydirectinput.keyDown('left')
        pydirectinput.press(self.config.get(section='KEYBINDS - Mage - pyautogui', option='teleportkey'))
        pydirectinput.keyUp('left')

    def teleport_right(self):
        self.activate()
        pydirectinput.keyDown('right')
        pydirectinput.press(self.config.get(section='KEYBINDS - Mage - pyautogui', option='teleportkey'))
        pydirectinput.keyUp('right')

    def cast_mg(self):

        key_config = eval(self.config.get(section='KEYBINDS - Mage', option='mgkey'))
        while True:
            pyPostMessage('press', key_config, self.hwnd)
            time.sleep(0.2)
            if len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Misc Images', option='fresh_mg'), cv2.IMREAD_COLOR), threshold=0.95)):
                break
        return random.randint(200, 250)

    def cast_infinity(self):

        key_config = eval(self.config.get(section='KEYBINDS - Mage', option='infinitykey'))
        pyPostMessage('press', key_config, self.hwnd)
        time.sleep(0.2)
        pyPostMessage('press', key_config, self.hwnd)
        return random.randint(600, 625)

    def cast_door(self):

        key_config = eval(self.config.get(section='KEYBINDS - Mage', option='doorkey'))
        pyPostMessage('press', key_config, self.hwnd)
        time.sleep(0.2)
        pyPostMessage('press', key_config, self.hwnd)
        time.sleep(0.2)
        pyPostMessage('press', key_config, self.hwnd)

    def reposition_needed(self):

        # haystack = self.take_screenshot()
        # curr_pos = self.find_self()
        # rects_left = find_image(haystack, self.left_positioning_target)
        # rects_right = find_image(haystack, self.right_positioning_target)
        #
        # if len(rects_left) and len(curr_pos):
        #     self_x, self_y = midpoint(self.hwnd, curr_pos)
        #     target_x, target_y = midpoint(self.hwnd, rects_left)
        #     if self_x - target_x < self.distance_with_left_target:
        #         return True
        #
        # elif len(rects_right) and len(curr_pos):
        #     self_x, self_y = midpoint(self.hwnd, curr_pos)
        #     target_x, target_y = midpoint(self.hwnd, rects_right)
        #     if target_x - self_x < self.distance_with_right_target:
        #         return True
        #
        # elif not len(curr_pos):
        #     return True

        haystack = self.take_screenshot()
        rects_left = find_image(haystack, self.left_positioning_target)
        rects_right = find_image(haystack, self.right_positioning_target)

        if len(rects_left):
            target_x, target_y = midpoint(self.hwnd, rects_left)
            if target_x - self.client.left > self.left_target_threshold:
                return True

        elif len(rects_right):
            target_x, target_y = midpoint(self.hwnd, rects_right)
            if self.client.right - target_x > self.right_target_threshold:
                return True

    def reposition(self):
        # char_pos = self.find_self()
        # if len(char_pos):
        #     char_x, char_y = midpoint(self.hwnd, char_pos)
        #
        #     haystack = self.take_screenshot()
        #     rects_left = find_image(haystack, self.left_positioning_target, threshold=0.8)
        #     rects_right = find_image(haystack, self.right_positioning_target, threshold=0.8)
        #
        #     if len(rects_left):
        #         target_x, target_y = midpoint(self.hwnd, rects_left)
        #         print('{} distance with left target: {}'.format(self.ign, abs(char_x - target_x)))
        #         if self.position == 'top':
        #             if char_x > target_x:
        #                 self.jump_right_by(max(0, self.distance_with_left_target - abs(char_x - target_x)))
        #             else:
        #                 self.jump_right_by(self.distance_with_left_target + abs(char_x - target_x))
        #         else:
        #             if char_x > target_x:
        #                 self.move_right_by(max(0, self.distance_with_left_target - abs(char_x - target_x)))
        #             else:
        #                 self.move_right_by(self.distance_with_left_target + abs(char_x - target_x))
        #
        #     elif len(rects_right):
        #         target_x, target_y = midpoint(self.hwnd, rects_right)
        #         print('{} distance with right target: {}'.format(self.ign, abs(char_x - target_x)))
        #
        #         # safeguard to make sure character is still on the top-most platform
        #         if char_x - target_x > - 100 and self.position == 'top':
        #             self.teleport_left()
        #             # Reduce the distance by approx 250 to account for the teleport
        #             self.move_left_by(max(0, self.distance_with_right_target - 250 - abs(char_x - target_x)))
        #
        #         elif char_x < target_x:
        #             self.move_left_by(max(0, self.distance_with_right_target - abs(char_x - target_x)))
        #         else:
        #             self.move_left_by(self.distance_with_right_target + abs(char_x - target_x))
        # else:
        #     self.teleport_right()

        haystack = self.take_screenshot()
        rects_left = find_image(haystack, self.left_positioning_target, threshold=0.8)
        rects_right = find_image(haystack, self.right_positioning_target, threshold=0.8)

        if len(rects_left):
            target_x, target_y = midpoint(self.hwnd, rects_left)
            curr_target_dist_with_client = target_x - self.client.left
            print('{} -- Left target distance with client border: {}'.format(self.ign, curr_target_dist_with_client))

            if curr_target_dist_with_client > self.left_target_threshold:
                if self.position == 'top':
                    self.teleport_right()
                    self.jump_right_by(max(0, curr_target_dist_with_client - self.desired_left_target_dist))
                elif self.position == 'bot':
                    self.teleport_right()
                    self.move_right_by(max(0, curr_target_dist_with_client - self.desired_left_target_dist))

        elif len(rects_right):
            target_x, target_y = midpoint(self.hwnd, rects_right)
            curr_target_dist_with_client = self.client.right - target_x
            print('{} -- Right target distance with client border: {}'.format(self.ign, curr_target_dist_with_client))

            if curr_target_dist_with_client > self.right_target_threshold:
                self.move_left_by(curr_target_dist_with_client - self.desired_right_target_dist)

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

    def move_to_top(self):
        pass

    def find_self(self):

        # return the point closest to the middle of the client
        image = self.logo
        rects = find_image(haystack=self.take_screenshot(), needle=cv2.imread(image, cv2.IMREAD_COLOR))
        if len(rects) > 1:
            dist = []
            for rect in rects:
                x, y = midpoint(self.hwnd, rect)
                client_x, client_y = win32gui.ClientToScreen(self.hwnd, (int(self.client.width/2), int(self.client.height/2)))
                dist.append(math.sqrt((x - client_x) ** 2 + (y - client_y) ** 2))
            return rects[dist.index(min(dist))]
        return rects

    def farm(self):

        haystack = self.take_screenshot()
        images = []
        for item in self.config.items(section='MOB Images'):
            imgs = eval(item[1])
            images.extend(imgs)
        if self.detect_mobs_multi_image(haystack, images) >= 4:
            self.cast_ult()
            return True
