import os 
import sys
import cv2
import numpy as np
from PIL import Image, ImageGrab
import win32gui

# Ascii characters used to create the output 
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def resized_gray_image(image, new_width=70):
	width,height = image.size
	aspect_ratio = height/width
	new_height = int(aspect_ratio * new_width)
	resized_gray_image = image.resize((new_width,new_height)).convert('L')
	return resized_gray_image

def pix2chars(image):
	pixels = image.getdata()
	characters = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
	return characters

def generate_frame(image, new_width=70):
	new_image_data = pix2chars(resized_gray_image(image))
	total_pixels = len(new_image_data)
	ascii_image = "\n".join([new_image_data[index:(index+new_width)] for index in range(0, total_pixels, new_width)])
	sys.stdout.write(ascii_image)
	os.system('cls' if os.name == 'nt' else 'clear')

def capture_dynamic():
    toplist, winlist = [], []
    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_cb, toplist)
    wnd = [(hwnd, title) for hwnd, title in winlist if 'task manager' in title.lower()]
    if wnd:
        wnd = wnd[0]
        hwnd = wnd[0]
        bbox = win32gui.GetWindowRect(hwnd)
        img = ImageGrab.grab(bbox)
        return img
    else:
        return None

while True:
    # Dynamic Version
    screen_grab =  capture_dynamic()
    if screen_grab == None:
        print("No Window Found! Please Try Again")
        break
    screen_grab = np.array(screen_grab)
    cv2.imshow('window', cv2.cvtColor(screen_grab, cv2.COLOR_BGR2RGB))
    generate_frame(Image.fromarray(cv2.cvtColor(screen_grab, cv2.COLOR_BGR2RGB)))
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

# cap = capture_window("Task Manager")

# while True:
# 	ret, frame = cap.read()
# 	cv2.imshow("frame", frame)
# 	generate_frame(Image.fromarray(frame))
# 	cv2.waitKey(10)
