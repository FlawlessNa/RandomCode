import win32con
import pyautogui
from BasicCommands import BasicCommands
from PostMessage import pyPostMessage
from ImageDetection import find_image
import cv2
import time

class ComplexClient(BasicCommands):

    def __init__(self, config, ign):
        super().__init__(config, ign)

    def change_channel(self, destination):

        nbr_keys = self.get_current_channel() - destination

        while True:
            pyPostMessage('press', [win32con.VK_ESCAPE, 0], self.hwnd)
            pyPostMessage('press', [win32con.VK_RETURN, 0], self.hwnd)

            if nbr_keys < 0:
                for i in range(abs(nbr_keys)):
                    pyPostMessage('press', [win32con.VK_RIGHT, 1], self.hwnd)

            elif nbr_keys > 0:
                for i in range(nbr_keys):
                    pyPostMessage('press', [win32con.VK_LEFT, 1], self.hwnd)

            pyPostMessage('press', [win32con.VK_RETURN, 0], self.hwnd)

            time.sleep(1.25)
            if len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='change_channel_check'), cv2.IMREAD_COLOR))):
                pyPostMessage('press', [win32con.VK_RETURN, 0], self.hwnd)
            else:
                time.sleep(0.5)
                if len(find_image(self.take_screenshot(), cv2.imread(self.config.get(section='Map Images', option='target_sequence_4'), cv2.IMREAD_COLOR))):
                    break

        self.set_current_channel(destination)

    def leave_party(self):
        # This is to reset the entire party to make sure it is properly set
        self.allchat()
        self.type_message('/leaveparty')

    def remake_party(self):
        invite_list = list(eval(self.config.get(section='IGN', option='ign_dict')).keys())
        invite_list.remove(self.ign)
        invite_list.insert(0, '/partyinvite')

        self.allchat()
        self.type_message(' '.join(invite_list))

    def accept_party_invite(self):
        # TODO Refactor into absolute x, y position (relative to client position) since prompt will always spawn at exact same spot.
        # TODO Use pyPostMessage and mouseclick event to do so instead of pyautogui
        x, y = pyautogui.locateCenterOnScreen(image=self.config.get(section='Misc Images', option='party_invite_prompt'), region=self.client.box, confidence=0.95)
        pyautogui.doubleClick(x, y)

    def check_current_location(self):
        # TODO Use the buddy list (the character's location is written in there) to assess in which map the character is currently located
        pass

    def setup_hp_threshold(self):

        nbr_ticks_right = eval(self.config.get(section='HP Threshold', option='threshold_dict'))[self.ign]

        pyPostMessage('press', [win32con.VK_ESCAPE, 0], self.hwnd)
        for i in range(2):
            pyPostMessage('press', [win32con.VK_UP, 1], self.hwnd)

        pyPostMessage('press', [win32con.VK_RETURN, 0], self.hwnd)

        # Tab all the way down until reaching the HP threshold selection
        for i in range(7):
            pyPostMessage('press', [win32con.VK_TAB, 0], self.hwnd)

        # Turn the threshold all the way down to the bare minimum
        for i in range(20):
            pyPostMessage('press', [win32con.VK_LEFT, 1], self.hwnd)

        # Reset the threshold to the desired value
        for i in range(nbr_ticks_right):
            pyPostMessage('press', [win32con.VK_RIGHT, 1], self.hwnd)

        pyPostMessage('press', [win32con.VK_RETURN, 0], self.hwnd)

    def setup_mp_threshold(self):
        nbr_ticks_right = eval(self.config.get(section='MP Threshold', option='threshold_dict'))[self.ign]

        pyPostMessage('press', [win32con.VK_ESCAPE, 0], self.hwnd)
        for i in range(2):
            pyPostMessage('press', [win32con.VK_UP, 1], self.hwnd)

        pyPostMessage('press', [win32con.VK_RETURN, 0], self.hwnd)

        # Tab all the way down until reaching the MP threshold selection
        for i in range(8):
            pyPostMessage('press', [win32con.VK_TAB, 0], self.hwnd)

        # Turn the threshold all the way down to the bare minimum
        for i in range(20):
            pyPostMessage('press', [win32con.VK_LEFT, 1], self.hwnd)

        # Reset the threshold to the desired value
        for i in range(nbr_ticks_right):
            pyPostMessage('press', [win32con.VK_RIGHT, 1], self.hwnd)

        pyPostMessage('press', [win32con.VK_RETURN, 0], self.hwnd)

    def move_to_target(self, target, acceptable_dist_range, threshold=0.7):

        min_dist, max_dist = acceptable_dist_range
        loop = True
        increment = 1
        counter = 0
        while loop:
            current_pos = self.find_self()
            target_pos = find_image(self.take_screenshot(), cv2.imread(target, cv2.IMREAD_COLOR), threshold=threshold)
            if len(target_pos) and len(current_pos):
                current_pos_x = current_pos[0][0]
                target_pos_x = target_pos[0][0]
            else:
                counter += 1
                if counter > 15:
                    break
                continue  # This would happen if there are animations (such as an ult) blocking the target

            distance = target_pos_x - current_pos_x
            print('Horizontal distance is {}'.format(distance))
            if min_dist < distance < max_dist:
                return True
            elif distance > 0:
                self.move_right_by(distance / increment)
                increment += 0.75
            else:
                self.move_left_by(abs(distance / increment))
                increment += 0.75

    def detect_mobs(self, haystack, mob_image):
        return len(find_image(haystack, cv2.imread(mob_image, cv2.IMREAD_COLOR)))

    def detect_mobs_multi_image(self, haystack, mob_images):
        nbr_mobs = 0
        for image in mob_images:
            nbr_mobs += self.detect_mobs(haystack, image)
        return nbr_mobs

    def potion_setup(self):
        hp_pots_to_use = eval(self.config.get(section='HP Potions', option='potion_dict'))[self.ign]
        mp_pots_to_use = eval(self.config.get(section='MP Potions', option='potion_dict'))[self.ign]
        hp_needle = cv2.imread(eval(self.config.get(section='Inventory Images', option='potions'))[hp_pots_to_use], cv2.IMREAD_COLOR)
        mp_needle = cv2.imread(eval(self.config.get(section='Inventory Images', option='potions'))[mp_pots_to_use], cv2.IMREAD_COLOR)

        self.ensure_pet_is_on()
        self.ensure_equip_window_is_open()
        if not len(find_image(self.take_screenshot(), hp_needle, threshold=0.9)):
            self.setup_hp_pots(hp_needle)
        if not len(find_image(self.take_screenshot(), mp_needle, threshold=0.9)):
            self.setup_mp_pots(mp_needle)
        self.toggle_equip_window()


    def farm_setup(self):
        self.potion_setup()
        # self.feed_multiple_pets(len(eval(self.config.get(section='Pet Images', option='pets'))[self.ign]) * 3)

