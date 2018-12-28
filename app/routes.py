from flask import Flask, render_template
from flask import request, Response
import cv2

keypress = None


def stream_cv2_vidcap(cv2_vidcap):
    global keypress

    while True:
        # TODO: rm this debug print
        if keypress is not None:
            print(f'key pressed: {keypress}')
            print('key press reset')
            keypress = None

        grabbed, raw_frame = cv2_vidcap.read()
        raw_frame = cv2.flip(raw_frame, 1)
        jpg_bytes = cv2.imencode('.jpg', raw_frame)[1].tostring()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytes + b'\r\n')


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/video_feed')
def video_feed():
    return Response(stream_cv2_vidcap(cv2.VideoCapture(0)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/postmethod', methods=['POST'])
def get_post_javascript_data():
    global keypress
    keypress = request.form['keypress']
    return keypress


if __name__ == '__main__':
    app.run(debug=True)

