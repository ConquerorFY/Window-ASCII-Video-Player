import numpy as np
import cv2
from PIL import ImageGrab

# do something every 30 frames
n, read= 0, 30
while True:
    # (x, y, w, h), slect portion of the screen to screenshot
    img = ImageGrab.grab(bbox=(0, 1000, 100, 1100)) 
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    if n % read == 0:
        cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0Xff == ord('q'):
        break
    n+=1

cv2.destroyAllWindows()