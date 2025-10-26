import torch
from transformers import AutoTokenizer, AutoModel
import penman
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
import logging

from src.config import cfg 

logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("penman").setLevel(logging.ERROR)
logging.getLogger("penman.codec").setLevel(logging.ERROR)


AMR_FILE = cfg.amr_path
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TARGET_CONCEPT = "bias"
TOP_N = 10

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

def encode(texts):
    """Encode text into embeddings with model"""
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.cpu().numpy()

def load_amr_concepts(file_path):
    """Extract all conceptin AMR graph."""
    text = Path(file_path).read_text(encoding="utf-8")
    graphs = penman.loads(text)
    concepts = []
    for g in graphs:
        for triple in g.triples:
            src, role, tgt = triple
            if role == ":instance":
                concepts.append(tgt)
    return list(set(concepts))

concepts = load_amr_concepts(AMR_FILE)
print(f"{len(concepts)} concepts extraits du fichier AMR.")

all_embeddings = encode(concepts)
bias_embedding = encode([TARGET_CONCEPT])

similarities = cosine_similarity(bias_embedding, all_embeddings)[0]

sorted_indices = np.argsort(similarities)[::-1]
print(f"\nNearest concept from '{TARGET_CONCEPT}':\n")
for idx in sorted_indices[:TOP_N]:
    print(f"{concepts[idx]:20s} | Similarity = {similarities[idx]:.4f}")
