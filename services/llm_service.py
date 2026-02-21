import httpx
from typing import List, Dict
from core.config import settings

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

class LLMService:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.MODEL_NAME
        self.temperature = settings.TEMPERATURE

        if not self.api_key:
            raise ValueError("Missing OpenRouter API key")

    async def chat(self, messages: List[Dict[str, str]]) -> Dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost",
            "X-Title": "ai-chat-api"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                OPENROUTER_URL,
                headers=headers,
                json=payload
            )

        if response.status_code != 200:
            raise Exception(f"LLM Error: {response.text}")

        data = response.json()

        return {
            "content": data["choices"][0]["message"]["content"],
            "usage": data.get("usage", {})
        }