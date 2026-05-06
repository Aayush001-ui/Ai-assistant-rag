import os
import numpy as np
import faiss
from pypdf import PdfReader

from embedding_model import EmbeddingModel
from config import CHUNK_SIZE

class RAGEngine:
    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.index = None
        self.chunks = []

    def load_pdf(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        full_text = ""

        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

        return full_text

    def split_text(self, text: str) -> list[str]:
        chunks = []
        start = 0

        while start < len(text):
            end = start + CHUNK_SIZE
            chunk = text[start:end]
            chunks.append(chunk)
            start = end

        return chunks

    def build_index(self, document_path: str):
        print("Loading document...")
        text = self.load_pdf(document_path)

        print("Splitting text...")
        self.chunks = self.split_text(text)

        print("Generating embeddings...")
        embeddings = self.embedding_model.embed_batch(self.chunks)

        dimension = embeddings.shape[1]

        print("Creating FAISS index...")
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

        print(f"Index built with {len(self.chunks)} chunks.")

    def search(self, query: str, top_k: int = 3) -> list[str]:
        if self.index is None:
            raise ValueError("Index not built yet")

        query_vector = self.embedding_model.embed_text(query)
        query_vector = np.array([query_vector])

        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.chunks):
                results.append(self.chunks[idx])

        return results