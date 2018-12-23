from imutils.video import FPS
import argparse
import imutils
import cv2
from object_tracker import ObjectTracker
from tracer import Tracer
from course import Course


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--tracker", default="kcf",
                help="OpenCV object tracker type")
ap.add_argument("-w", "--width", default=500, type=int,
                help='Display width')
args = vars(ap.parse_args())

tracker = ObjectTracker(args['tracker'])
tracer = Tracer()
course = Course(cv2.imread('courses/course0.png'))

vidcap = cv2.VideoCapture(0)

# initialize the FPS throughput estimator
fps = None

# loop over frames from the video stream
while True:
    # grab the current frame, then handle if we are using a
    # VideoStream or VideoCapture object
    grabbed, frame = vidcap.read()

    # check to see if we have reached the end of the stream
    if not grabbed:
        break

    # resize the frame (so we can process it faster) and grab the
    # frame dimensions
    frame = imutils.resize(frame, width=args['width'])
    (frame_h, frame_w) = frame.shape[:2]
    frame = cv2.flip(frame, 1)

    # check to see if we are currently tracking an object
    if tracker.is_tracking:
        # grab the new bounding box coordinates of the object
        tracker.update(frame)

        # check to see if the tracking was a success
        if tracker.success:
            x, y = tracker.center_point()
            tracer.points.append((x, y))
            tracer.draw(frame)

        # update the FPS counter
        fps.update()
        fps.stop()

        # initialize the set of information we'll be displaying on
        # the frame
        info = [
            ("Tracker", args["tracker"]),
            ("Success", "Yes" if tracker.success else "No"),
            ("FPS", "{:.2f}".format(fps.fps())),
        ]

        # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, frame_h - ((i * 20) + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # show the output frame
    course.draw(frame)
    cv2.imshow("Trace Race!", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 's' key is selected, we are going to "select" a bounding
    # box to track
    if key == ord("s"):
        tracker.bounding_box = cv2.selectROI("Frame", frame, fromCenter=False,
                                             showCrosshair=True)

        tracker.init(frame)
        fps = FPS().start()
    elif key == ord("q") or key == 27:
        break

vidcap.release()

# close all windows
cv2.destroyAllWindows()



