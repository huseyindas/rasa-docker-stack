import logging
from typing import Any, Text, Dict, List

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher


class ActionLLM(Action):
    def name(self) -> Text:
        return "action_llm"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        try:
            data = {
                "model": "llama3.1",
                "prompt": tracker.latest_message.get("text"),
                "stream": False
            }
            response = requests.post(
                url="http://ollama:11434/api/generate",
                json=data
            ).json()
            dispatcher.utter_message(response["response"])
        except Exception as ex:
            logging.warn(ex)
            dispatcher.utter_message("The Llama model is currently unable to respond. Try later.")

        return [UserUtteranceReverted()]