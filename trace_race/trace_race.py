import imutils
import cv2
import numpy as np
from . import utils
from .object_tracker import ObjectTracker
from .course import Course
from .crayon import Crayon


class TraceRace:
    def __init__(self, crayon_color=None, course_number=None, frame_width=500, tracker_type="csrt", data_path=None):
        self.data_path = data_path

        self._course_number = course_number
        self._course_height = frame_width // 5 + 10
        self.course = Course(self._course_number,
                             height=self._course_height,
                             display_width=(frame_width + 100) // 3,
                             data_path=self.data_path)

        self.crayon = Crayon(crayon_color, data_path=self.data_path)

        self._tracker_type = tracker_type
        self.tracker = ObjectTracker(tracker_type)

        self.frame_width = frame_width
        self.tracker_init_bound_box = (frame_width - frame_width // 5,
                                       frame_width // 20,
                                       frame_width // 10,
                                       frame_width // 10)

        self.play_countdown_start = self.play_countdown = 25
        self.is_finished = False

    def _update_play_countdown(self):
        self.play_countdown -= 1

        cd_percent = self.play_countdown / self.play_countdown_start
        if cd_percent >= 0.66:
            countdown_display = 3
        elif cd_percent >= 0.33:
            countdown_display = 2
        else:
            countdown_display = 1

        return countdown_display

    def _pre_process_frame(self, frame):
        resized_frame = imutils.resize(frame, width=self.frame_width)
        processed_frame = cv2.flip(resized_frame, 1)

        return processed_frame, processed_frame.copy()

    def _display_countdown(self, frame):
        if self.play_countdown > 0:
            countdown_display = self._update_play_countdown()
            utils.put_centered_text(frame, countdown_display,
                                    size=10, color=(0, 0, 255), thickness=10)

    def _display_scores(self, frame, size=0.6, color=(0, 0, 255), thickness=2, font=cv2.FONT_HERSHEY_SIMPLEX):
        frame_height = frame.shape[0]

        acc_text_xy = (10, frame_height - 20)
        cov_text_xy = (10, frame_height - 40)

        acc_text = f'Accuracy: {self.course.calc_accuracy_percent()}%'
        cov_text = f'Coverage: {self.course.calc_coverage_percent()}%'

        cv2.putText(frame, acc_text, acc_text_xy, font, size, color, thickness)
        cv2.putText(frame, cov_text, cov_text_xy, font, size, color, thickness)

    def _trace_race_frame(self, frame, keypress):
        raw_frame, draw_frame = self._pre_process_frame(frame)

        if not self.tracker.is_tracking:
            utils.draw_outlined_box(draw_frame, self.tracker_init_bound_box)
        else:
            countdown_finished = self.play_countdown <= 0

            self.tracker.update(raw_frame)
            self.course.draw(draw_frame, update=countdown_finished)
            self._display_countdown(draw_frame)

            if self.tracker.success:
                x, y = self.tracker.center_point()

                if not countdown_finished:
                    self.crayon.draw(draw_frame, (x, y), use_color=True)
                else:
                    point_on_course = self.course.is_on_course(draw_frame, (x, y))
                    use_color_crayon = point_on_course and not self.is_finished

                    self.crayon.draw(draw_frame, (x, y), use_color=use_color_crayon)
                    self.is_finished = self.course.draw_on_course(draw_frame, (x, y),
                                                                  self.crayon.color_bgr,
                                                                  self.is_finished)
                    self._display_scores(draw_frame)

        draw_frame = self.course.display_below(draw_frame)

        if keypress == 32 and not self.tracker.is_tracking:
            self.tracker.bounding_box = self.tracker_init_bound_box
            self.tracker.init(raw_frame)
        elif keypress in [ord("R"), ord("r")]:
            self.play_countdown = self.play_countdown_start
            self.tracker = ObjectTracker(self._tracker_type)
            self.course = Course(self._course_number, height=self._course_height, data_path=self.data_path)
            self.is_finished = False

        return draw_frame

    def _append_instructions(self, frame):
        canvas = np.ones((50, 400, 3), dtype='uint8')

        if not self.tracker.is_tracking:
            image_text = 'Place finger in box and press space to begin'
        else:
            image_text = "Press 'R' to reset"

        utils.put_centered_text(canvas, image_text,
                                size=0.5, color=(0, 0, 255), thickness=1)

        canvas = imutils.resize(canvas, width=frame.shape[1])

        return np.vstack((frame, canvas))

    def play_flask(self, frame, keypress):
        reset_keypress = -1
        display_frame = self._trace_race_frame(frame, keypress)

        return display_frame, reset_keypress

    def play(self):
        vidcap = cv2.VideoCapture(0)
        keypress = -1

        while True:
            grabbed, frame = vidcap.read()
            if not grabbed:
                break

            display_frame = self._trace_race_frame(frame, keypress)
            display_frame = self._append_instructions(display_frame)
            cv2.imshow("Trace Race!", display_frame)

            keypress = cv2.waitKey(1) & 0xFF
            if keypress == ord("q") or keypress == 27:
                break

        vidcap.release()
        cv2.destroyAllWindows()
