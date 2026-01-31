import json
from datetime import datetime

FILE = "data/learning_logs.json"

def save_entry(entry):
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    entry["date"] = str(datetime.now())
    data.append(entry)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_entries():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []

