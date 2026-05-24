
from flask import Flask, request, render_template_string
import cv2
import numpy as np
import onnxruntime as ort
import os
import requests
app = Flask(__name__)

session = ort.InferenceSession("convnext_regression.onnx")
input_name = session.get_inputs()[0].name

MAX_PM = 530 

def run_model(img):
    img = cv2.resize(img, (224,224))
    img = img.astype(np.float32)/255.0
    img = np.transpose(img, (2,0,1))
    img = np.expand_dims(img,0)

    outputs = session.run(None, {input_name: img})
    pm = float(outputs[0][0]) * MAX_PM
    return pm


HTML_PAGE = """
<h2>PM2.5 Predictor</h2>

<form method="post" action="/upload" enctype="multipart/form-data">

<input type="file" name="image">

<input type="submit" value="Predict">

</form>

{% if pm %}
<h3>Predicted PM2.5: {{pm}}</h3>
{% endif %}
"""


@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["image"]

    img = cv2.imdecode(
        np.frombuffer(file.read(), np.uint8),
        cv2.IMREAD_COLOR
    )

    pm = run_model(img)

    import time

    with open("/home/arduino/vision_env/predicted_pm.txt","w") as f:
        f.write(str(int(pm)))

    time.sleep(0.05)

    return {"pm25": pm}

app.run(host="0.0.0.0", port=5000)