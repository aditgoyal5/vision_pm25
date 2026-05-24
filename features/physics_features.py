import cv2
import numpy as np

def extract_physics_features(image):

    img = cv2.resize(image, (224, 224))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    features = []

    grid_size = 4
    h, w, _ = img.shape
    patch_h = h // grid_size
    patch_w = w // grid_size

    for i in range(grid_size):
        for j in range(grid_size):

            y1 = i * patch_h
            y2 = (i + 1) * patch_h
            x1 = j * patch_w
            x2 = (j + 1) * patch_w

            patch_rgb = rgb[y1:y2, x1:x2]
            patch_hsv = hsv[y1:y2, x1:x2]

            R = patch_rgb[:,:,0].astype(np.float32)
            G = patch_rgb[:,:,1].astype(np.float32)
            B = patch_rgb[:,:,2].astype(np.float32)

            B_safe = np.where(B == 0, 1, B)

            mean_R = np.mean(R)
            mean_G = np.mean(G)
            mean_B = np.mean(B)
            rb_ratio = np.mean(R / B_safe)

            saturation_mean = np.mean(patch_hsv[:,:,1])
            value_std = np.std(patch_hsv[:,:,2])

            min_channel = np.minimum(np.minimum(R, G), B)
            dark_channel = np.mean(min_channel)

            features.extend([
                mean_R,
                mean_G,
                mean_B,
                rb_ratio,
                saturation_mean,
                value_std,
                dark_channel
            ])

    return np.array(features, dtype=np.float32)