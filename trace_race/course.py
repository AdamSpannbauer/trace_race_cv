import pkg_resources
import cv2
import imutils
import numpy as np
from . import utils


class Course:
    def __init__(self, course_number, speed=1, height=100, display_width=200, data_path=None):
        if course_number is None:
            course_number = 0

        if data_path is not None:
            image_path = f'{data_path}/courses/course{course_number}.png'
        else:
            image_path = pkg_resources.resource_filename('trace_race', f'data/courses/course{course_number}.png')

        self.course_image = imutils.resize(utils.imread_anywhere(image_path), height=height)
        self.path = self._find_path()
        self.n_path_points = self._calc_path_points()

        self.course_progress = 0
        self.speed = speed

        self.x = 0
        self.height = height
        self.width = display_width

        self.on_path_checks = []
        self.prev_draw_point = None

    def _find_path(self):
        gray_course = cv2.cvtColor(self.course_image, cv2.COLOR_BGR2GRAY)
        split = np.median(gray_course)
        _, threshed_course = cv2.threshold(gray_course, split, 255, cv2.THRESH_BINARY)
        return threshed_course

    def _calc_path_points(self):
        kernel = np.ones((5, 5), np.uint8)
        eroded_path = cv2.erode(self.path, kernel, iterations=1)

        return sum(eroded_path.flatten() == 255)

    def _update(self):
        if self.course_progress + self.width < self.course_image.shape[1]:
            self.course_progress += self.speed

    def _get_coords(self, image_shape):
        self.x = image_shape[1] - self.width

    def display_below(self, image):
        display_course = imutils.resize(self.course_image, width=image.shape[1])
        return np.vstack((image, display_course[:, :, :3]))

    def draw(self, image, alpha=0.8, update=True):
        image_overlay = image.copy()
        cropped_course = self.course_image[:, self.course_progress:self.course_progress + self.width]

        self._get_coords(image.shape[:2])

        image_overlay[:self.height, self.x:] = cropped_course[:, :, :3]

        cv2.addWeighted(image_overlay, alpha, image, 1 - alpha, 0, image)

        if update:
            self._update()

        return image

    def draw_on_course(self, image, point, color, is_finished):
        if self.is_on_course(image, point) and not is_finished:
            x, y = point
            x = x - self.x + self.course_progress

            self.on_path_checks.append(self.is_on_path((x, y)))
            is_finished = self.is_finished((x, y))

            if self.prev_draw_point is None:
                self.prev_draw_point = (x, y)
                cv2.circle(self.course_image, (x, y), radius=3, color=color, thickness=-1)
            else:
                cv2.line(self.course_image, self.prev_draw_point, (x, y), color=color, thickness=3)
                self.prev_draw_point = (x, y)
        else:
            self.prev_draw_point = None

        return is_finished

    def is_finished(self, point, tolerance=10):
        x, _ = point
        course_width = self.course_image.shape[1]

        return course_width - x <= tolerance

    def is_on_course(self, image, point):
        x, y = point
        h, w = image.shape[:2]

        return 0 <= y <= self.height and self.x <= x <= w

    def is_on_path(self, point):
        x, y = point
        try:
            on_path = self.path[y, x] == 255
        except IndexError:
            on_path = False

        return on_path

    def calc_accuracy_percent(self, precision=2):
        if len(self.on_path_checks) > 0:
            acc = sum(self.on_path_checks) / len(self.on_path_checks)
        else:
            acc = 0
        return round(100 * acc, precision)

    def calc_coverage_percent(self, precision=2):
        cov = sum(self.on_path_checks) / self.n_path_points
        return round(100 * cov, precision)
