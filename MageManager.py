from ClientManager import ClientManager
import pydirectinput

class MageManager(ClientManager):
    def __init__(self):
        super().__init__()

    def cast_ult(self):
        self.client.activate()
        pydirectinput.press('ctrlright')

    def check_pots_left(self):
        pass

    def rebuff(self):
        pass


