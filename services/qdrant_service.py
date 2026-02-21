from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

class QdrantService:
    def __init__(self):
        self.client = QdrantClient(host="qdrant", port=6333)
        self.collection_name = "documents"
        self._ensure_collection()

    def _ensure_collection(self):
        if self.collection_name not in [c.name for c in self.client.get_collections().collections]:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )

    def add_document(self, text: str, vector: list[float], metadata: dict):
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "text": text,
                        **metadata
                    }
                )
            ]
        )

    def search(self, vector: list[float], top_k: int = 3):
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=top_k
        )

        return [
            (point.payload["text"], point.score)
            for point in results.points
        ]