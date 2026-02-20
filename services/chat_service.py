from services.llm_service import LLMService


class ChatService:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    async def handle_chat(self, message: str):
        messages = [
            {"role": "user", "content": message},
        ]
        return await self.llm.chat(messages)