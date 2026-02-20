from sqlalchemy.orm import Session
from db.models import Conversation, Message

class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_conversation(self, conversation_id: str):
        conv = self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
        return conv

    def create_conversation(self, user_id: str) -> Conversation:
        conv = Conversation(user_id=user_id)
        self.db.add(conv)
        self.db.commit()
        self.db.refresh(conv)
        return conv

    def add_message(self, conversation_id: int, role: str, content: str):
        msg = Message(conversation_id=conversation_id, role=role, content=content)
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg

    def get_messages(self, conversation_id: int):
        conv = self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
        return conv.messages if conv else []