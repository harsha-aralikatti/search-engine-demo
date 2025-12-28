# src/core/embeddings.py

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")   # 384 dims

def generate_local_embedding(text: str) -> list:
    embedding = model.encode(text)
    return embedding.tolist()
