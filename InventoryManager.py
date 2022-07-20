import cv2
import os
import pandas as pd
import win32gui
import pyautogui
import pytesseract
from matplotlib import pyplot as plt
from HsvFiltering import HsvFilter, apply_hsv_filter
from ImageDetection import find_image, midpoint
import time
import random


class InventoryManager:

    filter = HsvFilter(hMin=0,
                       sMin=0,
                       vMin=255,
                       hMax=0,
                       sMax=0,
                       vMax=255,
                       sAdd=0,
                       sSub=0,
                       vAdd=0,
                       vSub=0)

    inventory_title_midpoint_offset_x = -30
    inventory_title_midpoint_offset_y = 55
    box_x_dim = 38
    box_y_dim = 35

    def __init__(self, client):

        self.client = client
        self.total_item_kept = 0
        inv_offsets_x = [self.inventory_title_midpoint_offset_x + self.box_x_dim * (i % 4 + 4 * (i // 24)) for i in range(96)]
        inv_offsets_y = [self.inventory_title_midpoint_offset_y + self.box_y_dim * (i // 4 - 6 * (i // 24)) for i in range(96)]
        self.inventory_offsets = pd.DataFrame(data={'x': inv_offsets_x, 'y': inv_offsets_y}, index=range(96))

        self.craven = {
            'image': cv2.imread(self.client.config.get(section='Inventory Images', option='craven'), cv2.IMREAD_COLOR),
            'meaningful stats': ['atk'],
            'box': {'width': 30,
                    'height': 20,
                    'crop_x': 108,
                    'crop_y': 238},
            'stats path': 'KeyImages/Inventory/Stats/RedCraven/'
        }

        self.blood_dagger = {
            'image': cv2.imread(self.client.config.get(section='Inventory Images', option='blood_dagger'), cv2.IMREAD_COLOR),
            'meaningful stats': ['atk'],
            'box': {'width': 29,
                    'height': 15,
                    'crop_x': 110,
                    'crop_y': 230},
            'stats path': 'KeyImages/Inventory/Stats/BloodDagger/'
        }

        self.red_pirate_pants = cv2.imread(self.client.config.get(section='Inventory Images', option='red_pirate_pants'), cv2.IMREAD_COLOR)
        self.red_pirate_pants_dexbox = {'width': 30,
                                      'height': 15,
                                      'crop_x': 40,
                                      'crop_y': 185}
        self.red_pirate_pants_lukbox = {'width': 30,
                                      'height': 15,
                                      'crop_x': 40,
                                      'crop_y': 200}

        self.red_pirate_top = cv2.imread(self.client.config.get(section='Inventory Images', option='red_pirate_top'), cv2.IMREAD_COLOR)
        self.red_pirate_top_dexbox = {'width': 30,
                                      'height': 15,
                                      'crop_x': 40,
                                      'crop_y': 185}
        self.red_pirate_top_lukbox = {'width': 30,
                                      'height': 15,
                                      'crop_x': 40,
                                      'crop_y': 200}

        # TODO: still need to test 12-7, 12-6, 11-8!
        self.white_pioneer = {
            'image': cv2.imread(self.client.config.get(section='Inventory Images', option='white_pioneer'), cv2.IMREAD_COLOR),
            'meaningful stats': ['str', 'dex'],
            'box': {'width': 26,
                    'height': 26,
                    'crop_x': 44,
                    'crop_y': 217},
            'stats path': 'KeyImages/Inventory/Stats/WhitePioneer'
        }


        self.all_items = [self.craven, self.blood_dagger, self.white_pioneer]

    def loop_through_all(self):
        nbr_to_keep = 0
        self.client.ensure_inventory_is_open()

        # Moving the inventory towards the left, such that the item stat box always follow the cursor (if the inventory is too far right within client, this is not the case)
        rect = find_image(self.client.take_screenshot(), cv2.imread(self.client.config.get(section='Inventory Images', option='inventory_title'), cv2.IMREAD_COLOR), threshold=0.9)
        if len(rect):
            x, y = midpoint(self.client.hwnd, rect)
            self.client.move_cursor_to(x, y)
            target_x, target_y = win32gui.ClientToScreen(self.client.hwnd, (115, 225))
            self.client.drag_to(target_x, target_y)
            rand_x, rand_y = win32gui.ClientToScreen(self.client.hwnd, (random.randint(10, 45), random.randint(10, 45)))
            self.client.move_cursor_to(rand_x, rand_y)

        for i in self.all_items:
            nbr_to_keep = self.loop_through_items_in_inventory(i, nbr_to_keep)

        print('Successfully sorted {} items'.format(nbr_to_keep))
        self.total_item_kept += nbr_to_keep
        self.client.toggle_inventory()

        return nbr_to_keep

    def loop_through_items_in_inventory(self, item, item_kept):

        self.client.ensure_inventory_is_open()

        img_inv = self.client.take_screenshot()
        rects = find_image(img_inv, item['image'])
        if len(rects):
            for rect in rects:

                x, y, w, h = rect
                x += w/2
                y += h/2
                screen_x, screen_y = midpoint(self.client.hwnd, rect)
                self.client.move_cursor_to(screen_x, screen_y)
                time.sleep(0.1)

                dim = item['box'].copy()
                dim['crop_x'] += int(x)
                dim['crop_y'] += int(y)

                stat_img = apply_hsv_filter(self.client.take_screenshot(dim=dim), self.filter)
                # cv2.imshow('test', stat_img)
                # cv2.waitKey(10000)
                item_kept += self.loop_through_stats(item, stat_img, item_kept)

        return item_kept

    def loop_through_stats(self, item, stat_to_find, item_kept):
        for file in os.listdir(item['stats path']):
            haystack = cv2.imread(os.path.join(item['stats path'], file), cv2.IMREAD_COLOR)
            if len(find_image(haystack, stat_to_find, threshold=0.975)):
                self.move_to_top(item_kept)
                return 1
        return 0

    def move_to_top(self, item_kept):
        offset_x, offset_y = self.inventory_offsets.iloc[item_kept]
        target_x, target_y = win32gui.ClientToScreen(self.client.hwnd, (115+offset_x, 225+offset_y))
        self.client.drag_to(target_x, target_y)
        self.client.click()
        time.sleep(0.25)
