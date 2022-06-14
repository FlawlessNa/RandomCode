from ClientManager import ClientManager
import pydirectinput
import pyautogui
import win32con
import win32api
import time

class MageManager(ClientManager):
    def __init__(self, config, ign):
        super().__init__(config, ign)

    def cast_ult(self):

        key, extended_param = eval(self.config.get(section='KEYBINDS - Mage', option='ultkey'))
        lparam_keydown = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYDOWN, extended_key=extended_param, previous_key_state=0)
        lparam_keyup = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYUP, extended_key=extended_param)

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, key, lparam_keydown)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, key, lparam_keyup)

    def teleport_left(self):

        self.client.activate()
        pydirectinput.keyDown('left')
        pydirectinput.press(self.config.get(section='KEYBINDS - Mage - pyautogui', option='teleportkey'))
        pydirectinput.keyUp('left')

    def teleport_right(self):
        self.client.activate()
        pydirectinput.keyDown('right')
        pydirectinput.press(self.config.get(section='KEYBINDS - Mage - pyautogui', option='teleportkey'))
        pydirectinput.keyUp('right')

    def cast_mg(self):

        key, extended_param = eval(self.config.get(section='KEYBINDS - Mage', option='mgkey'))

        lparam_keydown = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYDOWN, extended_key=extended_param, previous_key_state=0)
        lparam_keyup = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYUP, extended_key=extended_param)

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, key, lparam_keydown)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, key, lparam_keyup)

    def cast_infinity(self):

        key, extended_param = eval(self.config.get(section='KEYBINDS - Mage', option='infinitykey'))

        lparam_keydown = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYDOWN, extended_key=extended_param, previous_key_state=0)
        lparam_keyup = self.construct_lparams(repeat_count=1, key=key, wm_command=win32con.WM_KEYUP, extended_key=extended_param)

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, key, lparam_keydown)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, key, lparam_keyup)

    def reposition(self, target):
        char_pos = pyautogui.locateOnScreen(image='KeyImages/MasterAdventurer.png', region=self.client.box, confidence=0.95)
        target_pos = pyautogui.locateOnScreen(image=target, region=self.client.box, confidence=0.95)
        if char_pos is not None and target_pos is not None:
            if target_pos.left - char_pos.left > 150:
                self.move_right_for(1)
            elif char_pos.left - target_pos.left > 150:
                self.move_left_for(1)
        print(char_pos)
        print(target_pos)


    def detect_mobs(self, mob_image):
        return len(list(pyautogui.locateAllOnScreen(image=mob_image, region=self.client.box, confidence=0.9)))

    def farm_mode(self, target_position):
        while True:
            nbr_mobs = len(list(pyautogui.locateAllOnScreen(image='KeyImages/Veetron_left.png', region=self.client.box, confidence=0.9))) + \
                       len(list(pyautogui.locateAllOnScreen(image='KeyImages/Veetron_right.png', region=self.client.box, confidence=0.9))) + \
                       len(list(pyautogui.locateAllOnScreen(image='KeyImages/Berserkie_left.png', region=self.client.box, confidence=0.9))) + \
                       len(list(pyautogui.locateAllOnScreen(image='KeyImages/Berserkie_right.png', region=self.client.box, confidence=0.9)))
            if nbr_mobs >= 5:
                self.cast_ult()
                time.sleep(1.5)
                self.reposition(target_position)
                time.sleep(4)


# LegalizeIt = MageManager(config=configurations)
# LegalizeIt.teleport_right()
# LegalizeIt.farm_mode('KeyImages/MapNavigation/Top_Map_Position.png')
# LegalizeIt.teleport_left()
# LegalizeIt.farm_mode()