from fastapi.params import Depends
from services.chat_service import ChatService
from services.llm_service import LLMService


def get_llm_service():
    return LLMService()

def get_chat_service(
    llm_service: LLMService = Depends(get_llm_service)
):
    return ChatService(llm_service)
