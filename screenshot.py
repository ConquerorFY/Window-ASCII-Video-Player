from PIL import ImageGrab
import win32gui

hwnd = win32gui.FindWindow(None, r'Task Manager')
win32gui.SetForegroundWindow(hwnd)
dimensions = win32gui.GetWindowRect(hwnd)

image = ImageGrab.grab(dimensions)
image.show()