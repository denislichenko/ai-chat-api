import uuid
from services.chunking import chunk_text
from services.embedding_service import EmbeddingService
from services.qdrant_service import QdrantService


class DocumentIngestionService:
    def __init__(
            self,
            embedding_service: EmbeddingService,
            qdrant_service: QdrantService
    ):
        self.embedding = embedding_service
        self.qdrant = qdrant_service

    def ingest_text(self, text: str, source: str):
        chunks = chunk_text(text)

        for chunk in chunks:
            vector = self.embedding.embed(chunk)

            self.qdrant.add_document(
                text=chunk,
                vector=vector,
                metadata={
                    "source": source,
                    "chunk_id": str(uuid.uuid4())
                }
            )