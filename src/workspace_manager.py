import os
import json

BASE_DIR = "data/users"
os.makedirs(BASE_DIR, exist_ok=True)

def init_user(username):
    user_dir = os.path.join(BASE_DIR, username)
    os.makedirs(user_dir, exist_ok=True)

    files = {
        "learning_logs.json": [],
        "subjects.json": [],
        "analytics.json": {}
    }

    for file, default in files.items():
        path = os.path.join(user_dir, file)
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump(default, f, indent=2)

    return user_dir
