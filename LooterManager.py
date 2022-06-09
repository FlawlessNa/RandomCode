from ClientManager import ClientManager
import pyautogui
import pydirectinput
import time
import win32api
import win32con


# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
configurations={'EmptyCellValue': 236,
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


class LooterManager(ClientManager):

    def __init__(self, config):
        super().__init__(config)

    def use_stance(self):
        # self.client.activate()
        # pydirectinput.press('end')

        lparam_keydown = self.construct_lparams(repeat_count=1, key=self.config['StanceKey'], wm_command=win32con.WM_KEYDOWN, extended_key=self.config['StanceKeyExt'], previous_key_state=0)
        lparam_keyup = self.construct_lparams(repeat_count=1, key=self.config['StanceKeyExt'], wm_command=win32con.WM_KEYUP, extended_key=1)

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, self.config['StanceKey'], lparam_keydown)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, self.config['StanceKey'], lparam_keyup)

        time.sleep(0.6)

    def chat_feed_is_displayed(self):
        if pyautogui.locateOnScreen(image='KeyImages/Feed_is_Displayed.png', region=self.client.box) is not None:
            return True
        elif pyautogui.locateOnScreen(image='KeyImages/Feed_is_not_Displayed.png', region=self.client.box) is not None:
            return False
        else:
            return None

    def feed_multiple_pets(self, nbr_press):
        for i in range(nbr_press):
            self.feed_pets()

    def feed_mount(self):

        self.ensure_mount_is_used()
        lparam_keydown = self.construct_lparams(repeat_count=1, key=self.config['MountFoodKey'], wm_command=win32con.WM_KEYDOWN, extended_key=self.config['MountFoodKeyExt'], previous_key_state=0)
        lparam_keyup = self.construct_lparams(repeat_count=1, key=self.config['MountFoodKey'], wm_command=win32con.WM_KEYUP, extended_key=self.config['MountFoodKeyExt'])

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, self.config['MountFoodKey'], lparam_keydown)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, self.config['MountFoodKey'], lparam_keyup)

    def toggle_mount(self):

        lparam_keydown = self.construct_lparams(repeat_count=1, key=self.config['MountKey'], wm_command=win32con.WM_KEYDOWN, extended_key=self.config['MountKeyExt'], previous_key_state=0)
        lparam_keyup = self.construct_lparams(repeat_count=1, key=self.config['MountKey'], wm_command=win32con.WM_KEYUP, extended_key=self.config['MountKeyExt'])

        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, self.config['MountKey'], lparam_keydown)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, self.config['MountKey'], lparam_keyup)

    def ensure_mount_is_used(self):

        if pyautogui.locateOnScreen(image=self.config['MountImg'], region=self.client.box, confidence=0.9) is None:
            self.toggle_mount()

    def map_sequence_1(self):

        cond1 = """pyautogui.locateOnScreen(image='KeyImages/MapNavigation/BackHead.png',
                                        region=self.client.box,
                                        confidence=0.9) != None"""

        self.jump_right_for(5)
        self.move_right_and_down_until(expression=cond1)

        pydirectinput.keyDown('up')
        time.sleep(0.3)
        pydirectinput.keyUp('up')
        # self.move_up_until(expression=cond2)

    def map_sequence_2(self):

        cond1 = """pyautogui.locateOnScreen(image='KeyImages/MapNavigation/Target_Sequence2_Pole.png',
                                        region=self.client.box,
                                        confidence=0.9) != None"""
        self.jump_left_until(expression=cond1)
        time.sleep(0.2)
        self.jump()
        time.sleep(1.5)

    def map_sequence_3(self):

        cond1 = """pyautogui.locateOnScreen(image='KeyImages/MapNavigation/BackHead.png',
                                        region=self.client.box,
                                        confidence=0.9) != None"""
        self.jump_right_for(5)
        self.move_right_and_down_until(expression=cond1)
        self.move_down_for(0.4)
        self.jump_left()
        time.sleep(1)

    def map_sequence_4(self):

        cond1 = """pyautogui.locateOnScreen(image='KeyImages/MapNavigation/Target_Sequence4_Portal.png',
                                        region=self.client.box,
                                        confidence=0.9) != None"""
        # self.jump_down_until(expression=cond1)
        self.jump_down()
        time.sleep(0.6)
        self.jump_down()
        time.sleep(1)
        self.move_left_until(expression=cond1)


Guarding = LooterManager(config=configurations)
Guarding.jump()
Guarding.map_sequence_1()
Guarding.map_sequence_2()
Guarding.map_sequence_3()
Guarding.map_sequence_4()
print('ok')
