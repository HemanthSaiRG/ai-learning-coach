import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

DATA_FILE = DATA_DIR / "memory.json"

def load_memory():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text())
        except:
            return []
    return []

def add_memory(text, meta):
    data = load_memory()

    entry = {
        "text": text,
        "meta": meta,
        "time": datetime.now().isoformat()
    }

    data.append(entry)
    DATA_FILE.write_text(json.dumps(data, indent=2))
