from flask import Flask, Response
from flask_cors import CORS
import cv2

app = Flask(__name__)
CORS(app)

RTSP_SWEDEN_URL = "http://195.196.36.242/mjpg/video.mjpg"
RTSP_PENDELCAM_URL = "http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg"


def video_stream(url):
    cap = cv2.VideoCapture(url)
    while True:
        success, frame = cap.read()
        if not success:
            break
        ret, buffer = cv2.imencode(".jpg", frame)
        if not ret:
            continue
        frame = buffer.tobytes()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/video_feed_sweden")
def video_feed_sweden():
    return Response(
        video_stream(RTSP_SWEDEN_URL),
        mimetype="multipart/x-mixed-replace; boundary=--frame",
    )


@app.route("/video_feed_pendelcam")
def video_feed_pendelcam():
    return Response(
        video_stream(RTSP_PENDELCAM_URL),
        mimetype="multipart/x-mixed-replace; boundary=--frame",
    )


if __name__ == "__main__":
    app.run(debug=True)
