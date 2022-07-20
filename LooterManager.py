from ComplexClient import ComplexClient
import pyautogui
import time
import win32gui
import win32con
from PostMessage import pyPostMessage
import cv2
from ImageDetection import find_image, midpoint
import random


class LooterManager(ComplexClient):

    def __init__(self, config, ign):
        super().__init__(config, ign)

    def use_stance(self):

        key_config = eval(self.config.get(section='KEYBINDS - Looter', option='stancekey'))
        pyPostMessage('press', key_config, self.hwnd)

    def feed_mount(self):

        key_config = eval(self.config.get(section='KEYBINDS - Looter', option='mountfoodkey'))
        self.ensure_mount_is_used()

        pyPostMessage('press', key_config, self.hwnd)
        return random.randint(500, 650)

    def toggle_mount(self):

        key_config = eval(self.config.get(section='KEYBINDS - Looter', option='mountkey'))
        pyPostMessage('press', key_config, self.hwnd)

    def check_is_mounted(self):
        if len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Mount Image', option='mount_icon'), cv2.IMREAD_COLOR))):
            return True
        return False

    def ensure_mount_is_used(self):

        if not self.check_is_mounted():
            self.toggle_mount()

    def find_self(self):
        image = self.config.get(section='Character Images', option='looter_guildlogo')
        return find_image(haystack=self.take_screenshot(), needle=cv2.imread(image, cv2.IMREAD_COLOR))

    def check_inventory_slots(self):
        self.ensure_inventory_is_open()
        self.ensure_inventory_is_expanded()

        # Get to Equip Inventory
        while True:
            if not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Inventory Images', option='equip_inventory'), cv2.IMREAD_COLOR), threshold=0.8)):
                pyPostMessage('press', [win32con.VK_TAB, 0], self.hwnd)
            else:
                break
        # sorting/merging just to minimize the number of cells that may be mis-read as not empty
        self.inventory_merge_and_sort()

        inv_slots = len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Inventory Images', option='empty_inventory_cell'), cv2.IMREAD_COLOR), threshold=0.9))
        self.toggle_inventory()
        print('nbr equip slots left: {}'.format(inv_slots))
        return inv_slots

    def check_for_godlies(self):
        pass

    def move_to_and_enter_door(self):

        cond1 = """not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='ulu1'), cv2.IMREAD_COLOR), threshold=0.9))"""
        cond2 = """len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='CBD'), cv2.IMREAD_COLOR), threshold=0.8))"""
        cond3 = """len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='ulu1'), cv2.IMREAD_COLOR), threshold=0.9))"""
        target = self.config.get(section='Map Images', option='door')

        self.map_sequence_1()
        self.ensure_mount_is_used()
        time.sleep(1)
        self.toggle_mount()
        self.move_cursor_to(random.randint(100, 200), random.randint(100, 200))
        self.toggle_buddy_list()
        time.sleep(0.5)

        self.move_right_and_up_until(cond1, timeout=8)
        time.sleep(1.25)

        while True:

            if eval(cond2):
                self.toggle_buddy_list()
                break
            # TODO: Improve this elif clause since it only attemps to detect door once and the door may be hindered by a mage ult
            elif eval(cond3):
                self.toggle_buddy_list()
                if len(find_image(self.take_screenshot(), cv2.imread(target, cv2.IMREAD_COLOR))):
                    self.move_to_target(target, [-30, 0], threshold=0.7)
                    self.move_up()

    def move_from_door_to_fm(self):

        cond1 = """not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='CBD_portal1'), cv2.IMREAD_COLOR), threshold=0.8))"""
        cond2 = """not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='CBD_FM'), cv2.IMREAD_COLOR), threshold=0.8))"""
        self.move_left_for(2.5)

        while True:
            self.move_right_and_up_until(cond1)
            time.sleep(1)
            if eval(cond1):
                self.move_right_for(0.5)
                break

        while True:
            self.move_right_and_up_until(cond2)
            time.sleep(1)
            # TODO: replace the confirmation on whether the door was succesfully entered by using self.check_current_location!
            if eval(cond2):
                break

    def move_from_fm_to_door(self):
        cond1 = """not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='FM_NPC'), cv2.IMREAD_COLOR), threshold=0.8))"""
        cond2 = """not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='CBD_FM'), cv2.IMREAD_COLOR), threshold=0.8))"""
        cond3 = """not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='CBD_portal1'), cv2.IMREAD_COLOR), threshold=0.8))"""

        self.move_up()
        time.sleep(1)
        # TODO: replace the confirmation on whether the door was succesfully entered by using self.check_current_location!
        if len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='FM_NPC'), cv2.IMREAD_COLOR), threshold=0.8)):
            self.move_up()
            time.sleep(1)

        # Minimize chat to better detect the map anchor at this spot
        if self.chat_feed_is_displayed():
            self.toggle_chatfeed()

        self.move_left_for(0.5)
        self.move_left_and_up_until(cond2)
        self.ensure_mount_is_used()
        time.sleep(1)
        self.jump_right()
        time.sleep(1)
        self.toggle_mount()
        self.move_right_and_up_until(cond3)
        time.sleep(1)
        # TODO: replace the confirmation on whether the door was succesfully entered by using self.check_current_location!
        self.toggle_mount()

    def after_channel_change(self):

        time.sleep(1)
        self.toggle_mount()
        time.sleep(1.25)
        self.use_stance()
        time.sleep(1.25)
        self.ensure_mount_is_used()
        if self.check_inventory_slots() < 15:
            return True
        return False

    def click_fm_storage(self):
        # Values are hard-coded since location is never-changing. Prevents issues as there may be characters/animations hindering the npc
        x, y = win32gui.ClientToScreen(self.hwnd, (60, 550))
        self.click_at(x, y)

    def click_fm_seller(self):
        x, y = win32gui.ClientToScreen(self.hwnd, (500, 275))
        self.click_at(x, y)

    def store_items(self, nbr_items):
        self.ensure_inventory_is_open()
        time.sleep(0.25)
        self.toggle_inventory()
        time.sleep(0.25)
        self.click_fm_storage()
        time.sleep(0.25)
        x, y = win32gui.ClientToScreen(self.hwnd, (600, 372))
        for i in range(nbr_items):
            self.double_click_at(x, y)
            pyPostMessage('press', [win32con.VK_RETURN, 0], self.hwnd)
            time.sleep(0.25)

        pyPostMessage('press', [win32con.VK_ESCAPE, 0], self.hwnd)

    def setup_inventory_for_selling(self):
        # When this method is called, the sell_etc_items should ALWAYS be called right afterwards

        self.ensure_inventory_is_open()
        self.ensure_inventory_is_expanded()

        # Get to Etc Inventory
        while True:
            if not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Inventory Images', option='etc_inventory'), cv2.IMREAD_COLOR), threshold=0.8)):
                pyPostMessage('press', [win32con.VK_TAB, 0], self.hwnd)
            else:
                break
        self.inventory_merge_and_sort()
        self.move_cursor_to(*win32gui.ClientToScreen(self.hwnd, (random.randint(100, 200), random.randint(100, 200))))  # Move cursors away so as not to hide images

        # Get to Equip Inventory
        while True:
            if not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Inventory Images', option='equip_inventory'), cv2.IMREAD_COLOR), threshold=0.8)):
                pyPostMessage('press', [win32con.VK_TAB, 0], self.hwnd)
            else:
                break
        self.inventory_merge_and_sort()

    def sell_equip_items(self, nbr_sold=0):

        if nbr_sold == 0:
            self.click_fm_seller()

        self.move_cursor_to(*win32gui.ClientToScreen(self.hwnd, (random.randint(100, 200), random.randint(100, 200))))  # Move cursors away so as not to hide images
        time.sleep(0.5)

        i = 0
        while i <= 10:
            rect = find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Inventory Images', option='equip_tab_seller'), cv2.IMREAD_COLOR), threshold=0.8)
            if len(rect):
                break
            else:
                i += 1
        x, y = midpoint(self.hwnd, rect)
        self.click_at(x, y + 40)  # Click on first item to sell in the list, which is just slightly underneath the screenshot being detected

        time.sleep(1)
        haystack = self.take_screenshot()
        target = find_image(haystack, cv2.imread(self.config.get(section='Inventory Images', option='sell_item'), cv2.IMREAD_COLOR), threshold=0.8)
        x, y = midpoint(self.hwnd, target)
        item_sold = nbr_sold

        while item_sold < nbr_sold + 10:
            self.click_at(x, y)
            pyPostMessage('press', [0x59, 0], self.hwnd)  # Press 'Y' key
            time.sleep(random.uniform(0.01, 0.1))
            item_sold += 1
        self.move_cursor_to(random.randint(100, 200), random.randint(100, 200))
        return item_sold

    def sell_etc_items(self):
        # ALWAYS call this method after the sell_equip_items method.

        self.move_cursor_to(*win32gui.ClientToScreen(self.hwnd, (int(100), int(100))))  # Move cursors away so as not to hide images

        haystack = self.take_screenshot()
        etc_target = find_image(haystack, cv2.imread(self.config.get(section='Inventory Images', option='etc_tab_seller'), cv2.IMREAD_COLOR), threshold=0.9)
        x, y = midpoint(self.hwnd, etc_target)
        self.click_at(x, y)  # Go into the ETC tab within the npc's store

        # This method assumes that the inventory has been sorted already.
        while True:
            haystack = self.take_screenshot()
            sweat_bead = find_image(haystack, cv2.imread(self.config.get(section='Inventory Images', option='sweat_bead'), cv2.IMREAD_COLOR), threshold=0.9)
            veetron_horn = find_image(haystack, cv2.imread(self.config.get(section='Inventory Images', option='veetron_horn'), cv2.IMREAD_COLOR), threshold=0.9)
            leave_store = find_image(haystack, cv2.imread(self.config.get(section='Inventory Images', option='leave_store'), cv2.IMREAD_COLOR), threshold=0.8)

            if len(sweat_bead):
                x, y = midpoint(self.hwnd, sweat_bead[0])
                self.double_click_at(x + 40, y)  # offset such that the cursor does not hinder the next screenshot
                pyPostMessage('press', [win32con.VK_RETURN, 0], self.hwnd)
                time.sleep(0.25)

            elif len(veetron_horn):
                x, y = midpoint(self.hwnd, veetron_horn[0])
                self.double_click_at(x + 40, y)  # offset such that the cursor does not hinder the next screenshot
                pyPostMessage('press', [win32con.VK_RETURN, 0], self.hwnd)
                time.sleep(0.25)
            else:
                x, y = midpoint(self.hwnd, leave_store)
                self.click_at(x, y)
                break

    def map_sequence_1(self):

        self.ensure_mount_is_used()
        self.jump_right_for(2)
        time.sleep(1.5)

    def map_sequence_2(self):

        self.jump_right_for(1)
        time.sleep(1.5)

    def map_sequence_3(self):

        cond = """len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='left_ladder'), cv2.IMREAD_COLOR)))"""
        self.move_right_until(expression=cond, timeout=5)
        self.move_right_for(0.4)


    def map_sequence_4(self):

        self.ensure_mount_is_used()
        self.jump_left_for(3)

    def map_sequence_5(self):

        cond = """len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='target_sequence_2'), cv2.IMREAD_COLOR)))"""
        self.move_left_until(expression=cond, timeout=6)
        time.sleep(0.2)

    def map_sequence_6(self):

        self.move_left_for(0.5)
        time.sleep(1.25)
        self.jump_right()
        time.sleep(0.75)

    def map_sequence_7(self):

        self.ensure_mount_is_used()
        time.sleep(0.75)
        self.jump_right()
        time.sleep(0.75)
        self.move_right_for(1)
        self.move_left_for(1)
        self.jump_right()
        time.sleep(1)

    def map_sequence_8(self):

        cond = """len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Character Images', option='looter_backhead'), cv2.IMREAD_COLOR), threshold=0.8))"""
        self.move_right_and_down_until(expression=cond, timeout=9)
        self.move_down_for(1.5)

    def map_sequence_9(self):

        self.jump_left()
        time.sleep(1.25)
        self.jump_down()
        time.sleep(0.6)
        self.jump_down()
        self.move_right_for(1.5)

    def map_sequence_10(self):

        cond = """len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='target_sequence_4'), cv2.IMREAD_COLOR)))"""
        self.jump_left_for(2)
        self.move_left_until(expression=cond, timeout=8)

    def map_sequence_11(self):

        self.move_left_for(0.5)
        self.jump_right_for(3.5)
        time.sleep(1.5)

