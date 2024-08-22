import logging
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from .assistant import Assistant

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
            assistant = Assistant(tracker=tracker)
            _ = assistant.get_or_create_assistant()

            response = await assistant.chat(
                message=tracker.latest_message.get("text")
            )

            dispatcher.utter_message(response)
            return [UserUtteranceReverted()]
        except Exception as ex:
            logging.warn(ex)
            dispatcher.utter_message("The chatbot is currently unable to respond. Try later.")
            return []
