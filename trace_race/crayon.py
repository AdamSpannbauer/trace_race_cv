import random
import pkg_resources
import cv2
import imutils
import numpy as np

VALID_COLORS = ['blue', 'green', 'pink', 'red', 'yellow']

CRAYON_BGR_COLOR_DICT = {
    'blue': (255, 0, 0),
    'green': (0, 255, 0),
    'pink': (240, 70, 220),
    'red': (0, 0, 255),
    'yellow': (60, 200, 250)
}


class Crayon:
    """Place crayon tip on specific x, y coordinate

    For use in trace race.  Crayon tip will follow centroid of object being tracked.
    Assumed that bottom right corner of crayon image is tip of crayon.

    :param color: valid colors are ['blue', 'green', 'pink', 'red', 'yellow']
    :param max_height: Resize crayon image to this height; no resizing down if image height less than max_height

    >>> crayon = Crayon('red')
    >>> image = cv2.imread('my_image.png')
    >>> crayon.draw(image, (100, 100))
    """
    def __init__(self, color, max_height=100):
        if color not in VALID_COLORS:
            print('No valid crayon color provided; choosing at random')
            color = random.choice(VALID_COLORS)

        self.crayon_image = self._read_crayon_image(color, max_height)
        self.gray_crayon_image = self._read_crayon_image('gray', max_height)

        self.color = color
        self.color_bgr = CRAYON_BGR_COLOR_DICT[color]

        self.crayon_h, self.crayon_w = self.crayon_image.shape[:2]

    @staticmethod
    def _read_crayon_image(color, max_height):
        path = pkg_resources.resource_filename('trace_race', f'data/crayons/{color}.png')
        crayon_image = cv2.imread(path, cv2.IMREAD_UNCHANGED)

        if crayon_image.shape[0] > max_height:
            crayon_image = imutils.resize(crayon_image, height=max_height)

        return crayon_image

    def draw(self, frame, tracking_centroid, use_color=True):
        if use_color:
            crayon_image = self.crayon_image
        else:
            crayon_image = self.gray_crayon_image

        x, y = tracking_centroid

        # shift since tip of crayon assets not perfectly in bottom corner
        x += 3
        y += 3

        # crop overhanging portions of crayon image
        overhang_x = x - self.crayon_w
        overhang_y = y - self.crayon_h

        crop_x = -1 * min(overhang_x, 0)
        crop_y = -1 * min(overhang_y, 0)

        cropped_crayon = crayon_image[crop_y:, crop_x:]

        # find non transparent coords of crayon image
        non_negative_space = np.where(cropped_crayon[:, :, 3] > 0)

        # overlay crayon image on frame
        min_x = x - cropped_crayon.shape[1]
        min_y = y - cropped_crayon.shape[0]

        frame[min_y:y, min_x:x][non_negative_space] = cropped_crayon[:, :, :3][non_negative_space]
