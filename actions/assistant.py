import os

import httpx
import redis
import requests
from rasa_sdk import Tracker


REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
LLM_ASSISTANT_BAKCEND = os.getenv("LLM_ASSISTANT_BAKCEND")

r = redis.Redis(host='redis', port=6379, db=2, password=REDIS_PASSWORD)

class Assistant:
    def __init__(self, tracker: Tracker) -> None:
        self.tracker = tracker
        self.user_id = tracker.sender_id
        self.assistant_id = r.get(self.user_id)

    def get_or_create_assistant(self):
        if not self.assistant_id:
            
            data = {
                "user_id": self.user_id
            }
            response = requests.post(
                url=f"{LLM_ASSISTANT_BAKCEND}/assistants/create",
                json=data
            ).json()
            self.assistant_id = response["run_id"]
            r.set(self.user_id, self.assistant_id)

        return self.assistant_id

    async def chat(self, message):
        data = {
            "run_id": str(self.assistant_id),
            "user_id": self.user_id,
            "message": message
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=f"{LLM_ASSISTANT_BAKCEND}/assistants/chat",
                json=data,
                timeout=60
            )
            return str(response.text)