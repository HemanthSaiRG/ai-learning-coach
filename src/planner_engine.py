import json
from datetime import datetime, timedelta
import os

def load_progress(user_dir):
    path = os.path.join(user_dir, "subjects.json")
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return []

def generate_plan(user_dir, available_minutes=60):
    progress = load_progress(user_dir)
    today = datetime.now().date()

    # find weak topics (studied only once)
    freq = {}
    for p in progress:
        freq[p["topic"]] = freq.get(p["topic"], 0) + 1

    weak = [t for t, c in freq.items() if c == 1]
    strong = [t for t, c in freq.items() if c > 1]

    plan = []

    if weak:
        plan.append({"task": f"Revise: {weak[0]}", "minutes": 30})
    if strong:
        plan.append({"task": f"Practice: {strong[0]}", "minutes": 20})

    plan.append({"task": "Read new topic from syllabus", "minutes": 10})

    return plan
