import os

class ClientManager():
    def __init__(self):
        pass

    def open(self, resolution):
        name = resolution if resolution == '800x600' else ''
        client_path = os.path.join(os.getcwd(), '..', 'MapleRoyals' + name)
        open(client_path + 'MapleRoyals')

    def move(self, direction):
        pass

