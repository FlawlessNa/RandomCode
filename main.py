import win32gui
from configparser import ConfigParser
from LooterManager import LooterManager
from ImageDetection import find_image, midpoint
from QueueManagement import QueueManager
from MageManager import MageManager
import multiprocessing
import psutil
import time
import cv2
import random
from PostMessage import pyPostMessage
import pytesseract

user = 'Nass'
config = ConfigParser()
config.read('common_config.ini')

if user == 'Nass':
    config.read('config_nass.ini')
else:
    config.read('config_lec.ini')  # TODO
config.read(config.get(section='Login Credentials', option='path'))

if __name__ == '__main__':

    # pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    # test = MageManager(config, 'LegalizeIt')
    # test.ensure_inventory_is_open()
    #
    # haystack = test.take_screenshot()
    # needle = cv2.imread(config.get(section='Inventory Images', option='craven'), cv2.IMREAD_COLOR)
    # rects = find_image(haystack, needle)
    # for rect in rects:
    #     x, y, w, h = rect
    #     click_x, click_y = midpoint(test.hwnd, rect)  # Do not use the midpoint function to crop screenshots - the midpoint returns location on the actual screen, not on the screenshot
    #     test.move_cursor_to(click_x, click_y)
    #     dimensions = {
    #         'width': 225,
    #         'height': 230 - 140,
    #         'crop_x': int(x + w/2 + 10),
    #         'crop_y': int(y + h/2 + test.titlebar_pixels + 25) + 140
    #     }
    #     image_test = test.take_screenshot(dim=dimensions)
    #     image_test = cv2.GaussianBlur(image_test, (3, 3), 1)
    #     # ret, image_test = cv2.threshold(image_test, 150, 255, cv2.THRESH_BINARY)
    #     craven_data = pytesseract.image_to_string(image_test)
    #     print('data:', craven_data)
    #
    #     cv2.imshow('test', image_test)
    #     cv2.waitKey(0)

    manager = QueueManager(config)

    proc1 = multiprocessing.Process(target=manager.looter)
    proc2 = multiprocessing.Process(target=manager.bishop)
    proc3 = multiprocessing.Process(target=manager.bot_mage, args=('Goldmine1', ))
    proc4 = multiprocessing.Process(target=manager.top_mage, args=('Goldmine2', 1, ))
    proc5 = multiprocessing.Process(target=manager.top_mage, args=('Goldmine3', 2, ))

    proc1.start()
    proc2.start()
    proc3.start()
    proc4.start()
    proc5.start()

    proc1.join()
    proc2.join()
    proc3.join()
    proc4.join()
    proc5.join()

