from typing import Generator, Optional, List, Dict, Any, Literal

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from phi.assistant import Assistant, AssistantRun
from ollama import Client
from pydantic import BaseModel

from ai.assistant import get_assistant
from ai.storage import combined_assistant_storage
from .schemas import (
    CreateRunRequest,
    CreateRunResponse,
    ChatRequest,
    ChatHistoryRequest,
    GetAssistantRunRequest
)
from .logger import logger
from .consts import OLLAMA_HOST, OLLAMA_MODEL

assistants_router = APIRouter(prefix="/assistants", tags=["Assistants"])

@assistants_router.post("/load-knowledge-base")
def load_knowledge_base():
    """Loads the knowledge base for an Assistant"""

    assistant = get_assistant()
    if assistant.knowledge_base:
        assistant.knowledge_base.load(recreate=False)
    return {"message": "Knowledge Base Loaded"}


@assistants_router.post("/pull-model")
def pull_model():
    """Pull ollama model for Assistant"""

    ollama_client = Client(host=OLLAMA_HOST)
    response = ollama_client.pull(OLLAMA_MODEL)
    return response


@assistants_router.post("/create", response_model=CreateRunResponse)
def create_assistant_run(body: CreateRunRequest):
    """Create a new Assistant run and returns the run_id"""

    logger.debug(f"CreateRunRequest: {body}")
    assistant: Assistant = get_assistant(user_id=body.user_id)

    run_id: Optional[str] = assistant.create_run()
    if run_id is None:
        raise HTTPException(status_code=500, detail="Failed to create assistant run")
    logger.debug(f"Created Assistant Run: {run_id}")

    return CreateRunResponse(
        run_id=run_id,
        user_id=assistant.user_id,
        chat_history=assistant.memory.get_chat_history(),
    )


@assistants_router.post("/chat")
def chat(body: ChatRequest):
    """Sends a message to an Assistant and returns the response"""

    logger.debug(f"ChatRequest: {body}")
    assistant: Assistant = get_assistant(
        run_id=body.run_id, user_id=body.user_id
    )
    return assistant.run(body.message, stream=False)


@assistants_router.post("/history", response_model=List[Dict[str, Any]])
def get_chat_history(body: ChatHistoryRequest):
    """Return the chat history for an Assistant run"""

    logger.debug(f"ChatHistoryRequest: {body}")
    assistant: Assistant = get_assistant(
        run_id=body.run_id, user_id=body.user_id
    )
    assistant.read_from_storage()
    return assistant.memory.get_chat_history()


@assistants_router.post("/get", response_model=Optional[AssistantRun])
def get_assistant_run(body: GetAssistantRunRequest):
    """Returns the Assistant run"""

    logger.debug(f"GetAssistantRunRequest: {body}")
    assistant: Assistant = get_assistant(
        run_id=body.run_id, user_id=body.user_id
    )
    return assistant.read_from_storage()