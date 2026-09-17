from flask import Flask, render_template, Response
from ultralytics import YOLO
from picamera2 import Picamera2
import cv2

app = Flask(__name__)

model = YOLO("mira_exp019.pt")

picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={"format": "RGB888", "size": (1920, 1080)}
)

picam2.configure(config)

camera_ligada = False

objeto_detectado = None
confianca = 0.0

def generate_frames():
    global camera_ligada
    global objeto_detectado
    global confianca
    while camera_ligada:
        frame = picam2.capture_array()

        results = model(frame, verbose=False)



        for box in results[0].boxes:
            id_classe = int(box.cls[0])
            nome_classe = model.names[id_classe]
            confianca = float(box.conf[0])

            if confianca >= 0.7:
                objeto_detectado = nome_classe


        frame = results[0].plot()

        sucess, buffer = cv2.imencode(
            ".jpg",
            frame,
            [cv2.IMWRITE_JPEG_QUALITY, 95]
        )

        if not sucess:
            continue

        frame = buffer.tobytes()
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")



    
@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/iniciar-camera")
def iniciar_camera():
    global camera_ligada

    if not camera_ligada:
        picam2.start()
        camera_ligada = True

    return "ok"


@app.route("/parar-camera")
def parar_camera():
    global camera_ligada

    camera_ligada = False

    if picam2.started:
        picam2.stop()

    return "ok"

@app.route("/resultado")
def mostrarResultado():
    global objeto_detectado
    global confianca

    if confianca >= 0.7:
        parar_camera()

    return {"classe": objeto_detectado}

@app.route("/foto")
def camera():
   return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run()