import numpy as np
import cv2
from mss import mss

sct = mss()
monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

while True:
    img = sct.grab(monitor)
    cv2.imshow("Netstream", np.array(img))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()