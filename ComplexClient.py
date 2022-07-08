import win32con
import pyautogui
from BasicCommands import BasicCommands
from PostMessage import pyPostMessage


class ComplexClient(BasicCommands):

    def __init__(self, config, ign):
        super().__init__(config, ign)

    def change_channel(self, destination):

        nbr_keys = self.get_current_channel() - destination

        pyPostMessage('press', [win32con.VK_ESCAPE, 0], self.hwnd)
        pyPostMessage('press', [win32con.VK_RETURN, 0], self.hwnd)

        if nbr_keys < 0:
            for i in range(abs(nbr_keys)):
                pyPostMessage('press', [win32con.VK_RIGHT, 1], self.hwnd)

        elif nbr_keys > 0:
            for i in range(nbr_keys):
                pyPostMessage('press', [win32con.VK_LEFT, 1], self.hwnd)

        pyPostMessage('press', [win32con.VK_RETURN, 0], self.hwnd)

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

    def find_image(self, image):
        if pyautogui.locateCenterOnScreen(image=image, region=self.client.box, confidence=0.8) is not None:
            return pyautogui.locateCenterOnScreen(image=image, region=self.client.box, confidence=0.8)
        else:
            return None

    def move_to_target(self, target, acceptable_dist_range):

        # The target must be visible within the client
        if pyautogui.locateOnScreen(image=target, region=self.client.box, confidence=0.9) is None:
            return False

        min_dist, max_dist = acceptable_dist_range
        loop = True
        increment = 1
        while loop:
            current_pos = self.find_self()
            target_pos = self.find_image(target)
            if current_pos is None or target_pos is None:
                continue  # This would happen if there are animations (such as an ult) blocking the target
            else:
                distance = target_pos.x - current_pos.x
                print('Horizontal distance is {}'.format(distance))
                if min_dist < distance < max_dist:
                    return True
                elif distance > 0:
                    self.move_right_by(distance / increment)
                    increment += 0.75
                else:
                    self.move_left_by(abs(distance / increment))
                    increment += 0.75