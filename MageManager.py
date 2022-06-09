from ClientManager import ClientManager
import pydirectinput
import pyautogui
import win32con
import win32api

configurations={'EmptyCellValue': 236,
                'EmptyCellThreshold': 0.99,
                'YellowDotPath': 'KeyImages/MapNavigation/YellowDot.png',
                'MapToggled': 'KeyImages/MapNavigation/MapProperlyToggled.png',
                'MapRect': 5,
                'IGN': 'LegalizeIt',
                'Sequence_1_Target': 'KeyImages/MapNavigation/Target_Sequence1.png',
                'UltKey': win32con.VK_RCONTROL}

class MageManager(ClientManager):
    def __init__(self, config):
        super().__init__(config)

    def cast_ult(self):

        lparam_keydown = self.construct_lparams(repeat_count=1, key=self.config['UltKey'], WM_command=win32con.WM_KEYDOWN, extended_key=1, previous_key_state=0)
        lparam_keyup = self.construct_lparams(repeat_count=1, key=self.config['UltKey'], WM_command=win32con.WM_KEYUP, extended_key=1)

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, self.config['UltKey'], lparam_keydown)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, self.config['UltKey'], lparam_keyup)


    def check_pots_left(self):
        pass

    def rebuff(self):
        pass

    def farm_mode(self):
        while True:
            nbr_mobs = len(list(pyautogui.locateAllOnScreen(image='KeyImages/Veetron_left.png', region=self.client.box, confidence=0.9))) + \
                       len(list(pyautogui.locateAllOnScreen(image='KeyImages/Veetron_right.png', region=self.client.box, confidence=0.9))) + \
                       len(list(pyautogui.locateAllOnScreen(image='KeyImages/Berserkie_left.png', region=self.client.box, confidence=0.9))) + \
                       len(list(pyautogui.locateAllOnScreen(image='KeyImages/Berserkie_right.png', region=self.client.box, confidence=0.9)))
            if nbr_mobs >= 5:
                self.cast_ult()

# LegalizeIt = MageManager(config=configurations)
# LegalizeIt.cast_ult()