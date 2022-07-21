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

user = 'Nass'
config = ConfigParser()
config.read('common_config.ini')

if user == 'Nass':
    config.read('config_nass.ini')
else:
    config.read('config_lec.ini')  # TODO
config.read(config.get(section='Login Credentials', option='path'))

if __name__ == '__main__':

    # test = MageManager(config, 'LegalizeIt', 'top')
    #
    # while True:
    #     if test.reposition_needed():
    #         print('reposition needed')
    #         test.reposition()
    #     ult_cast = test.farm()
    #     if ult_cast:
    #         time.sleep(3)

        # haystack = test.take_screenshot()
        # curr_pos = test.find_self()
        # rects_left = find_image(haystack, test.left_positioning_target)
        # rects_right = find_image(haystack, test.right_positioning_target)
        #
        # if len(rects_left) and len(curr_pos):
        #     self_x, self_y = midpoint(test.hwnd, curr_pos)
        #     target_x, target_y = midpoint(test.hwnd, rects_left)
        #     print('Horizontal distance with left target: {}'.format(self_x - target_x))
        #
        # if len(rects_right) and len(curr_pos):
        #     self_x, self_y = midpoint(test.hwnd, curr_pos)
        #     target_x, target_y = midpoint(test.hwnd, rects_right)
        #     print('Horizontal distance with right target: {}'.format(self_x - target_x))
        #
        # time.sleep(1)

    # test = MageManager(config, 'LegalizeIt', 'bot')
    # test = LooterManager(config, 'Guarding')
    # init_control_gui()
    # test.ensure_inventory_is_open()
    # haystack = test.take_screenshot()
    # needle = cv2.imread(config.get(section='Inventory Images', option='craven'), cv2.IMREAD_COLOR)
    # rects = find_image(haystack, needle)
    # filter = HsvFilter(hMin=0,
    #                    sMin=0,
    #                    vMin=255,
    #                    hMax=0,
    #                    sMax=0,
    #                    vMax=255,
    #                    sAdd=0,
    #                    sSub=0,
    #                    vAdd=0,
    #                    vSub=0)
    # i = 0
    # for rect in rects:
    #     i += 1
    #     x, y, w, h = rect
    #     click_x, click_y = midpoint(test.hwnd, rect)  # Do not use the midpoint function to crop screenshots - the midpoint returns location on the actual screen, not on the screenshot
    #     test.move_cursor_to(click_x, click_y)
    #     dimensions = {
    #         'width': 50,
    #         'height': 45,
    #         'crop_x': int(x + w/2 + 110),
    #         'crop_y': int(y + h/2 + test.titlebar_pixels) + 210
    #     }
    #     image_test = test.take_screenshot(dim=dimensions)
    #     processed = apply_hsv_filter(image_test, filter)
    #     # cv2.imwrite('KeyImages/Inventory/Stats/RedPirateTop/image' + str(i) + '.png', processed)
    #     cv2.imshow('test', processed)
    #     if cv2.waitKey(3000) == ord('q'):
    #         cv2.destroyAllWindows()
    #         break

    manager = QueueManager(config)

    proc1 = multiprocessing.Process(target=manager.looter)
    proc2 = multiprocessing.Process(target=manager.bishop)
    proc3 = multiprocessing.Process(target=manager.mage, args=('Goldmine1', 'bot', 'second', ))
    proc4 = multiprocessing.Process(target=manager.mage, args=('Goldmine2', 'top', 'first', ))
    proc5 = multiprocessing.Process(target=manager.mage, args=('Goldmine3', 'top', 'second', ))

    # proc1 = multiprocessing.Process(target=manager.looter, args=('MidN',))
    # proc2 = multiprocessing.Process(target=manager.bishop, args=('GriZ', 'bot'))
    # proc3 = multiprocessing.Process(target=manager.mage, args=('Zushy', 'bot', 'second', ))
    # proc4 = multiprocessing.Process(target=manager.mage, args=('ZirG', 'top', 'first', ))
    # proc5 = multiprocessing.Process(target=manager.mage, args=('Leake', 'top', 'second', ))
    #
    print('time started {}'.format(time.strftime('%H:%M:%S', time.localtime())))
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



