from LooterManager import LooterManager
from MageManager import MageManager
import multiprocessing


class MultiClients:

    INITIALIZATION = 0
    MAP_SEQUENCE_1 = 1
    MAP_SEQUENCE_2 = 2
    MAP_SEQUENCE_3 = 3
    MAP_SEQUENCE_4 = 4

    def __init__(self, config):
        self.config = config
        self.clients = []
        processes = [multiprocessing.Process(target=self.initialization, args=(ign, char_type, )) for ign, char_type in eval(self.config.get(section='IGN', option='ign_dict')).items()]
        for p in processes:
            p.start()
        for p in processes:
            p.join()

    def initialization(self, ign, char_type):
        if char_type == 'looter':
            c = LooterManager(self.config, ign)
            self.clients.append(c)
        elif char_type == 'mage':
            c = MageManager(self.config, ign)
            self.clients.append(c)

    def setup(self):
        processes = [multiprocessing.Process(target=client.farm_setup()) for client in self.clients]
        for p in processes:
            p.start()
        for p in processes:
            p.join()

        self.party_setup()

    def party_setup(self):
        pass

