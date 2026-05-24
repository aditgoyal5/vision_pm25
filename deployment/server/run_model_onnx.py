import onnxruntime as ort
import cv2
import numpy as np
import time

MAX_PM = 530.0

session = ort.InferenceSession("convnext_regression.onnx")

img = cv2.imread("test.jpg")
img = cv2.resize(img,(224,224))
img = img.astype(np.float32)/255.0
img = np.transpose(img,(2,0,1))
img = np.expand_dims(img,0)

start = time.time()

outputs = session.run(None, {"image": img})

pm = float(outputs[0][0]) * MAX_PM

end = time.time()

print("Predicted PM2.5:", pm)
print("Inference time:", end-start)