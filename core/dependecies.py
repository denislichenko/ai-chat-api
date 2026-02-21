from fastapi.params import Depends
from db.session import SessionLocal
from repositories.conversation_repository import ConversationRepository
from services.chat_service import ChatService
from services.document_ingestion_service import DocumentIngestionService
from services.embedding_service import EmbeddingService
from services.llm_service import LLMService
from services.qdrant_service import QdrantService


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_conversation_repository(db = Depends(get_db)):
    return ConversationRepository(db)

def get_llm_service():
    return LLMService()

def get_embedding_service():
    return EmbeddingService()

def get_qdrant_service():
    return QdrantService()

def get_ingestion_service(
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    qdrant_service: QdrantService = Depends(get_qdrant_service)
):
    return DocumentIngestionService(embedding_service, qdrant_service)

def get_chat_service(
    llm_service: LLMService = Depends(get_llm_service),
    conv_repo: ConversationRepository = Depends(get_conversation_repository),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    qdrant_service: QdrantService = Depends(get_qdrant_service)
):
    return ChatService(llm_service, conv_repo, embedding_service, qdrant_service)



