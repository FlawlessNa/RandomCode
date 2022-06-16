from ClientManager import ClientManager
import pyautogui
import pydirectinput
import time
import win32api
import win32con
from PostMessage import pyPostMessage


# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
# http://www.kbdedit.com/manual/low_level_vk_list.html

class LooterManager(ClientManager):

    def __init__(self, config, ign):
        super().__init__(config, ign)

    def use_stance(self):

        key_config = eval(self.config.get(section='KEYBINDS - Looter', option='stancekey'))
        pyPostMessage('press', key_config, self.hwnd)
        time.sleep(0.8)

    def chat_feed_is_displayed(self):
        if pyautogui.locateOnScreen(image='KeyImages/Feed_is_Displayed.png', region=self.client.box) is not None:
            return True
        else:
            return False

    def feed_mount(self):

        key_config = eval(self.config.get(section='KEYBINDS - Looter', option='mountfoodkey'))
        self.ensure_mount_is_used()

        pyPostMessage('press', key_config, self.hwnd)

    def toggle_mount(self):

        key_config = eval(self.config.get(section='KEYBINDS - Looter', option='mountkey'))
        pyPostMessage('press', key_config, self.hwnd)
        time.sleep(0.3)

    def ensure_mount_is_used(self):

        if pyautogui.locateOnScreen(image=self.config.get(section='Mount Image', option='mount_icon'), region=self.client.box, confidence=0.95) is None:
            self.toggle_mount()
            return True
        return False

    def find_self(self):
        image = self.config.get(section='Character Images', option='looter_guildlogo')
        return self.find_image(image)


    def move_to_and_enter_door(self):

        # This method should only be used after changing channel!
        while pyautogui.locateOnScreen(self.config.get(section='Map Images', option='ulu_minimap'), region=self.client.box) is None:
            self.toggle_minimap()

        loop = True
        self.move_right_by(666 - 322)
        while loop:
            self.move_to_target(target=self.config.get(section='Map Images', option='door'), acceptable_dist_range=[13, 37])
            self.jump()
            time.sleep(0.6)
            self.move_up()
            time.sleep(1)
            loop = self.check_portal_success(self.config.get(section='Map Images', option='CBD_minimap'))

    def move_to_and_enter_portal1(self):

        # This method should only be used after entering door!
        loop = True
        while loop:
            self.move_to_target(target=self.config.get(section='Map Images', option='CBD_portal1'), acceptable_dist_range=[18, 42])
            self.move_up()
            time.sleep(1)
            loop = self.check_portal_success(self.config.get(section='Map Images', option='CBD_fm'))

    def move_to_and_enter_fm(self):

        # This method should only be used after entering portal1
        loop = True
        while loop:
            self.move_to_target(target=self.config.get(section='Map Images', option='CBD_fm'), acceptable_dist_range=[10, 36])
            self.move_up()
            time.sleep(1)
            loop = self.check_portal_success(self.config.get(section='Map Images', option='FM_minimap'))

    def move_to_and_enter_portal2(self):

        # This method should only be used after leaving fm
        loop = True
        while loop:
            self.move_to_target(target=self.config.get(section='Map Images', option='CBD_portal2'), acceptable_dist_range=[16, 40])
            self.move_up()
            time.sleep(2)
            if self.chat_feed_is_displayed():
                self.toggle_chatfeed()
            loop = self.check_portal_success(self.config.get(section='Map Images', option='CBD_portal1'))

    def move_to_and_enter_door_from_town(self):

        if not self.ensure_mount_is_used():
            self.toggle_mount()
        self.jump_right()

        loop = True
        while loop:
            self.move_to_target(target=self.config.get(section='Map Images', option='door'), acceptable_dist_range=[13, 37])
            self.move_up()
            time.sleep(1)
            loop = self.check_portal_success(self.config.get(section='Map Images', option='ulu_minimap'))
        self.toggle_mount()

    def click_fm_storage(self):
        # Values are hard-coded since location is never-changing. Prevents issues using LocateOnScreen as there may be characters/animations hindering the npc
        self.click_at(60, 600)

    def click_fm_seller(self):
        self.click_at(575, 370)

    def check_portal_success(self, image):
        if pyautogui.locateOnScreen(image=image, region=self.client.box, confidence=0.9):
            return False
        else:
            return True





    def map_sequence_1(self):

        cond1 = """pyautogui.locateOnScreen(image=self.config.get(section='Character Images', option='looter_backhead'), region=self.client.box, confidence=0.9) != None"""
        self.jump_right_for(4)
        self.move_right_and_down_until(expression=cond1)

        pydirectinput.keyDown('up')
        time.sleep(0.5)
        pydirectinput.keyUp('up')
        # self.move_up_until(expression=cond2)

    def map_sequence_2(self):

        cond1 = """pyautogui.locateOnScreen(image=self.config.get(section='Map Images', option='target_sequence_2'), region=self.client.box, confidence=0.9) != None"""
        self.jump_left_until(expression=cond1)
        time.sleep(0.2)
        self.jump()
        time.sleep(1.5)

    def map_sequence_3(self):

        cond1 = """pyautogui.locateOnScreen(image=self.config.get(section='Character Images', option='looter_backhead'), region=self.client.box, confidence=0.9) != None"""
        self.jump_right_for(4)
        self.move_right_and_down_until(expression=cond1)
        self.move_down_for(0.4)
        self.jump_left()
        time.sleep(1)

    def map_sequence_4(self):

        cond1 = """pyautogui.locateOnScreen(image=self.config.get(section='Map Images', option='target_sequence_4'), region=self.client.box, confidence=0.9) != None"""
        self.jump_down()
        time.sleep(0.6)
        self.jump_down()
        time.sleep(1)
        self.move_left_until(expression=cond1)
