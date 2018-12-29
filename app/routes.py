from flask import Flask, render_template
from flask import request, Response
import cv2
from trace_race import TraceRace


app = Flask(__name__)
# gave up on doing assets the right way
IMG_PATH = 'https://raw.githubusercontent.com/AdamSpannbauer/trace_race_cv/master/trace_race/data'


def stream_trace_race(cv2_vidcap, data_path):
    global keypress

    keypress = -1
    flask_trace_race = TraceRace(frame_width=750, data_path=data_path)

    while True:
        grabbed, raw_frame = cv2_vidcap.read()
        display_frame, keypress = flask_trace_race.play_flask(raw_frame, int(keypress))

        jpg_bytes = cv2.imencode('.jpg', display_frame)[1].tostring()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytes + b'\r\n')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/video_feed')
def video_feed():
    return Response(stream_trace_race(cv2.VideoCapture(0), data_path=IMG_PATH),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/postmethod', methods=['POST'])
def get_post_javascript_data():
    global keypress
    keypress = request.form['keypress']
    return keypress


if __name__ == '__main__':
    app.run(debug=True)
