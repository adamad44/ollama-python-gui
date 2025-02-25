import tkinter as tk
from tkinter import *
import threading
from utils import *
import os 

root = tk.Tk()
root.title("Local LLM")
root.geometry("800x800")

if not (os.path.exists(os.path.join(os.getcwd(), "images"))):
    os.mkdir(os.path.join(os.getcwd(), "images"))


def clearImages():
    for root_dir, dirs, files in os.walk(os.path.join(os.getcwd(), "images")):
        for file in files:
            try:
                os.remove(os.path.join(root_dir, file))
            except Exception as e:
                print("there was an error deleting image in the images folder. please delete manually")
clearImages()

models = get_models()


def generate(prompt, model):
    try:
        client = Client()
        stream = client.generate(model=model, prompt=prompt, stream=True)
        for chunk in stream:
            if 'response' in chunk:
                outputBox.insert(END, chunk['response'])
    except Exception as e:
        print(f"Error: {str(e)}")

def getMoreModels():
    exec(open("get_models.py").read())

def gen():
    try: 
        outputBox.delete(1.0, END)
        generate_button.config(state=DISABLED, text="Generating...", fg="green")   
        selected_model = model_selection.get()
        query = user_input.get("1.0", END)
        generate(query, selected_model)   
        
        generate_button.config(state=NORMAL, text="Generate", fg="black")
    except Exception as e:
        outputBox.insert(END, f"An error occurred: {e}")
        generate_button.config(state=NORMAL, text="Generate", fg="black")

    
def startThreadGen():
    threading.Thread(target=gen).start()


##################

size_label = Label(root, text=f"Total size of models: {get_size()} GB")
size_label.pack()

model_selection = StringVar()
model_selection.set(models[0])

model_selection_dropdown = OptionMenu(root, model_selection, *models)
model_selection_dropdown.pack()

user_input = Text(root, height=3, width= 80, font=("Helvetica", 11))
user_input.pack()


generate_button = Button(root, text="Generate", command=startThreadGen)
generate_button.pack()

outputBox = Text(root, height=30, width=80, font=("Helvetica", 11), wrap=WORD)
outputBox.pack()
##################




root.mainloop()
clearImages()