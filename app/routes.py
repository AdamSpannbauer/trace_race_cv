from flask import Flask, render_template, Response
import cv2


def stream_cv2_vidcap(cv2_vidcap):
    while True:
        grabbed, raw_frame = cv2_vidcap.read()
        jpg_bytes = cv2.imencode('.jpg', raw_frame)[1].tostring()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytes + b'\r\n')


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/video_feed')
def video_feed():
    return Response(stream_cv2_vidcap(cv2.VideoCapture(0)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)

