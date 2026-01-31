import json
import os

def calculate_readiness(user_dir):
    path = os.path.join(user_dir, "subjects.json")
    try:
        with open(path, "r") as f:
            subjects = json.load(f)
    except:
        return 0

    if not subjects:
        return 0

    studied = len(subjects)
    unique_topics = len(set([s["topic"] for s in subjects]))
    score = int((unique_topics / max(studied, 1)) * 100)

    return min(score, 100)
