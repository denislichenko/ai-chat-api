from repositories.conversation_repository import ConversationRepository
from services.llm_service import LLMService


class ChatService:
    def __init__(self, llm_service: LLMService, conv_repo: ConversationRepository):
        self.llm = llm_service
        self.conv_repo = conv_repo

    async def handle_chat(self, user_id: str, conversation_id: str, message: str):
        if conversation_id:
            conv = self.conv_repo.get_conversation(conversation_id)
            if not conv:
                raise ValueError(f"Conversation with id {conversation_id} not found")
        else:
            conv = self.conv_repo.create_conversation(user_id)

        self.conv_repo.add_message(conv.id, role="user", content=message)

        messages = [
            {"role": m.role, "content": m.content}
            for m in self.conv_repo.get_messages(conv.id)
        ]

        result = await self.llm.chat(messages)

        self.conv_repo.add_message(conv.id, role="assistant", content=result["content"])

        return result