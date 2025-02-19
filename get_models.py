import subprocess

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

    

