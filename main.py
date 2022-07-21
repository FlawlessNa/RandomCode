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

    test = MageManager(config, 'LegalizeIt', 'bot')
    init_control_gui()

    while True:
        loop_time= time.time()
        sc = test.take_screenshot()
        processed_sc = apply_hsv_filter(sc)

        cv2.imshow('Processed Img', processed_sc)
        current_filters = get_hsv_filter_from_controls()

        # images = []
        # for item in config.items(section='MOB Images'):
        #     imgs = eval(item[1])
        #     images.extend(imgs)
        #
        # mobs = []
        # for image in images:
        #     mobs.append(find_image(sc, cv2.imread(image, cv2.IMREAD_COLOR), threshold=0.7))
        #
        # for mob in mobs:
        #     for rects in mob:
        #         x, y, w, h = rects
        #         cv2.rectangle(sc, (x, y), (x + w, y + h), (255, 0, 0), thickness=5)

        # cv2.imshow('Test', sc)
        print('FPS {}'.format(1 / (time.time() - loop_time)))
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break






    # manager = QueueManager(config)
    #
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



