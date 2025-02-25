import tkinter as tk
from tkinter import *
import threading
import ollama
from ollama import Client
import re
import os
import numpy as np
import pyautogui

BACKGROUND_COLOR = "#1e1e2e"
TEXT_BG_COLOR = "#282a36"
TEXT_FG_COLOR = "#f8f8f2"
BUTTON_BG_COLOR = "#6272a4"
BUTTON_FG_COLOR = "#f8f8f2"
BUTTON_ACTIVE_BG = "#8293d8"
GENERATING_FG_COLOR = "#50fa7b"
ERROR_FG_COLOR = "#ff5555"
BORDER_COLOR = "#44475a"
DROPDOWN_HOVER = "#44475a"

root = tk.Tk()
root.title("Local LLM")
root.state('zoomed')
root.config(bg=BACKGROUND_COLOR)

stop_event = threading.Event()

def get_models():
    try:
        client = Client()
        models = client.list()
        return [model['model'] for model in models['models']]
    except Exception as e:
        return f"Error: {str(e)}"

models = get_models()

def generate(prompt, model):
    try:
        client = Client()
        stream = client.generate(model=model, prompt=prompt, stream=True)
        for chunk in stream:
            if stop_event.is_set():
                break
            if 'response' in chunk:
                outputBox.insert(END, chunk['response'])
    except Exception as e:
        print(f"Error: {str(e)}")

def gen():
    try:
        outputBox.delete(1.0, END)
        generate_button.config(state=DISABLED, text="Generating...", fg=GENERATING_FG_COLOR)
        stop_button.config(state=NORMAL)
        
        selected_model = model_selection.get()
        query = user_input.get("1.0", END)
        generate(query, selected_model)
            
        generate_button.config(state=NORMAL, text="Generate", fg="black")
        stop_button.config(state=DISABLED)
    except Exception as e:
        outputBox.insert(END, f"An error occurred: {e}")
        generate_button.config(state=NORMAL, text="Generate", fg="black")
        stop_button.config(state=DISABLED)

def startThreadGen():
    global stop_event
    stop_event.clear()
    threading.Thread(target=gen).start()

def stop_generation():
    global stop_event
    stop_event.set()

def on_enter(event):
    if generate_button['state'] != DISABLED:  
        startThreadGen()
        return "break"
    return "break"

def on_shift_enter(event):
    user_input.insert(INSERT, "\n")
    return "break"

main_frame = Frame(root, bg=BACKGROUND_COLOR)
main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

title_label = Label(main_frame, text="Ollama Interface", font=("Helvetica", 16, "bold"), bg=BACKGROUND_COLOR, fg=TEXT_FG_COLOR)
title_label.pack(pady=(0, 15))

output_frame = Frame(main_frame, bg=BORDER_COLOR, padx=2, pady=2)
output_frame.pack(fill=BOTH, expand=True, pady=10)

scroll_y = Scrollbar(output_frame)
scroll_y.pack(side=RIGHT, fill=Y)

outputBox = Text(output_frame, height=30, width=80, font=("Consolas", 11), wrap=WORD, bg=TEXT_BG_COLOR, fg=TEXT_FG_COLOR, padx=10, pady=10, yscrollcommand=scroll_y.set, insertbackground=TEXT_FG_COLOR)
outputBox.pack(fill=BOTH, expand=True)
scroll_y.config(command=outputBox.yview)

input_frame = Frame(main_frame, bg=BORDER_COLOR, padx=2, pady=2)
input_frame.pack(fill=X, pady=10)

scroll_y_input = Scrollbar(input_frame)
scroll_y_input.pack(side=RIGHT, fill=Y)

user_input = Text(input_frame, height=4, width=80, font=("Consolas", 11), bg=TEXT_BG_COLOR, fg=TEXT_FG_COLOR, padx=10, pady=10, wrap=WORD, yscrollcommand=scroll_y_input.set, insertbackground=TEXT_FG_COLOR)
user_input.insert(1.0, "Enter your prompt here...")
user_input.pack(fill=X)
scroll_y_input.config(command=user_input.yview)
user_input.bind("<Return>", on_enter)
user_input.bind("<Shift-Return>", on_shift_enter)

control_frame = Frame(main_frame, bg=BACKGROUND_COLOR)
control_frame.pack(fill=X, pady=10)

model_selection = StringVar()
model_selection.set(models[0])

model_label = Label(control_frame, text="Model:", bg=BACKGROUND_COLOR, fg=TEXT_FG_COLOR, font=("Helvetica", 11))
model_label.pack(side=LEFT, padx=(0, 5))

model_selection_dropdown = OptionMenu(control_frame, model_selection, *models)
model_selection_dropdown.config(bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, font=("Helvetica", 11), activebackground=DROPDOWN_HOVER, activeforeground=BUTTON_FG_COLOR, highlightbackground=BORDER_COLOR, highlightthickness=1, bd=0)
model_selection_dropdown["menu"].config(bg=TEXT_BG_COLOR, fg=BUTTON_FG_COLOR, activebackground=DROPDOWN_HOVER)
model_selection_dropdown.pack(side=LEFT, padx=5)

generate_button = Button(control_frame, text="Generate", command=startThreadGen, bg=BUTTON_BG_COLOR, fg="black", font=("Helvetica", 11, "bold"), activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_FG_COLOR, relief=FLAT, padx=20, pady=5)
generate_button.pack(side=RIGHT, padx=5)

stop_button = Button(control_frame, text="Stop", command=stop_generation, bg=BUTTON_BG_COLOR, fg="black", font=("Helvetica", 11, "bold"), activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_FG_COLOR, relief=FLAT, padx=20, pady=5, state=DISABLED)
stop_button.pack(side=RIGHT, padx=5)

status_frame = Frame(main_frame, bg=BACKGROUND_COLOR)
status_frame.pack(fill=X, pady=(10, 0))

root.mainloop()
