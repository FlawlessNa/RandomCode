import cv2
import numpy as np
# Can use filters to reduce the number of images to look for when farming. Can potentially reduce it from 4 images to 2 images (maybe even 1?)
# To use if you ever run into performance issues

def init_control_gui():

    cv2.namedWindow('Trackbars', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Trackbars', 350, 700)

    # required callback. we'll be using getTrackbarPos() to do lookups
    # instead of using the callback.
    def nothing(position):
        pass

    # create trackbars for bracketing.
    # OpenCV scale for HSV is H: 0-179, S: 0-255, V: 0-255
    cv2.createTrackbar('HMin', 'Trackbars', 0, 179, nothing)
    cv2.createTrackbar('SMin', 'Trackbars', 0, 255, nothing)
    cv2.createTrackbar('VMin', 'Trackbars', 0, 255, nothing)
    cv2.createTrackbar('HMax', 'Trackbars', 0, 179, nothing)
    cv2.createTrackbar('SMax', 'Trackbars', 0, 255, nothing)
    cv2.createTrackbar('VMax', 'Trackbars', 0, 255, nothing)
    # Set default value for Max HSV trackbars
    cv2.setTrackbarPos('HMax', 'Trackbars', 179)
    cv2.setTrackbarPos('SMax', 'Trackbars', 255)
    cv2.setTrackbarPos('VMax', 'Trackbars', 255)

    # trackbars for increasing/decreasing saturation and value
    cv2.createTrackbar('SAdd', 'Trackbars', 0, 255, nothing)
    cv2.createTrackbar('SSub', 'Trackbars', 0, 255, nothing)
    cv2.createTrackbar('VAdd', 'Trackbars', 0, 255, nothing)
    cv2.createTrackbar('VSub', 'Trackbars', 0, 255, nothing)

def get_hsv_filter_from_controls():
    # Get current positions of all trackbars
    hsv_filter = HsvFilter()
    hsv_filter.hMin = cv2.getTrackbarPos('HMin', 'Trackbars')
    hsv_filter.sMin = cv2.getTrackbarPos('SMin', 'Trackbars')
    hsv_filter.vMin = cv2.getTrackbarPos('VMin', 'Trackbars')
    hsv_filter.hMax = cv2.getTrackbarPos('HMax', 'Trackbars')
    hsv_filter.sMax = cv2.getTrackbarPos('SMax', 'Trackbars')
    hsv_filter.vMax = cv2.getTrackbarPos('VMax', 'Trackbars')
    hsv_filter.sAdd = cv2.getTrackbarPos('SAdd', 'Trackbars')
    hsv_filter.sSub = cv2.getTrackbarPos('SSub', 'Trackbars')
    hsv_filter.vAdd = cv2.getTrackbarPos('VAdd', 'Trackbars')
    hsv_filter.vSub = cv2.getTrackbarPos('VSub', 'Trackbars')
    return hsv_filter

    # given an image and an HSV filter, apply the filter and return the resulting image.
    # if a filter is not supplied, the control GUI trackbars will be used


def apply_hsv_filter(original_image, hsv_filter=None):
    # convert image to HSV
    hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

    # if we haven't been given a defined filter, use the filter values from the GUI
    if not hsv_filter:
        hsv_filter = get_hsv_filter_from_controls()

    # add/subtract saturation and value
    h, s, v = cv2.split(hsv)
    s = shift_channel(s, hsv_filter.sAdd)
    s = shift_channel(s, -hsv_filter.sSub)
    v = shift_channel(v, hsv_filter.vAdd)
    v = shift_channel(v, -hsv_filter.vSub)
    hsv = cv2.merge([h, s, v])

    # Set minimum and maximum HSV values to display
    lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
    upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])
    # Apply the thresholds
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(hsv, hsv, mask=mask)

    # convert back to BGR for imshow() to display it properly
    img = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

    return img

 # apply adjustments to an HSV channel
# https://stackoverflow.com/questions/49697363/shifting-hsv-pixel-values-in-python-using-numpy
def shift_channel(c, amount):
    if amount > 0:
        lim = 255 - amount
        c[c >= lim] = 255
        c[c < lim] += amount
    elif amount < 0:
        amount = -amount
        lim = amount
        c[c <= lim] = 0
        c[c > lim] -= amount
    return c

# custom data structure to hold the state of an HSV filter
class HsvFilter:

    def __init__(self, hMin=None, sMin=None, vMin=None, hMax=None, sMax=None, vMax=None, sAdd=None, sSub=None, vAdd=None, vSub=None):
        self.hMin = hMin
        self.sMin = sMin
        self.vMin = vMin
        self.hMax = hMax
        self.sMax = sMax
        self.vMax = vMax
        self.sAdd = sAdd
        self.sSub = sSub
        self.vAdd = vAdd
        self.vSub = vSub