import ctypes
import win32gui
import pyautogui
import win32con
from LooterManager import LooterManager
from MageManager import MageManager
import multiprocessing

configurations_loot={'EmptyCellValue': 236,
                'EmptyCellThreshold': 0.99,
                'YellowDotPath': 'KeyImages/MapNavigation/YellowDot.png',
                'MapToggled': 'KeyImages/MapNavigation/MapProperlyToggled.png',
                'MountImg': 'KeyImages/SilverMane.png',
                'MountKey': 0x58,  # chr(120) represents key 'x'
                'MountKeyExt': 0,
                'MapRect': 5,
                'IGN': 'Guarding',
                'Sequence_1_Target': 'KeyImages/MapNavigation/Target_Sequence1.png',
                'StanceKey': win32con.VK_END,
                'StanceKeyExt': 1,
                'PetFoodKey': 0x37,  # chr(55) represents key '7'
                'MountFoodKey': 0x38,  # chr(56) represents key '8'
                'MountFoodKeyExt': 0,
                'ToggleChatFeed': 0xDE,  # chr(222) represents key "'"
                'JumpKey': win32con.VK_MENU,  # The right ALT key
                'JumpKeyExt': 1
                }

configurations_mage1={'EmptyCellValue': 236,
                'EmptyCellThreshold': 0.99,
                'YellowDotPath': 'KeyImages/MapNavigation/YellowDot.png',
                'MapToggled': 'KeyImages/MapNavigation/MapProperlyToggled.png',
                'MapRect': 5,
                'IGN': 'LegalizeIt',
                'Sequence_1_Target': 'KeyImages/MapNavigation/Target_Sequence1.png',
                'UltKey': win32con.VK_RCONTROL,
                      'UltKeyExt': 1,
                      'TeleportKey': 0x43,
                      'TeleportKeyExt': 0}

configurations_mage2={'EmptyCellValue': 236,
                'EmptyCellThreshold': 0.99,
                'YellowDotPath': 'KeyImages/MapNavigation/YellowDot.png',
                'MapToggled': 'KeyImages/MapNavigation/MapProperlyToggled.png',
                'MapRect': 5,
                'IGN': 'Goldmine1',
                'Sequence_1_Target': 'KeyImages/MapNavigation/Target_Sequence1.png',
                'UltKey': win32con.VK_RCONTROL,
                      'UltKeyExt': 1,
                      'TeleportKey': 0x43,
                      'TeleportKeyExt': 0}

Guarding = LooterManager(config=configurations_loot)
LegalizeIt = MageManager(config=configurations_mage1)
Goldmine1 = MageManager(config=configurations_mage2)

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
    proc1 = multiprocessing.Process(target=loot)
    proc2 = multiprocessing.Process(target=farm1)
    proc3 = multiprocessing.Process(target=farm2)
    proc1.start()
    proc2.start()
    proc3.start()