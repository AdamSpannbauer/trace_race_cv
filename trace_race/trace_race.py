import imutils
import cv2
from .object_tracker import ObjectTracker
from .course import Course
from .crayon import Crayon
from .utils import draw_outlined_box, put_centered_text


class TraceRace:
    def __init__(self, crayon_color=None, course_number=None, frame_width=500, tracker_type="csrt", data_path=None):
        self.data_path = data_path

        self._course_number = course_number
        self._course_height = 110
        self.course = Course(self._course_number, height=self._course_height, data_path=self.data_path)

        self.crayon = Crayon(crayon_color, data_path=self.data_path)

        self._tracker_type = tracker_type
        self.tracker = ObjectTracker(tracker_type)

        self.frame_width = frame_width
        self.tracker_init_bound_box = (frame_width - frame_width // 5,
                                       frame_width // 20,
                                       frame_width // 10,
                                       frame_width // 10)

        self.play_countdown_start = self.play_countdown = 40
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
            put_centered_text(frame, countdown_display,
                              size=10, color=(0, 0, 255), thickness=10)

            countdown_finished = False
        else:
            countdown_finished = True

        return countdown_finished

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
            draw_outlined_box(draw_frame, self.tracker_init_bound_box)
        else:
            countdown_finished = self._display_countdown(draw_frame)

            self.tracker.update(raw_frame)
            self.course.draw(draw_frame, update=countdown_finished)

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
            cv2.imshow("Trace Race!", display_frame)

            keypress = cv2.waitKey(1) & 0xFF
            if keypress == ord("q") or keypress == 27:
                break

        vidcap.release()
        cv2.destroyAllWindows()
