import cv2
import win32gui
import win32ui
import win32con
import numpy as np

def take_screenshot(client, dim=None):

    if dim is None:
        width = client.width
        height = client.height
        crop_x = 0
        crop_y = 0
    else:
        width = dim['width']
        height = dim['height']
        crop_x = dim['crop_x']
        crop_y = dim['crop_y']

    # Function that takes a screenshot of a client object, even if that client is not visible on screen (hidden by another window or minimized)

    wDC = win32gui.GetWindowDC(client._hWnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (width, height), dcObj, (crop_x, crop_y), win32con.SRCCOPY)
    signedIntsArray = dataBitMap.GetBitmapBits(True)

    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)

    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(client._hWnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    img = img[:, :, :3]
    img = np.ascontiguousarray(img)

    return img


def find_image(haystack, needle, method=cv2.TM_CCOEFF_NORMED, threshold=0.7):

    result = cv2.matchTemplate(haystack, needle, method)
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), needle.shape[1], needle.shape[0]]

        # Add every box twice in order to retain single (non-overlapping) boxes
        rectangles.append(rect)
        rectangles.append(rect)

        # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is done. If you put it at 2 then an object needs at least 3 overlapping rectangles
        # to appear in the result. I've set eps to 0.5, which is:
        # "Relative difference between sides of the rectangles to merge them into a group."

    rectangles, weights = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

    return rectangles


def midpoint(handle, rectangle):
    try:
        x, y, w, h = list(*rectangle)
    except TypeError:
        x, y, w, h = rectangle

    return win32gui.ClientToScreen(handle, (int(x + w/2), int(y + h/2)))
