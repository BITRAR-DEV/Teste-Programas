from flask import Flask, render_template
from picamera2 import Picamera2
import cv2


app = Flask(__name__)

picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={"format": "RGB888", "size": (1280, 720)}
)

picam2.configure(config)
picam2.start()

while True:
    frame = picam2.capture_array()
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) == 27:
        break





@app.route("/")
def homepage():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()