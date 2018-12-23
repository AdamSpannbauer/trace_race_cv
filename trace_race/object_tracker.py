import cv2


object_trackers = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}


class ObjectTracker:
    def __init__(self, tracker_type='kcf'):
        self.tracker_type = tracker_type
        self.tracker = object_trackers[tracker_type]()
        self.bounding_box = None
        self.is_tracking = False
        self.success = False

    def init(self, frame):
        self.is_tracking = True
        self.tracker.init(frame, self.bounding_box)

    def update(self, frame):
        self.success, self.bounding_box = self.tracker.update(frame)

    def center_point(self):
        (x, y, w, h) = [int(v) for v in self.bounding_box]
        center_x = round(x + w / 2)
        center_y = round(y + h / 2)

        return center_x, center_y
