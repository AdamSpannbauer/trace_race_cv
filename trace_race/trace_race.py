import random
import imutils
import cv2
from .object_tracker import ObjectTracker
from .course import Course
from .crayon import Crayon
from .utils import draw_outlined_box

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
        self._course_path = f'{COURSE_DIR}/course{course_number}.png'
        self._course_height = 110
        self.course = Course(self._course_path, height=self._course_height)

        self.gray_crayon = Crayon(f'{CRAYON_DIR}/gray.png')
        self.crayon_color = crayon_color
        self.crayon_color_bgr = None  # Defined by self._set_crayon_attributes()
        self.crayon = None            # Defined by self._set_crayon_attributes()
        self._set_crayon_attributes()

        self._tracker_type = tracker_type
        self.tracker = ObjectTracker(tracker_type)

        self.frame_width = frame_width
        self.tracker_init_bound_box = (frame_width - frame_width // 5,
                                       frame_width // 20,
                                       frame_width // 10,
                                       frame_width // 10)

    def _set_crayon_attributes(self):
        if self.crayon_color not in CRAYON_BGR_COLOR_DICT.keys():
            print('No valid crayon color provided; choosing at random')

            self.crayon_color = random.choice(list(CRAYON_BGR_COLOR_DICT.keys()))

        self.crayon_color_bgr = CRAYON_BGR_COLOR_DICT[self.crayon_color]
        self.crayon = Crayon(f'{CRAYON_DIR}/{self.crayon_color}.png')

    def play(self):
        vidcap = cv2.VideoCapture(0)

        while True:
            grabbed, raw_frame = vidcap.read()

            if not grabbed:
                break

            # resize the frame and grab dimensions
            raw_frame = imutils.resize(raw_frame, width=self.frame_width)

            # flip frame for more natural motion
            raw_frame = cv2.flip(raw_frame, 1)

            draw_frame = raw_frame.copy()

            # check to see if we are currently tracking an object
            if self.tracker.is_tracking:
                # grab the new bounding box coordinates of the object
                self.tracker.update(raw_frame)
                self.course.draw(draw_frame)

                # check to see if the tracking was a success
                if self.tracker.success:
                    x, y = self.tracker.center_point()
                    if self.course.is_on_course(draw_frame, (x, y)):
                        self.crayon.draw(draw_frame, (x, y))
                        self.course.draw_on_course(draw_frame, (x, y), self.crayon_color_bgr)

                        text = f'Accuracy: {self.course.calc_accuracy()}%'
                        cv2.putText(draw_frame, text, (10, draw_frame.shape[0] - 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    else:
                        self.gray_crayon.draw(draw_frame, (x, y))
            else:
                draw_outlined_box(draw_frame, self.tracker_init_bound_box)

            # show the output frame
            cv2.imshow("Trace Race!", draw_frame)
            key = cv2.waitKey(1) & 0xFF

            if key == 32 and not self.tracker.is_tracking:  # if space bar pressed
                self.tracker.bounding_box = self.tracker_init_bound_box
                self.tracker.init(raw_frame)
            elif key == ord("q") or key == 27:
                break
            elif key == ord("r"):
                self.tracker = ObjectTracker(self._tracker_type)
                self.course = Course(self._course_path, height=self._course_height)

        vidcap.release()

        # close all windows
        cv2.destroyAllWindows()



