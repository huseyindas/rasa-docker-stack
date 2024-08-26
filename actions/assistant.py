import os

import httpx
from rasa_sdk import Tracker


REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
LANGCHAIN_ASSISTANT_BAKCEND = os.getenv("LANGCHAIN_ASSISTANT_BAKCEND", "http://backend:8000")

class Assistant:
    def __init__(self, tracker: Tracker) -> None:
        self.tracker = tracker
        self.user_id = tracker.sender_id

    async def chat(self, message):
        data = {
            "message": message
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=f"{LANGCHAIN_ASSISTANT_BAKCEND}/bot/chat",
                json=data,
                timeout=60
            )
            return str(response.text)