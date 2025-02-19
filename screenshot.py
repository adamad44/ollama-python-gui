import numpy as np
import cv2
import pyautogui



def take_screenshot():
    code = np.random.randint(99, 999999)
    image = pyautogui.screenshot()
    image1 = pyautogui.screenshot(f"images/{code}.png")
    return code

