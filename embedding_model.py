from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def embed_text(self, text: str) -> np.ndarray:
        embedding = self.model.encode(text)
        return np.array(embedding, dtype='float32')

    def embed_batch(self, texts: list[str]) -> np.ndarray:
        embeddings = self.model.encode(texts)
        return np.array(embeddings, dtype='float32')