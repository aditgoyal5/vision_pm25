from flask import Flask, request, render_template_string
import cv2
import numpy as np
import onnxruntime as ort
import os
import csv
import time

app = Flask(__name__)

session = ort.InferenceSession("convnext_regression.onnx")
input_name = session.get_inputs()[0].name

MAX_PM = 530

CSV_FILE = "calibration_data.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE,"w",newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp","predicted_pm","actual_pm"])


def run_model(img):
    img = cv2.resize(img,(224,224))
    img = img.astype(np.float32)/255.0
    img = np.transpose(img,(2,0,1))
    img = np.expand_dims(img,0)

    outputs = session.run(None,{input_name: img})
    pm = float(outputs[0][0]) * MAX_PM

    return pm


HTML_PAGE = """

<h2>PM2.5 Predictor + Calibration</h2>

<form method="post" action="/upload" enctype="multipart/form-data">

Select sky image:<br>
<input type="file" name="image"><br><br>

Actual PM reading (from sensor):<br>
<input type="number" step="0.1" name="actual_pm"><br><br>

<input type="submit" value="Predict + Save">

</form>

{% if pm %}
<hr>
<h3>Predicted PM2.5: {{pm}}</h3>
<h4>Actual PM2.5: {{actual_pm}}</h4>
{% endif %}

"""


@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


@app.route("/upload",methods=["POST"])
def upload():

    file = request.files["image"]
    actual_pm = request.form.get("actual_pm")

    img = cv2.imdecode(
        np.frombuffer(file.read(),np.uint8),
        cv2.IMREAD_COLOR
    )

    pm = run_model(img)

    # store predicted value for UNO Q
    with open("/home/arduino/vision_env/predicted_pm.txt","w") as f:
        f.write(str(int(pm)))

    # store calibration data
    if actual_pm:
        with open(CSV_FILE,"a",newline="") as f:
            writer = csv.writer(f)
            writer.writerow([time.time(), pm, actual_pm])

    time.sleep(0.05)

    return render_template_string(
        HTML_PAGE,
        pm=round(pm,2),
        actual_pm=actual_pm
    )


app.run(host="0.0.0.0",port=5000)