import cv2
import imutils
import numpy as np


class Course:
    def __init__(self, image, speed=1, height=100, display_width=200):
        self.course_image = imutils.resize(image, height=height)
        self.path = self._find_path()

        self.course_progress = 0
        self.speed = speed

        self.x = 0
        self.y = 0
        self.height = height
        self.width = display_width

    def _find_path(self):
        gray_course = cv2.cvtColor(self.course_image, cv2.COLOR_BGR2GRAY)
        split = np.median(gray_course)
        _, threshed_course = cv2.threshold(gray_course, split, 255, cv2.THRESH_BINARY)
        return threshed_course

    def _update(self):
        if self.course_progress + self.width < self.course_image.shape[1]:
            self.course_progress += self.speed

    def _get_coords(self, image_shape):
        self.x = image_shape[1] - self.width

    def draw(self, image, alpha=0.8, update=True):
        image_overlay = image.copy()
        cropped_course = self.course_image[:, self.course_progress:self.course_progress + self.width]

        self._get_coords(image.shape[:2])

        image_overlay[:self.height, self.x:] = cropped_course

        cv2.addWeighted(image_overlay, alpha, image, 1 - alpha, 0, image)

        if update:
            self._update()

        return image

    def is_on_path(self, xy):
        on_path = False
        adjusted_x = xy[0] - self.x

        if (0 <= adjusted_x <= self.course_image.shape[1] and
                0 <= xy[1] <= self.course_image.shape[0]):
            on_path = self.path[xy[1], adjusted_x] == 255

        return on_path
