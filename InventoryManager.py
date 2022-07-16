from BasicCommands import ClientManager
import cv2
import numpy as np
import pyautogui
import pytesseract
from matplotlib import pyplot as plt
from HsvFiltering import HsvFilter


class InventoryManager:

    cursor_itembox_offset_x = 10
    cursor_itembox_offset_y = 165  # The cropping is always the same except for unique/untradeable items, but we won't be looking at those items anyways
    itembox_width = 225  # The width is the same for all equip items
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

    def __init__(self, client):

        self.client = client

        self.craven = cv2.imread(self.client.config.get(section='Inventory Images', option='craven'), cv2.IMREAD_COLOR)
        self.craven_box = {'width': 30,
                           'height': 15,
                           'crop_x': 110,
                           'crop_y': 210}

        self.blood_dagger = cv2.imread(self.client.config.get(section='Inventory Images', option='blood_dagger'), cv2.IMREAD_COLOR)
        self.blood_dagger_box = {'width': 30,
                                 'height': 15,
                                 'crop_x': 110,
                                 'crop_y': 200}

        self.red_pirate_top = cv2.imread(self.client.config.get(section='Inventory Images', option='red_pirate_pants'), cv2.IMREAD_COLOR)
        self.red_pirate_top_dexbox = {'width': 30,
                                      'height': 15,
                                      'crop_x': 40,
                                      'crop_y': 185}
        self.red_pirate_top_lukbox = {'width': 30,
                                      'height': 15,
                                      'crop_x': 40,
                                      'crop_y': 200}
