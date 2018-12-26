import random
import imutils
import cv2
from .object_tracker import ObjectTracker
from .course import Course
from .crayon import Crayon

CRAYON_DIR = 'crayons'
COURSE_DIR = 'courses'

CRAYON_BGR_COLOR_DICT = {
    'blue': (255, 0, 0),
    'green': (0, 255, 0),
    'pink': (240, 70, 220),
    'red': (0, 0, 255),
    'yellow': (60, 200, 250)
}


class TraceRace:
    def __init__(self, crayon_color=None, course_number=None, frame_width=500, tracker_type="csrt"):
        # TODO: add more courses, and random/user selection
        course_number = 0
        self.course = Course(f'{COURSE_DIR}/course{course_number}.png')

        self.crayon_color = crayon_color
        self.crayon_color_bgr = None  # Defined by self._set_crayon_attributes()
        self.crayon = None            # Defined by self._set_crayon_attributes()
        self._set_crayon_attributes()

        self.tracker = ObjectTracker(tracker_type)

        self.frame_width = frame_width

    def _set_crayon_attributes(self):
        if self.crayon_color not in CRAYON_BGR_COLOR_DICT.keys():
            print('No valid crayon color provided; choosing at random')

            self.crayon_color = random.sample(CRAYON_BGR_COLOR_DICT.keys())

        self.crayon_color_bgr = CRAYON_BGR_COLOR_DICT[self.crayon_color]
        self.crayon = Crayon(f'{CRAYON_DIR}/{self.crayon_color}.png')

    def play(self):
        vidcap = cv2.VideoCapture(0)

        while True:
            grabbed, frame = vidcap.read()

            if not grabbed:
                break

            # resize the frame and grab dimensions
            frame = imutils.resize(frame, width=self.frame_width)

            # flip frame for more natural motion
            frame = cv2.flip(frame, 1)

            # check to see if we are currently tracking an object
            if self.tracker.is_tracking:
                # grab the new bounding box coordinates of the object
                self.tracker.update(frame)
                self.course.draw(frame)

                # check to see if the tracking was a success
                if self.tracker.success:
                    x, y = self.tracker.center_point()
                    self.crayon.draw(frame, (x, y))
            else:
                self.course.draw(frame)

            # show the output frame
            cv2.imshow("Trace Race!", frame)
            key = cv2.waitKey(1) & 0xFF

            # if the 's' key is selected, we are going to "select" a bounding
            # box to track
            if key == ord("s"):
                self.tracker.bounding_box = cv2.selectROI("Frame", frame, fromCenter=False,
                                                          showCrosshair=True)

                self.tracker.init(frame)
            elif key == ord("q") or key == 27:
                break

        vidcap.release()

        # close all windows
        cv2.destroyAllWindows()



