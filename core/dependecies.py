from fastapi.params import Depends
from sqlalchemy.orm import Session

from db.session import SessionLocal
from repositories.conversation_repository import ConversationRepository
from services.chat_service import ChatService
from services.llm_service import LLMService


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

def get_chat_service(
    llm_service: LLMService = Depends(get_llm_service),
    conv_repo: ConversationRepository = Depends(get_conversation_repository)
):
    return ChatService(llm_service, conv_repo)



