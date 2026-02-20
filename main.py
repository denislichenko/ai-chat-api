from http.client import HTTPException
from typing import Optional

from fastapi import FastAPI
from fastapi.params import Depends
from pydantic import BaseModel
from core.dependecies import get_chat_service
from services.chat_service import ChatService

app = FastAPI()


class ChatRequest(BaseModel):
    user_id: str
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    tokens_used: dict

@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)):
    try:
        result = await chat_service.handle_chat(
            request.user_id,
            request.conversation_id,
            request.message)
        return ChatResponse(
            answer=result["content"],
            tokens_used=result["usage"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))