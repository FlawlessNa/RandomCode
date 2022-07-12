from LooterManager import LooterManager
from MageManager import MageManager


class MultiClients:

    INITIALIZATION = 0
    MAP_SEQUENCE_1 = 1
    MAP_SEQUENCE_2 = 2
    MAP_SEQUENCE_3 = 3
    MAP_SEQUENCE_4 = 4

    def __init__(self, config):
        self.config = config
        self.clients = []
        for ign, char_type in eval(self.config.get(section='IGN', option='ign_dict')).items():
            if char_type == 'looter':
                self.clients.append(LooterManager(self.config, ign))
            elif char_type == 'mage':
                self.clients.append(MageManager(self.config, ign))

    def farm_setup(self):
        for client in self.clients:
            client.farm_setup()

