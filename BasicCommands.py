import win32con
import win32gui
import cv2
import pydirectinput
import random
import time
from PostMessage import pyPostMessage
from BasicMovements import BasicMovements
from ImageDetection import find_image, midpoint


class BasicCommands(BasicMovements):

    def __init__(self, config, ign):
        super().__init__(config, ign)

    def toggle_character_stats(self):

        key_config = eval(self.config.get(section='KEYBINDS - Common', option='characterstatskey'))
        pyPostMessage('press', key_config, self.hwnd)

    def toggle_inventory(self):

        key_config = eval(self.config.get(section='KEYBINDS - Common', option='inventorykey'))
        pyPostMessage('press', key_config, self.hwnd)

    def toggle_chatfeed(self):

        key_config = eval(self.config.get(section='KEYBINDS - Common', option='togglechatfeedkey'))
        pyPostMessage('press', key_config, self.hwnd)

    def toggle_minimap(self):

        key_config = eval(self.config.get(section='KEYBINDS - Common', option='minimapkey'))
        pyPostMessage('press', key_config, self.hwnd)

    def toggle_equip_window(self):
        key_config = eval(self.config.get(section='KEYBINDS - Common', option='equipwindowkey'))
        pyPostMessage('press', key_config, self.hwnd)

    def toggle_buddy_list(self):
        key_config = eval(self.config.get(section='KEYBINDS - Common', option='togglebuddylist'))
        pyPostMessage('press', key_config, self.hwnd)

    def click(self):
        self.client.activate()
        pydirectinput.click()

    def feed_pet(self):

        key_config = eval(self.config.get(section='KEYBINDS - Common', option='petfoodkey'))
        pyPostMessage('press', key_config, self.hwnd)
        return random.randint(450, 600)

    def feed_multiple_pets(self, nbr_press):
        for i in range(nbr_press):
            timer = self.feed_pet()
        return timer

    def click_at(self, x, y):
        self.client.activate()
        pydirectinput.click(int(x), int(y))

    def double_click_at(self, x, y):
        self.client.activate()
        pydirectinput.doubleClick(int(x), int(y))

    def move_cursor_to(self, x, y):
        pydirectinput.moveTo(int(x), int(y))

    def drag_to(self, x, y):
        pydirectinput.mouseDown()
        pydirectinput.moveTo(int(x), int(y))
        pydirectinput.mouseUp()
        x, y = win32gui.ClientToScreen(self.hwnd, (10, 10))
        pydirectinput.moveTo(x, y)

    def check_pots_left(self):
        pass

    def allchat(self):

        key_config = eval(self.config.get(section='KEYBINDS - Common', option='allchatkey'))
        pyPostMessage('press', key_config, self.hwnd)

    def type_message(self, message):

        # This assumes all characters are "standard" (from A-Z, 0-9)
        for char in message:
            pyPostMessage('write', [ord(char), 0], self.hwnd)

        pyPostMessage('press', [win32con.VK_RETURN, 0], self.hwnd)
        pyPostMessage('press', [win32con.VK_ESCAPE, 0], self.hwnd)

    def mapowner(self):

        self.allchat()
        self.type_message('~mapowner')

    def ensure_pet_is_on(self):
        self.ensure_equip_window_is_open()
        if len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Misc Images', option='pet_is_off'), cv2.IMREAD_COLOR), threshold=0.99)):
            self.turn_pets_on()
        self.toggle_equip_window()

    def ensure_equip_window_is_open(self):
        if not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Inventory Images', option='equip_window'), cv2.IMREAD_COLOR), threshold=0.99)):
            self.toggle_equip_window()

    def ensure_inventory_is_open(self):
        if not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Inventory Images', option='inventory_title'), cv2.IMREAD_COLOR), threshold=0.99)):
            self.toggle_inventory()

    def ensure_inventory_is_expanded(self):
        rect = find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Inventory Images', option='inventory_collapsed'), cv2.IMREAD_COLOR), threshold=0.99)
        if len(rect):
            x, y = midpoint(self.hwnd, rect)
            self.click_at(x, y)

    def inventory_merge_and_sort(self):
        rect = find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Inventory Images', option='inventory_merge'), cv2.IMREAD_COLOR), threshold=0.99)
        if len(rect):
            x, y = midpoint(self.hwnd, rect)
            self.click_at(x, y)
            time.sleep(0.2)
            self.click_at(x, y)

    def turn_pets_on(self):

        self.ensure_inventory_is_open()

        # Get to Cash Inventory
        while True:
            if not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Inventory Images', option='cash_inventory'), cv2.IMREAD_COLOR), threshold=0.99)):
                pyPostMessage('press', [win32con.VK_TAB, 0], self.hwnd)
            else:
                break
        pet_images = eval(self.config.get(section='Pet Images', option='pets'))[self.ign]
        haystack = self.take_screenshot()
        for image in pet_images:
            rect = find_image(haystack, cv2.imread(image, cv2.IMREAD_COLOR), threshold=0.99)
            if len(rect):
                x, y = midpoint(self.hwnd, rect)
                self.double_click_at(x, y)

            rect_multi_pet_trigger = find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Inventory Images', option='multi_pet_trigger'), cv2.IMREAD_COLOR), threshold=0.99)
            if len(rect_multi_pet_trigger):
                x, y, w, h = list(*rect_multi_pet_trigger)
                offset_x, offset_y = win32gui.ClientToScreen(self.hwnd, (x, y))
                offset_x += 0.9 * w
                offset_y += 0.9 * h
                self.click_at(int(offset_x), int(offset_y))

        self.toggle_inventory()

    def setup_hp_pots(self, pots_image):

        self.ensure_inventory_is_open()
        curr_pos = find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Inventory Images', option='inventory_title'), cv2.IMREAD_COLOR), threshold=0.99)
        x, y, w, h = list(*curr_pos)
        center_x, center_y = win32gui.ClientToScreen(self.hwnd, (x, y))
        center_x += w / 2
        center_y += h / 2

        target_x, target_y = win32gui.ClientToScreen(self.hwnd, (400, 50))
        self.move_cursor_to(int(center_x), int(center_y))
        self.drag_to(target_x, target_y)


        # Get to Use Inventory
        while True:
            if not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Inventory Images', option='use_inventory'), cv2.IMREAD_COLOR), threshold=0.99)):
                pyPostMessage('press', [win32con.VK_TAB, 0], self.hwnd)
            else:
                break

        rect_potions = find_image(self.take_screenshot(), pots_image, threshold=0.9)
        if len(rect_potions):
            if len(rect_potions) > 1:
                x, y, w, h = rect_potions[0]
            else:
                x, y, w, h = list(*rect_potions)
            center_x, center_y = win32gui.ClientToScreen(self.hwnd, (x, y))
            center_x += w/2
            center_y += h/2
            self.click_at(int(center_x), int(center_y))

        target = cv2.imread(self.config.get(section='Inventory Images', option='auto_hp'), cv2.IMREAD_COLOR)
        rect_target = find_image(self.take_screenshot(), target, threshold=0.95)
        if len(rect_target):
            x, y, w, h = list(*rect_target)
            center_x, center_y = win32gui.ClientToScreen(self.hwnd, (x, y))
            center_x += w/2 + 30  # Offset by 30 pixels to get into the actual square where potions should be placed
            center_y += h/2
            self.click_at(int(center_x), int(center_y))
            pyPostMessage('press', [win32con.VK_ESCAPE, 0], self.hwnd)
        self.toggle_inventory()

    def setup_mp_pots(self, pots_image):
        self.ensure_inventory_is_open()

        # Get to Use Inventory
        while True:
            if not len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Inventory Images', option='use_inventory'), cv2.IMREAD_COLOR), threshold=0.99)):
                pyPostMessage('press', [win32con.VK_TAB, 0], self.hwnd)
            else:
                break

        rect_potions = find_image(self.take_screenshot(), pots_image, threshold=0.9)
        if len(rect_potions):
            if len(rect_potions) > 1:
                x, y, w, h = rect_potions[0]
            else:
                x, y, w, h = list(*rect_potions)
            center_x, center_y = win32gui.ClientToScreen(self.hwnd, (x, y))
            center_x += w / 2
            center_y += h / 2
            self.click_at(int(center_x), int(center_y))

        target = cv2.imread(self.config.get(section='Inventory Images', option='auto_mp'), cv2.IMREAD_COLOR)
        rect_target = find_image(self.take_screenshot(), target, threshold=0.95)
        if len(rect_target):
            x, y, w, h = list(*rect_target)
            center_x, center_y = win32gui.ClientToScreen(self.hwnd, (x, y))
            center_x += w / 2 + 30  # Offset by 30 pixels to get into the actual square where potions should be placed
            center_y += h / 2
            self.click_at(int(center_x), int(center_y))
            pyPostMessage('press', [win32con.VK_ESCAPE, 0], self.hwnd)
        self.toggle_inventory()

    def find_self(self):
        pass
