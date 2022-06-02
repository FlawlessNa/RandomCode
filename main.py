import numpy as np
import cv2
from PIL import ImageGrab
import win32gui
import pyautogui

while True:
    img = ImageGrab.grab(bbox=(0, 0, 1024, 768))  # x, y, w, h
    img_np = np.array(img)
    # frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    cv2.imshow("window", img_np)
    if cv2.waitKey(25) & 0Xff == ord('q'):
        break

cv2.destroyAllWindows()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
win32gui.FindWindow()