from flask import Flask, request, render_template_string
import cv2
import numpy as np
import onnxruntime as ort
import os
import csv
import time

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

session = ort.InferenceSession("convnext_regression.onnx")
input_name = session.get_inputs()[0].name

MAX_PM = 530

CSV_FILE = "calibration_data.csv"

# create csv if not exists
if not os.path.exists(CSV_FILE):

    with open(CSV_FILE,"w",newline="") as f:

        writer = csv.writer(f)

        writer.writerow(["timestamp","predicted_pm","actual_pm"])


# ---------- MODEL ----------

def run_model(img):

    img = cv2.resize(img,(224,224))

    img = img.astype(np.float32)/255.0

    img = np.transpose(img,(2,0,1))

    img = np.expand_dims(img,0)

    outputs = session.run(None,{input_name: img})

    pm_raw = float(outputs[0][0]) * MAX_PM

    return pm_raw



# ---------- CALIBRATION ----------

def compute_calibration():

    data = []

    with open(CSV_FILE,"r") as f:

        reader = csv.reader(f)

        next(reader)  # skip header

        for row in reader:

            try:

                pred = float(row[1])

                actual = float(row[2])

                data.append((pred,actual))

            except:

                pass


    # not enough data yet
    if len(data) < 5:

        return None


    X = np.array([d[0] for d in data]).reshape(-1,1)

    y = np.array([d[1] for d in data])


    poly = PolynomialFeatures(degree=2)

    X_poly = poly.fit_transform(X)

    model = LinearRegression()

    model.fit(X_poly,y)


    a = model.coef_[2]

    b = model.coef_[1]

    c = model.intercept_


    return a,b,c



def apply_calibration(pm_raw):

    calib = compute_calibration()


    # if insufficient data, return raw
    if calib is None:

        return pm_raw


    a,b,c = calib


    pm_corrected = (

        a*(pm_raw**2)

        + b*(pm_raw)

        + c

    )


    return pm_corrected



# ---------- UI ----------

HTML_PAGE = """

<h2>PM2.5 Predictor (Self-Calibrating)</h2>

<form method="post" action="/upload" enctype="multipart/form-data">

Select sky image:<br>
<input type="file" name="image"><br><br>

Actual PM reading from sensor:<br>
<input type="number" step="0.1" name="actual_pm"><br><br>

<input type="submit" value="Predict">

</form>

{% if raw_pm %}

<hr>

<!-- <h3>Raw PM prediction: {{raw_pm}}</h3> -->

<h3>Calibrated PM prediction: {{pm}}</h3>

<h4>Actual PM entered: {{actual_pm}}</h4>

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


    pm_raw = run_model(img)

    pm_corrected = apply_calibration(pm_raw)


    # save datapoint if actual value provided
    if actual_pm:

        with open(CSV_FILE,"a",newline="") as f:

            writer = csv.writer(f)

            writer.writerow([

                time.time(),

                pm_raw,

                actual_pm

            ])


    # send corrected value to MCU
    with open("/home/arduino/vision_env/predicted_pm.txt","w") as f:

        f.write(str(int(pm_corrected)))


    time.sleep(0.05)


    return render_template_string(

        HTML_PAGE,

        pm = round(pm_corrected,2),

        raw_pm = round(pm_raw,2),

        actual_pm = actual_pm

    )



app.run(host="0.0.0.0",port=5000)