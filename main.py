import win32gui
from configparser import ConfigParser
from LooterManager import LooterManager
from ImageDetection import find_image
from MageManager import MageManager
import multiprocessing
import psutil
import time
import cv2
import random


user = 'Nass'
config = ConfigParser()
config.read('common_config.ini')

if user == 'Nass':
    config.read('config_nass.ini')
else:
    config.read('config_lec.ini')  # TODO
config.read(config.get(section='Login Credentials', option='path'))


# Guarding = LooterManager(config=config, ign='Guarding')
Goldmine1 = MageManager(config=config, ign='Goldmine1')
# Goldmine2 = MageManager(config=config, ign='Goldmine2')
# Goldmine3 = MageManager(config=config, ign='Goldmine3')
LegalizeIt = MageManager(config=config, ign='LegalizeIt')

# Goldmine1 = MageManager(config=config)


def bot_farmer():

    LegalizeIt.cast_mg()
    mg_time = time.time()
    next_mg = random.randint(450, 550)
    time.sleep(1.5)

    LegalizeIt.cast_infinity()
    inf_time = time.time()
    next_inf = random.randint(605, 650)
    time.sleep(0.5)

    while True:
        val = LegalizeIt.farm_mode('bot')
        if val:
            time.sleep(2.8)
            if time.time() > mg_time + next_mg:
                LegalizeIt.cast_mg()
                mg_time = time.time()
                time.sleep(1.5)

            elif time.time() > inf_time + next_inf:
                LegalizeIt.cast_infinity()
                inf_time = time.time()
                time.sleep(0.5)


def top_farmer():

    Goldmine1.cast_mg()
    mg_time = time.time()
    next_mg = random.randint(450, 550)
    time.sleep(1.5)

    Goldmine1.cast_infinity()
    inf_time = time.time()
    next_inf = random.randint(605, 650)
    time.sleep(0.5)

    while True:
        val = Goldmine1.farm_mode('top')
        if val:
            time.sleep(2.8)
            if time.time() > mg_time + next_mg:
                Goldmine1.cast_mg()
                mg_time = time.time()
                time.sleep(1.5)

            elif time.time() > inf_time + next_inf:
                Goldmine1.cast_infinity()
                inf_time = time.time()
                time.sleep(0.5)

if __name__ == '__main__':

    loop_time = time.time()
    proc1 = multiprocessing.Process(target=top_farmer)
    proc2 = multiprocessing.Process(target=bot_farmer)
    proc1.start()
    proc2.start()

    proc1.join()
    proc2.join()

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