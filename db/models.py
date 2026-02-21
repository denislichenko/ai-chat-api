import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String) # user or assistant
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    conversation = relationship("Conversation", back_populates="messages")
