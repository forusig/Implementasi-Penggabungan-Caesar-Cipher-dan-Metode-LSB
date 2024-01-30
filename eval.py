import cv2
import numpy as np

img_original = cv2.imread('bgr.png')
img_result = cv2.imread('hasil_bgr.png')
img_original = img_original.astype(float)
img_result = img_result.astype(float)
mse = np.mean((img_original - img_result)**2)
psnr = 10 * np.log10((255**2) / mse)
print(f"MSE: {mse}")
print(f"PSNR: {psnr} dB")
