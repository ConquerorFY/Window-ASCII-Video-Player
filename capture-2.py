import cv2
import numpy as np
from PIL import ImageGrab
import win32gui

def capture_dynamic():
    toplist, winlist = [], []
    
    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

    win32gui.EnumWindows(enum_cb, toplist)

    wnd = [(hwnd, title) for hwnd, title in winlist if 'task manager' in title.lower()]
    # wnd = [(hwnd, title) for hwnd, title in winlist]
    print(wnd)

    if wnd:
        wnd = wnd[0]
        hwnd = wnd[0]

        bbox = win32gui.GetWindowRect(hwnd)
        img = ImageGrab.grab(bbox)
        return img
    else:
        return None

while(True):
    # Dynamic Version
    screen_grab =  capture_dynamic()

    if (screen_grab == None):
        print("No Window Found! Please Try Again")
        break

    screen_grab = np.array(screen_grab)
    cv2.imshow('window', cv2.cvtColor(screen_grab, cv2.COLOR_BGR2RGB))

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break