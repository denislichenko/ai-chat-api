import logging
from typing import Optional

from fastapi import FastAPI, UploadFile
from fastapi import HTTPException
from fastapi.params import Depends, File
from pydantic import BaseModel
from core.dependecies import get_chat_service, get_ingestion_service
from db.models import Base
from db.session import engine
from services.chat_service import ChatService
from services.document_ingestion_service import DocumentIngestionService

app = FastAPI()
logger = logging.getLogger(__name__)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


class ChatRequest(BaseModel):
    user_id: str
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    tokens_used: dict

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    ingestion_service: DocumentIngestionService = Depends(get_ingestion_service)
):
    content = await file.read()
    text = content.decode("utf-8")
    ingestion_service.ingest_text(
        text=text,
        source=file.filename
    )

    return {"status": "indexed"}



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
        logger.exception("Chat endpoint failed")
        raise HTTPException(status_code=500, detail=str(e))
