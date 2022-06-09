import ctypes
import win32gui
import pyautogui
from LooterManager import LooterManager
from MageManager import MageManager
import multiprocessing

configurations_loot={'EmptyCellValue': 236,
                'EmptyCellThreshold': 0.99,
                'YellowDotPath': 'KeyImages/MapNavigation/YellowDot.png',
                'MapToggled': 'KeyImages/MapNavigation/MapProperlyToggled.png',
                'MapRect': 5,
                'IGN': 'Guarding',
                'Sequence_1_Target': 'KeyImages/MapNavigation/Target_Sequence1.png'}

configurations_mage={'EmptyCellValue': 236,
                'EmptyCellThreshold': 0.99,
                'YellowDotPath': 'KeyImages/MapNavigation/YellowDot.png',
                'MapToggled': 'KeyImages/MapNavigation/MapProperlyToggled.png',
                'MapRect': 5,
                'IGN': 'LegalizeIt',
                'Sequence_1_Target': 'KeyImages/MapNavigation/Target_Sequence1.png'}

Guarding = LooterManager(config=configurations_loot)
LegalizeIt = MageManager(config=configurations_mage)

def loot():
    Guarding.use_stance()
    Guarding.ensure_mount_is_used()
    Guarding.map_sequence_1()
    Guarding.map_sequence_2()
    Guarding.map_sequence_3()
    Guarding.map_sequence_4()

def farm():
    LegalizeIt.farm_mode()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    proc1 = multiprocessing.Process(target=loot)
    proc2 = multiprocessing.Process(target=farm)
    proc1.start()
    proc2.start()