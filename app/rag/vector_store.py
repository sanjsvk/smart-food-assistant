import chromadb
from chromadb.config import Settings
from typing import List

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client(
            Settings(persist_directory="data/embeddings")
        )
        self.collection = self.client.get_or_create_collection(
            name="food_logs"
        )

    def add_document(self, doc_id: str, text: str, metadata: dict):
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )

    def query(self, query_text: str, n_results: int = 3) -> List[dict]:
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        return [
            {
                "text": doc,
                "metadata": meta
            }
            for doc, meta in zip(documents, metadatas)
        ]