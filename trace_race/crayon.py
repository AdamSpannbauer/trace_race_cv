import cv2
import imutils
import numpy as np


class Crayon:
    """Place crayon tip on specific x, y coordinate

    For use in trace race.  Crayon tip will follow centroid of object being tracked.
    Assumed that bottom right corner of crayon image is tip of crayon.

    :param crayon_image_path: Path to crayon image to use
    :param max_height: Resize crayon image to this height; no resizing down if image height less than max_height

    >>> crayon = Crayon('crayons/red.png')
    >>> image = cv2.imread('my_image.png')
    >>> crayon.draw(image, (100, 100))
    """
    def __init__(self, crayon_image_path, max_height=100):
        self.crayon_image = self._read_crayon_image(crayon_image_path, max_height)
        self.gray_crayon_image = self._read_crayon_image('crayons/gray.png', max_height)

        self.crayon_h, self.crayon_w = self.crayon_image.shape[:2]

    @staticmethod
    def _read_crayon_image(path, max_height):
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
