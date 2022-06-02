import cv2
import numpy as np
from matplotlib import pyplot as plt


# img_rgb = cv2.imread('KeyImages/FullImageTest.png')
# img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
# template = cv2.imread('KeyImages/EmptyInventoryCell.png', 0)
#
# template2 = template[2:32, 2:32]
#
# w, h = template2.shape[::-1]
# res = cv2.matchTemplate(img_gray, template2, cv2.TM_CCOEFF_NORMED)
# threshold = .99
# loc = np.where( res >= threshold)
# for pt in zip(*loc[::-1]):
#     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
# cv2.imshow('resempty', img_rgb)
# cv2.waitKey(0)


# For now, we are assuming the large (1024x768) client is always used for inventory management.
# This class will take in images from client regularly to assess the status of inventory
# Goal is that it will be capable of determining which items are to be kept and which are to sell
# It should also know when it is time to go npc (aka when inventory is full)
class InventoryManager:
    def __init__(self, config):
        # TODO Create an actual config file
        # TODO Create methods to re-size those config for small client
        self.GRAYSCALE = config['EmptyCellValue']  # Grayscale color is 236 (except first line/col which is 206
        self.THRESHOLD = config['EmptyCellThreshold']  # 0.99
        self.template = self.create_template(cv2.imread(config['EmptyCellPath'], cv2.IMREAD_GRAYSCALE))
        self.template_width, self.template_height = self.template.shape[::-1]

    def create_template(self, template_screenshot):
        # simply removing the first 2 rows, 2 columns, as well as last 3 rows, 3 columns from the screenshot I took
        return template_screenshot[2:template_screenshot.shape[0] - 3, 2:template_screenshot.shape[1] - 3]

    def get_number_of_empty_inventory_space(self, image_grayscale):
        # TODO test out other cv2 built-in methods of resolving match, maybe one fits better our needs

        match_result = cv2.matchTemplate(image_grayscale, self.template, cv2.TM_CCOEFF_NORMED)
        good_fits = np.where(match_result >= self.THRESHOLD)
        return len(good_fits[0])

    # Just a temporary method used for testing purposes
    def print_red_squares_on_image(self, image):
        image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        match_result = cv2.matchTemplate(image_grayscale, self.template, cv2.TM_CCOEFF_NORMED)
        good_fits = np.where(match_result >= self.THRESHOLD)

        for pt in zip(*good_fits[::-1]):
            cv2.rectangle(image, pt, (pt[0] + self.template_width, pt[1] + self.template_height), (0, 0, 255), 2)

        cv2.imshow('result', image)
        cv2.waitKey(0)  # Press any key on the window that pops-up to allow code to continue executing


test = InventoryManager(config={'EmptyCellValue': 236, 'EmptyCellThreshold': 0.99,
                                'EmptyCellPath': 'KeyImages/EmptyInventoryCell.png'})

current_image = cv2.imread('KeyImages/FullImageTest.png')
current_im_gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
empty_spots = test.get_number_of_empty_inventory_space(current_im_gray)
print('Number of space remaining in inventory: {}'.format(empty_spots))
test.print_red_squares_on_image(current_image)

# TODO Take a bunch of screenshots along with the real number of available space, and run on each to see if output
# TODO is always consistent
