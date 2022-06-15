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

    def reposition(self):
        char_pos = self.find_image(image=self.config.get(section='Character Images', option='mage_medal'))
        too_far_left = self.find_image(image=self.config.get(section='Map Images', option='target_sequence_2'))
        too_far_right = self.find_image(image=self.config.get(section='Map Images', option='left_ladder'))
        if char_pos is None:
            return None
        else:
            if too_far_left is not None:
                distance = char_pos.x - too_far_left.x
                desired_distance = 650
                self.move_right_by(distance=desired_distance - distance)
            elif too_far_right is not None:
                distance = too_far_right.x - char_pos.x
                desired_distance = 1000
                self.move_left_by(distance=desired_distance - distance)

    def find_image(self, image):
        if pyautogui.locateCenterOnScreen(image=image, region=self.client.box, confidence=0.8) is not None:
            return pyautogui.locateCenterOnScreen(image=image, region=self.client.box, confidence=0.8)
        else:
            return None

    def move_to_car(self):
        loop = True
        all_images = eval(self.config.get(section='MOB Images', option='veetron'))
        all_images.extend(eval(self.config.get(section='MOB Images', option='berserkie')))
        while loop:
            self.cast_ult()
            time.sleep(2)
            if self.detect_mobs_multi_image(all_images) == 0:
                self.move_right_for(0.65)
                self.teleport_right()
                time.sleep(0.1)
                self.jump()
            loop = False

    def detect_mobs(self, mob_image):
        return len(list(pyautogui.locateAllOnScreen(image=mob_image, region=self.client.box, confidence=0.9)))

    def detect_mobs_multi_image(self, mob_images):
        nbr_mobs = 0
        for image in mob_images:
            nbr_mobs += len(list(pyautogui.locateAllOnScreen(image=image, region=self.client.box, confidence=0.9)))
        return nbr_mobs

    def farm_mode(self):
        while True:
            nbr_mobs = len(list(pyautogui.locateAllOnScreen(image='KeyImages/Veetron_left.png', region=self.client.box, confidence=0.9))) + \
                       len(list(pyautogui.locateAllOnScreen(image='KeyImages/Veetron_right.png', region=self.client.box, confidence=0.9))) + \
                       len(list(pyautogui.locateAllOnScreen(image='KeyImages/Berserkie_left.png', region=self.client.box, confidence=0.9))) + \
                       len(list(pyautogui.locateAllOnScreen(image='KeyImages/Berserkie_right.png', region=self.client.box, confidence=0.9)))
            if nbr_mobs >= 5:
                self.cast_ult()
                time.sleep(2)
                self.reposition()

# LegalizeIt = MageManager(config=configurations)
# LegalizeIt.teleport_right()
# LegalizeIt.farm_mode('KeyImages/MapNavigation/Top_Map_Position.png')
# LegalizeIt.teleport_left()
# LegalizeIt.farm_mode()