from ComplexClient import ComplexClient
import pyautogui
import pydirectinput
import time
import win32api
import win32gui
import win32con
from PostMessage import pyPostMessage
import cv2
from ImageDetection import find_image
import random


class LooterManager(ComplexClient):

    def __init__(self, config, ign):
        super().__init__(config, ign)

    def use_stance(self):

        key_config = eval(self.config.get(section='KEYBINDS - Looter', option='stancekey'))
        pyPostMessage('press', key_config, self.hwnd)
        time.sleep(0.8)

    def chat_feed_is_displayed(self):
        if pyautogui.locateOnScreen(image='KeyImages/Feed_is_Displayed.png', region=self.client.box) is not None:
            return True
        else:
            return False

    def feed_mount(self):

        key_config = eval(self.config.get(section='KEYBINDS - Looter', option='mountfoodkey'))
        self.ensure_mount_is_used()

        pyPostMessage('press', key_config, self.hwnd)

    def toggle_mount(self):

        key_config = eval(self.config.get(section='KEYBINDS - Looter', option='mountkey'))
        pyPostMessage('press', key_config, self.hwnd)
        time.sleep(0.3)

    def ensure_mount_is_used(self):

        if pyautogui.locateOnScreen(image=self.config.get(section='Mount Image', option='mount_icon'), region=self.client.box, confidence=0.95) is None:
            self.toggle_mount()

    def find_self(self):
        image = self.config.get(section='Character Images', option='looter_guildlogo')
        return find_image(haystack=self.take_screenshot(), needle=cv2.imread(image, cv2.IMREAD_COLOR))

    def check_inventory_slots(self):
        self.ensure_inventory_is_open()
        self.ensure_inventory_is_expanded()

        # Get to Equip Inventory
        while True:
            if not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Inventory Images', option='equip_inventory'), cv2.IMREAD_COLOR), threshold=0.99)):
                pyPostMessage('press', [win32con.VK_TAB, 0], self.hwnd)
            else:
                break
        # sorting/merging just to minimize the number of cells that may be mis-read as not empty
        self.inventory_merge_and_sort()

        return len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Inventory Images', option='empty_inventory_cell'), cv2.IMREAD_COLOR), threshold=0.99))

    def check_for_godlies(self):
        pass

    def move_to_and_enter_door(self):

        target = self.config.get(section='Map Images', option='door')
        self.ensure_mount_is_used()
        self.toggle_mount()
        while True:
            self.move_to_target(target, [-30, 0])
            self.jump()
            time.sleep(0.75)
            self.move_up()
            if not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='above_car'), cv2.IMREAD_COLOR))):
                break
        self.toggle_mount()
            # curr_pos = self.find_self()
            # haystack = self.take_screenshot()
            #
            # target = find_image(haystack, needle)
            # if len(curr_pos) and len(target):
            #     x1, y1, w1, h1 = list(*curr_pos)
            #     x2, y2, w2, h2 = list(*target)

        # # TODO: Try finishing the "move_left_and_up" and "move_right_and_up" methods within ClientManager and use these instead?
        # # This method should only be used after changing channel!
        # while pyautogui.locateOnScreen(self.config.get(section='Map Images', option='ulu_minimap'), region=self.client.box) is None:
        #     self.toggle_minimap()
        #
        # loop = True
        # self.move_right_by(666 - 322)
        # while loop:
        #     self.move_to_target(target=self.config.get(section='Map Images', option='door'), acceptable_dist_range=[13, 37])
        #     self.jump()
        #     time.sleep(0.6)
        #     self.move_up()
        #     time.sleep(1)
        #     loop = self.check_portal_success(self.config.get(section='Map Images', option='CBD_minimap'))

    def move_from_door_to_fm(self):

        cond1 = """not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='CBD_portal1'), cv2.IMREAD_COLOR), threshold=0.9))"""
        cond2 = """not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='CBD_FM'), cv2.IMREAD_COLOR), threshold=0.9))"""
        self.move_left_for(2)
        self.move_right_and_up_until(cond1)
        time.sleep(1.5)
        self.move_right_and_up_until(cond2)
        self.move_right_for(0.5)


    def move_from_fm_to_door(self):
        cond1 = """not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='FM_NPC'), cv2.IMREAD_COLOR), threshold=0.8))"""
        cond2 = """not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='CBD_FM'), cv2.IMREAD_COLOR), threshold=0.5))"""
        cond3 = """not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='CBD_portal1'), cv2.IMREAD_COLOR), threshold=0.8))"""

        self.move_left_and_up_until(cond1)
        # Minimize chat to better detect the map anchor at this spot
        if self.chat_feed_is_displayed():
            self.toggle_chatfeed()

        self.move_left_and_up_until(cond2)
        self.ensure_mount_is_used()
        self.jump_right()
        self.move_right_and_up_until(cond3)

    def click_fm_storage(self):
        # Values are hard-coded since location is never-changing. Prevents issues as there may be characters/animations hindering the npc
        self.click_at(60, 600)

    def click_fm_seller(self):
        self.click_at(525, 325)

    def order_items_to_keep_on_top(self):
        pass

    def sell_items(self):
        self.click_fm_seller()
        x, y = win32gui.ClientToScreen(self.hwnd, (int(100), int(100)))
        self.move_cursor_to(x, y)
        rect = find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Inventory Images', option='equip_tab_seller'), cv2.IMREAD_COLOR), threshold=0.9)
        x, y, w, h = list(*rect)
        target_x = x + 30
        target_y = y + h/2 + 75
        self.click_at(target_x, target_y)

        haystack = self.take_screenshot()
        target = find_image(haystack, cv2.imread(self.config.get(section='Inventory Images', option='sell_item'), cv2.IMREAD_COLOR), threshold=0.9)
        x, y, w, h = list(*target)
        target_x, target_y = win32gui.ClientToScreen(self.hwnd, (int(x + w/2), int(y + h/2)))
        item_sold = 0
        while item_sold < 96:
            self.click_at(target_x, target_y)
            pyPostMessage('press', [0x59, 0], self.hwnd)
            time.sleep(random.uniform(0.01, 0.1))
            item_sold += 1

    def map_sequence_1(self):

        cond = """len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='left_ladder'), cv2.IMREAD_COLOR)))"""
        self.jump_right_for(4)
        self.move_right_until(expression=cond)

        pydirectinput.keyDown('up')
        time.sleep(0.5)
        pydirectinput.keyUp('up')

    def map_sequence_2(self):

        cond = """len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='target_sequence_2'), cv2.IMREAD_COLOR)))"""
        self.jump_left_for(2)
        self.move_left_until(expression=cond)
        time.sleep(0.2)
        self.jump()
        time.sleep(1.5)

    def map_sequence_3(self):
        cond = """len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Character Images', option='looter_backhead'), cv2.IMREAD_COLOR)))"""
        self.move_right_and_down_until(expression=cond)
        self.move_down_for(1)
        self.jump_left()
        time.sleep(1)

    def map_sequence_4(self):

        cond = """len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='target_sequence_4'), cv2.IMREAD_COLOR)))"""
        self.jump_down()
        time.sleep(0.6)
        self.jump_down()
        time.sleep(1)
        self.move_left_until(expression=cond)

