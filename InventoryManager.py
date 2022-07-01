from BasicCommands import ClientManager
import cv2
import numpy as np
import pyautogui
import pytesseract
from matplotlib import pyplot as plt

# TODO Create an actual config file
configurations={'EmptyCellValue': 236,
                'EmptyCellThreshold': 0.99,
                'EmptyCellPath': 'KeyImages/EmptyInventoryCell.png',
                'IGN': 'Guarding',
                'InventoryTitlePath': 'KeyImages/InventoryTitle.png',
                'InventorySlotMergePath': 'KeyImages/InventorySlotMerge.png',
                'InventorySortPath': 'KeyImages/InventorySort.png'}

# For now, we are assuming the large (1024x768) client is always used for inventory management.
# This class will take in images from client regularly to assess the status of inventory
# Goal is that it will be capable of determining which items are to be kept and which are to sell
# It should also know when it is time to go npc (aka when inventory is full)
class InventoryManager(ClientManager):
    def __init__(self, config):
        super().__init__(config['IGN'])

        # TODO Create methods to re-size those config for small client
        self.empty_cell = config['EmptyCellPath']
        self.inv_title = config['InventoryTitlePath']
        self.inv_slot_merge = config['InventorySlotMergePath']
        self.inv_sort = config['InventorySortPath']

    def confirm_inventory_is_open(self):
        if pyautogui.locateOnScreen(image=self.inv_title, region=self.client.box) is not None:
            return True
        else:
            return False

    def get_number_of_empty_inventory_space(self):
        if not self.confirm_inventory_is_open():
            self.toggle_inventory()

        empty_spaces = len(list(pyautogui.locateAllOnScreen(image=self.empty_cell, region=self.client.box)))
        self.toggle_inventory()
        return empty_spaces

    def merge_inventory(self):
        if not self.confirm_inventory_is_open():
            self.toggle_inventory()

        try:
            x, y = pyautogui.locateCenterOnScreen(image=self.inv_slot_merge, region=self.client.box)

        except TypeError:
            self.toggle_inventory()
            self.toggle_inventory()
            x, y = pyautogui.locateCenterOnScreen(image=self.inv_slot_merge, region=self.client.box)

        self.click_at(x, y)
        return x, y

    def sort_inventory(self, x, y):
        if not self.confirm_inventory_is_open():
            self.toggle_inventory()

        self.click_at(x, y)

    def merge_and_sort_inventory(self):
        x, y = self.merge_inventory()
        self.sort_inventory(x, y)


# test = InventoryManager(config=configurations)
# test.merge_and_sort_inventory()
# TODO Take a bunch of screenshots along with the real number of available space, and run on each to see if output
# TODO is always consistent
