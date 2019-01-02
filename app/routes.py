from flask import Flask, render_template
from flask import request, Response
import cv2
import numpy as np
import base64
from trace_race import TraceRace


app = Flask(__name__)
# gave up on doing assets the right way
IMG_PATH = 'https://raw.githubusercontent.com/AdamSpannbauer/trace_race_cv/master/trace_race/data'
keypress = -1
b64_img_data = None


def stream_trace_race(data_path):
    global keypress
    global b64_img_data

    keypress = -1
    flask_trace_race = TraceRace(frame_width=750, data_path=data_path)

    while True:
        raw_frame = decode_frame(b64_img_data)

        display_frame, keypress = flask_trace_race.play_flask(raw_frame, int(keypress))

        jpg_bytes = cv2.imencode('.jpg', display_frame)[1].tostring()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytes + b'\r\n')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/video_feed')
def video_feed():
    return Response(stream_trace_race(data_path=IMG_PATH),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def decode_frame(b64_str):
    decoded_img_data = base64.b64decode(b64_str)

    np_arr = np.fromstring(decoded_img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    return img


@app.route('/get_frame', methods=['POST'])
def get_frame():
    global b64_img_data
    img_uri = request.form['img']
    b64_img_data = img_uri.split(',')[1]

    return b64_img_data


@app.route('/keypress', methods=['POST'])
def get_post_javascript_data():
    global keypress
    keypress = request.form['keypress']
    return keypress


if __name__ == '__main__':
    app.run(debug=True)
