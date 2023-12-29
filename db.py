import json

def add_file(file):
    with open("storage.json", "r") as f:
        data = json.load(f)
    data.append(file)
    with open("storage.json", "w") as f:
        json.dump(data, f)

