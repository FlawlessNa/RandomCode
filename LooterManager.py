from ClientManager import ClientManager
import pyautogui
import pydirectinput

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

    def assess_map_location(self):
        pass


Guarding = LooterManager(config=configurations)
print('ok')
