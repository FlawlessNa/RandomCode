import ctypes
import win32gui
import pyautogui
from configparser import ConfigParser
import win32con
from LooterManager import LooterManager
from MageManager import MageManager
import multiprocessing
import psutil

user = 'Nass'
config = ConfigParser()
config.read('common_config.ini')

if user == 'Nass':
    config.read('config_nass.ini')
else:
    config.read('config_lec.ini') # TODO
config.read(config.get(section='Login Credentials', option='path'))


# Guarding = LooterManager(config=config, ign='Guarding')
# Goldmine1 = MageManager(config=config, ign='Goldmine1')
# Goldmine2 = MageManager(config=config, ign='Goldmine2')
# Goldmine3 = MageManager(config=config, ign='Goldmine3')
LegalizeIt = MageManager(config=config, ign='LegalizeIt')

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
    LegalizeIt.move_to_car()
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