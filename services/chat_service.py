from repositories.conversation_repository import ConversationRepository
from services.embedding_service import EmbeddingService
from services.llm_service import LLMService
from services.qdrant_service import QdrantService


class ChatService:
    def __init__(
            self,
            llm_service: LLMService,
            conv_repo: ConversationRepository,
            embedding_service: EmbeddingService,
            qdrant_service: QdrantService):
        self.llm = llm_service
        self.conv_repo = conv_repo
        self.embedding = embedding_service
        self.qdrant = qdrant_service

    async def handle_chat(self, user_id: str, conversation_id: str, message: str):
        if conversation_id:
            conv = self.conv_repo.get_conversation(conversation_id)
            if not conv:
                raise ValueError(f"Conversation with id {conversation_id} not found")
        else:
            conv = self.conv_repo.create_conversation(user_id)

        self.conv_repo.add_message(conv.id, role="user", content=message)

        query_vector = self.embedding.embed(message)
        similar_docs = self.qdrant.search(query_vector, top_k=3)
        context_text = "\n\n".join([doc for doc, _ in similar_docs])

        history_messages = [
            {"role": m.role, "content": m.content}
            for m in self.conv_repo.get_messages(conv.id)
        ]

        messages = [
            {
                "role": "system",
                "content": f"Use the following context to answer the user:\n\n{context_text}"
            }
        ] + history_messages

        result = await self.llm.chat(messages)

        self.conv_repo.add_message(conv.id, role="assistant", content=result["content"])

        return {
            "conversation_id": conv.id,
            "content": result["content"],
            "usage": result["usage"]
        }
