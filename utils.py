import ollama
import re
import os 
import subprocess
import requests
from bs4 import BeautifulSoup
import numpy as np
import cv2
import pyautogui
import tkinter as tk
from tkinter import Listbox, BOTH


def get_models_button_func(root):
    new_window = tk.Toplevel(root)
    new_window.title("Available Models")
    new_window.geometry("400x400")

    models_listbox = Listbox(new_window)
    models_listbox.pack(fill=BOTH, expand=True)

    
    for model in getModels():
        models_listbox.insert(END, model)
    



def take_screenshot():
    code = np.random.randint(99, 999999)
    image = pyautogui.screenshot()
    image1 = pyautogui.screenshot(f"images/{code}.png")
    return code





def getModels():
    listOfLLMS = [] 

    url = 'https://ollama.com/search'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
    
        links = soup.find_all('a')
        for link in links:
            linkHREF = link.get('href')
            if "/library/" in linkHREF:
                LLMName = linkHREF.split("/library/")[1]
                listOfLLMS.append(LLMName)
    
    else:
        return (f"Failed to retrieve the page. Status code: {response.status_code}")
    return listOfLLMS



def get_models():
    models = []
    terminal_output = subprocess.check_output("ollama list", shell=True, text=True)
    lines = terminal_output.strip().split('\n')
    for line in lines[1:]:
        split = line.split(" ")
        models.append(split[0])
    return models

def get_size():
    sizes = []
    terminal_output = subprocess.check_output("ollama list", shell=True, text=True)
    lines = terminal_output.strip().split('\n')
    for line in lines[1:]:
        split = line.split(" ")
        c = 0
        for i in split:
            
            if "GB" in i:
                sizes.append(float(split[c-1]))
            c += 1
    totalSize = sum(sizes)

    return totalSize

    


def generate(query, model_name):
    query_with_instruction = f"{query}"
    response = ollama.chat(model=model_name, messages=[{"role": "user", "content": query_with_instruction}])
    model_reply = response.message.content
    model_reply_no_formatting = re.sub(r'[\*\_]{1,2}(.*?)\1', r'\1', model_reply)
    return model_reply_no_formatting

def generateLLAVA(query, model_name, fullPath):
    query_with_instruction = f"look at the image and respond to this query: {query}"
    response = ollama.chat(model=model_name, messages=[{"role": "user", "content": query_with_instruction, "images": [f"{fullPath}"]}])
    model_reply = response.message.content
    model_reply_no_formatting = re.sub(r'[\*\_]{1,2}(.*?)\1', r'\1', model_reply)
    return model_reply_no_formatting
