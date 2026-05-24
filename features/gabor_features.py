import cv2
import numpy as np
from scipy.stats import skew, kurtosis

def extract_gabor_features(image):

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray = cv2.resize(gray, (200, 200))

    features = []

    orientations = [0, np.pi/4, np.pi/2, 3*np.pi/4]
    frequencies = [0.1, 0.2]

    for theta in orientations:
        for freq in frequencies:

            kernel = cv2.getGaborKernel(
                (21, 21),
                sigma=5,
                theta=theta,
                lambd=1/freq,
                gamma=0.5,
                psi=0,
                ktype=cv2.CV_32F
            )

            filtered = cv2.filter2D(gray, cv2.CV_32F, kernel)
            flat = filtered.flatten()

            mean_val = np.mean(flat)
            var_val = np.var(flat)

            if var_val < 1e-6:
                skew_val = 0.0
                kurt_val = 0.0
            else:
                skew_val = skew(flat)
                kurt_val = kurtosis(flat)

            skew_val = 0.0 if np.isnan(skew_val) else skew_val
            kurt_val = 0.0 if np.isnan(kurt_val) else kurt_val

            features.extend([mean_val, var_val, skew_val, kurt_val])

    features = np.array(features, dtype=np.float32)
    features = np.nan_to_num(features)

    return features