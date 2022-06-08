from ClientManager import ClientManager
import pyautogui
import pydirectinput
import time

configurations={'EmptyCellValue': 236,
                'EmptyCellThreshold': 0.99,
                'YellowDotPath': 'KeyImages/MapNavigation/YellowDot.png',
                'MapToggled': 'KeyImages/MapNavigation/MapProperlyToggled.png',
                'MapRect': 5,
                'IGN': 'Guarding',
                'Sequence_1_Target': 'KeyImages/MapNavigation/Target_Sequence1.png'}

class LooterManager(ClientManager):

    def __init__(self, config):
        super().__init__(config['IGN'])

    def use_stance(self):
        self.client.activate()
        pydirectinput.press('end')

    def feed_is_displayed(self):
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
        pydirectinput.press('8')

    def ensure_mount_is_used(self):
        self.client.activate()
        if self.feed_is_displayed() == True:
            pydirectinput.press("'")  # To minimize feed
        pydirectinput.press('end')  # Any skill that cannot be used while mounted is fine
        if pyautogui.locateOnScreen(image='KeyImages/TamedMonster.png', region=self.client.box) is None:
            time.sleep(0.6)
            pydirectinput.press('x') # Key to mount/unmount

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
        self.move_left_until(expression=cond1)


Guarding = LooterManager(config=configurations)
Guarding.ensure_mount_is_used()
Guarding.map_sequence_1()
Guarding.map_sequence_2()
Guarding.map_sequence_3()
Guarding.map_sequence_4()
print('ok')
