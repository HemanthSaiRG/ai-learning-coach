import json
from pathlib import Path
import numpy as np

try:
    import faiss
    from sentence_transformers import SentenceTransformer
    FAISS_AVAILABLE = True
except:
    FAISS_AVAILABLE = False

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

INDEX_FILE = DATA_DIR / "memory.index"
DATA_FILE = DATA_DIR / "memory.json"

DIM = 384

if FAISS_AVAILABLE:
    MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    INDEX = faiss.IndexFlatL2(DIM)
else:
    MODEL = None
    INDEX = None

def embed(text):
    if not FAISS_AVAILABLE:
        return None
    return MODEL.encode([text])[0]

def load_data():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text())
        except:
            return []
    return []

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))

def add_memory(text, meta):
    data = load_data()

    entry = {
        "text": text,
        "meta": meta
    }
    data.append(entry)
    save_data(data)

    if FAISS_AVAILABLE:
        vector = np.array([embed(text)]).astype("float32")
        INDEX.add(vector)
        faiss.write_index(INDEX, str(INDEX_FILE))

def search_memory(query, k=3):
    data = load_data()

    if not FAISS_AVAILABLE or not INDEX_FILE.exists():
        return data[-k:]

    index = faiss.read_index(str(INDEX_FILE))
    vector = np.array([embed(query)]).astype("float32")
    _, ids = index.search(vector, k)

    return [data[i] for i in ids[0] if i < len(data)]

def load_memory():
    return load_data()
