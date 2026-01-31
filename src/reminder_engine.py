import json
import os
from datetime import datetime

def load_reminders(user_dir):
    path = os.path.join(user_dir, "reminders.json")
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return []

def save_reminder(user_dir, text, date):
    path = os.path.join(user_dir, "reminders.json")
    reminders = load_reminders(user_dir)
    reminders.append({
        "text": text,
        "date": date,
        "done": False
    })
    with open(path, "w") as f:
        json.dump(reminders, f, indent=2)
