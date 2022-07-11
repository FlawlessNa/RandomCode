import win32con
import pyautogui
import pydirectinput
from PostMessage import pyPostMessage
from BasicMovements import BasicMovements


class BasicCommands(BasicMovements):

    def __init__(self, config, ign):
        super().__init__(config, ign)

    def toggle_character_stats(self):

        key_config = eval(self.config.get(section='KEYBINDS - Common', option='characterstatskey'))
        pyPostMessage('press', key_config, self.hwnd)

    def toggle_inventory(self):

        key_config = eval(self.config.get(section='KEYBINDS - Common', option='inventorykey'))
        pyPostMessage('press', key_config, self.hwnd)

    def toggle_chatfeed(self):

        key_config = eval(self.config.get(section='KEYBINDS - Common', option='togglechatfeedkey'))
        pyPostMessage('press', key_config, self.hwnd)

    def toggle_minimap(self):

        key_config = eval(self.config.get(section='KEYBINDS - Common', option='minimapkey'))
        pyPostMessage('press', key_config, self.hwnd)

    def click(self):
        self.client.activate()
        pydirectinput.click()

    def feed_pet(self):

        key_config = eval(self.config.get(section='KEYBINDS - Common', option='petfoodkey'))
        pyPostMessage('press', key_config, self.hwnd)

    def feed_multiple_pets(self, nbr_press):
        for i in range(nbr_press):
            self.feed_pet()

    def click_at(self, x, y):
        self.client.activate()
        pydirectinput.click(x, y)

    def move_cursor_to(self, x, y):
        pass

    def check_pots_left(self):
        pass

    def allchat(self):

        key_config = eval(self.config.get(section='KEYBINDS - Common', option='allchatkey'))
        pyPostMessage('press', key_config, self.hwnd)

    def type_message(self, message):

        # This assume all characters are "standard" (from A-Z, 0-9)
        for char in message:
            pyPostMessage('write', [ord(char), 0], self.hwnd)

        pyPostMessage('press', [win32con.VK_RETURN, 0], self.hwnd)
        pyPostMessage('press', [win32con.VK_ESCAPE, 0], self.hwnd)

    def mapowner(self):

        self.allchat()
        self.type_message('~mapowner')

    def turn_pet_on(self):
        pass

    def setup_hp_pots(self):
        pass

    def setup_mp_pots(self):
        pass

    def find_self(self):
        pass
