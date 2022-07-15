from BasicCommands import ClientManager
import cv2
import numpy as np
import pyautogui
import pytesseract
from matplotlib import pyplot as plt

class InventoryManager:

    cursor_itembox_offset_x = 10
    cursor_itembox_offset_y = 165  # The cropping is always the same except for unique/untradeable items, but we won't be looking at those items anyways
    itembox_width = 225  # The width is the same for all equip items

    def __init__(self, client):

        self.client = client

        self.craven = cv2.imread(self.client.config.get(section='Inventory Images', option='craven'), cv2.IMREAD_COLOR)
        self.craven_box_height = 90
naw
