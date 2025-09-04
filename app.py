import cv2
from flask import Flask, Response
from detector import detect_and_decode
import numpy as np # Add this import for the detector.py logic

app = Flask(__name__)

@app.route('/')
def index():
    # A simple web page with the video feed.
    return """
    <html>
        <head>
            <title>Barcode and QR Code Scanner</title>
        </head>
        <body>
            <h1>Live Barcode and QR Code Scanner</h1>
            <img src="/video_feed" width="640" height="480">
        </body>
    </html>
    """

def generate_frames():
    camera = cv2.VideoCapture(0) # Use 0 for the default camera

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            processed_frame, decoded_data = detect_and_decode(frame)

            # Check for decoded data and humanize it
            if decoded_data:
                for item in decoded_data:
                    print(f"Detected: {item['type']} -> {item['data']}")

            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
    