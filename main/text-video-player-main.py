import cv2
import numpy as np
from PIL import Image, ImageGrab

# Ascii characters used to create the output 
ASCII_CHARS_1 = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
ASCII_CHARS_2 = ['M', 'W', 'N', 'B', 'E', 'H', 'K', 'R', 'm', 'A', '#', '@', 'X', 'Q', 'b', 'd', '8', 'D', 'F', 'G', 'w', 'P', 'h', 'k', 'Z', 'U', 'S', '6', '9', 'x', 'T', 'p', 'q', 'O', '4', 'e', 'g', 'V', '0', 'a', 'f', '5', '%', '2', '$', 'L', 'Y', 'n', 's', '&', 'C', '3', 'u', 'z', 'J', 'y', 'o', 'v', 'I', 'r', 't', 'c', 'l', 'i', '1', 'j', '?', '7', '=', '>', '<', '"', '+', '*', ']', '[', '}', '(', ')', '{', '/', '\\', '!', ';', '|', ':', '^', '-', '~', "'", ',', '_', '.', '`']
WIDTH = 300		# new width
R_WIDTH = 1920	# resolution width
R_HEIGHT = 1080 # resolution height

def resized_gray_image(image, new_width=WIDTH):
	width,height = image.size
	aspect_ratio = height/width
	new_height = int(aspect_ratio * new_width)
	resized_gray_image = image.resize((new_width,new_height)).convert('L')
	return resized_gray_image

def pix2chars(image):
	pixels = image.getdata()
	characters = "".join([ASCII_CHARS_1[pixel//25] for pixel in pixels])
	return characters

def generate_frame(image, new_width=WIDTH):
	new_image_data = pix2chars(resized_gray_image(image))
	total_pixels = len(new_image_data)
	ascii_image = "\n".join([new_image_data[index:(index+new_width)] for index in range(0, total_pixels, new_width)])
	with open('../output.txt', 'w') as file:
		file.write(ascii_image)

while True:
    # (x, y, w, h), select portion of the screen to screenshot
    img = ImageGrab.grab(bbox=(0, 0, R_WIDTH, R_HEIGHT)) 
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("frame", frame)
    generate_frame(Image.fromarray(frame))
    if cv2.waitKey(1) & 0Xff == ord('q'):
        break

cv2.destroyAllWindows()