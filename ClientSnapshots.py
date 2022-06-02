import cv2
import win32gui
import pyautogui
from PIL import ImageGrab

# PIL module allows to take screenshots anywhere in any screen and manipulate those at will
# TODO: Figure a way to take screenshots of a given client (ideally, the client's position on-screen doesn't matter)
# TODO: The first and easier step might be to always have the clients at the very same spot on screen, can then work to
# TODO: make things more flexible if needed
while True:
    img = ImageGrab.grab(bbox=(0, 0, 1024, 768))  # x, y, w, h
    img_np = np.array(img)
    # frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    cv2.imshow("window", img_np)
    if cv2.waitKey(25) & 0Xff == ord('q'):
        break

cv2.destroyAllWindows()