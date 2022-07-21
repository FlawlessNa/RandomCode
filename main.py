import win32gui
import win32con
from configparser import ConfigParser
from LooterManager import LooterManager
from ImageDetection import find_image, midpoint
from QueueManagement import QueueManager
from MageManager import MageManager
from InventoryManager import InventoryManager
import multiprocessing
import psutil
import time
import cv2
from HsvFiltering import init_control_gui, get_hsv_filter_from_controls, apply_hsv_filter, HsvFilter
import random
import os

user = 'Nass'
config = ConfigParser()
config.read('common_config.ini')

if user == 'Nass':
    config.read('config_nass.ini')
else:
    config.read('config_lec.ini')  # TODO
config.read(config.get(section='Login Credentials', option='path'))

if __name__ == '__main__':

    test = MageManager(config, 'LegalizeIt', 'top')

    while True:
        haystack = test.take_screenshot()
        test.reposition_needed()
        # rects_left = find_image(haystack, test.left_positioning_target)
        # rects_right = find_image(haystack, test.right_positioning_target)
        #
        # if len(rects_left):
        #     x, y, w, h = list(*rects_left)
        #     mid_x = x + w/2
        #     print('left target current pos is {}'.format(x))
        #
        # elif len(rects_right):
        #     x, y, w, h = list(*rects_right)
        #     mid_x = x + w / 2
        #     print('right target current pos is {}'.format(x))

        cv2.imshow('test', haystack)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break
    # manager = QueueManager(config)

    # proc1 = multiprocessing.Process(target=manager.looter)
    # proc2 = multiprocessing.Process(target=manager.bishop)
    # proc3 = multiprocessing.Process(target=manager.mage, args=('Goldmine1', 'bot', 'second', ))
    # proc4 = multiprocessing.Process(target=manager.mage, args=('Goldmine2', 'top', 'first', ))
    # proc5 = multiprocessing.Process(target=manager.mage, args=('Goldmine3', 'top', 'second', ))

    # proc1 = multiprocessing.Process(target=manager.looter, args=('MidN',))
    # proc2 = multiprocessing.Process(target=manager.bishop, args=('GriZ', 'bot'))
    # proc3 = multiprocessing.Process(target=manager.mage, args=('Zushy', 'bot', 'second', ))
    # proc4 = multiprocessing.Process(target=manager.mage, args=('ZirG', 'top', 'first', ))
    # proc5 = multiprocessing.Process(target=manager.mage, args=('Leake', 'top', 'second', ))

    # print('time started {}'.format(time.strftime('%H:%M:%S', time.localtime())))
    # proc1.start()
    # proc2.start()
    # proc3.start()
    # proc4.start()
    # proc5.start()
    #
    # proc1.join()
    # proc2.join()
    # proc3.join()
    # proc4.join()
    # proc5.join()



