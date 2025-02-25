import ollama
from ollama import Client
import re
import os
import numpy as np
import pyautogui


def take_screenshot():
    code = np.random.randint(99, 999999)
    image = pyautogui.screenshot()
    image1 = pyautogui.screenshot(f"images/{code}.png")
    return code


def get_models():
    try:
        client = Client()
        models = client.list()
        return [model['model'] for model in models['models']]
    except Exception as e:
        return f"Error: {str(e)}"

def get_size():
    try:
        path = os.path.expanduser("~/.ollama/models")
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return round(total_size / (1024 * 1024 * 1024), 2)  
    except Exception as e:
        return f"Error: {str(e)}"
