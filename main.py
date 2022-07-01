import win32gui
from configparser import ConfigParser
from LooterManager import LooterManager
from ImageDetection import find_image
from MageManager import MageManager
import multiprocessing
import psutil
import time
import cv2

user = 'Nass'
config = ConfigParser()
config.read('common_config.ini')

if user == 'Nass':
    config.read('config_nass.ini')
else:
    config.read('config_lec.ini') # TODO
config.read(config.get(section='Login Credentials', option='path'))


Guarding = LooterManager(config=config, ign='Guarding')
# Goldmine1 = MageManager(config=config, ign='Goldmine1')
# Goldmine2 = MageManager(config=config, ign='Goldmine2')
# Goldmine3 = MageManager(config=config, ign='Goldmine3')
# LegalizeIt = MageManager(config=config, ign='LegalizeIt')

# Goldmine1 = MageManager(config=config)

def loot():
    Guarding.use_stance()
    Guarding.ensure_mount_is_used()
    Guarding.map_sequence_1()
    Guarding.map_sequence_2()
    Guarding.map_sequence_3()
    Guarding.map_sequence_4()

def farm1():
    LegalizeIt.farm_mode()

def farm2():
    Goldmine1.farm_mode()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    window_rect = win32gui.GetWindowRect(Guarding.hwnd)
    loop_time = time.time()
    images = []
    for item in config.items(section='MOB Images'):
        imgs = eval(item[1])
        images.extend(imgs)
    needles = [cv2.imread(image, cv2.IMREAD_COLOR) for image in images]

    while(True):

        haystack = Guarding.take_screenshot()
        for needle in needles:
            haystack = find_image(haystack, needle, threshold=0.8, method=cv2.TM_CCOEFF_NORMED)

        cv2.imshow('Screenshots', haystack)

        print('FPS {}'.format(1 / (time.time() - loop_time)))
        loop_time = time.time()

        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break

    # result = cv2.matchTemplate()

    # Guarding.move_right_and_up_by(200)
    # Guarding.setup_hp_threshold()
    # Guarding.setup_mp_threshold()
    # Guarding.ensure_mount_is_used()
    # Guarding.map_sequence_1()
    # Guarding.map_sequence_2()
    # Guarding.map_sequence_3()
    # Guarding.map_sequence_4()
    # proc1 = multiprocessing.Process(target=loot)
    # proc2 = multiprocessing.Process(target=farm1)
    # proc3 = multiprocessing.Process(target=farm2)
    # proc1.start()
    # proc2.start()
    # proc3.start()