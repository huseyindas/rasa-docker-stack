from typing import Optional, List, Dict, Any

from pydantic import BaseModel


class CreateRunRequest(BaseModel):
    user_id: Optional[str] = None


class CreateRunResponse(BaseModel):
    run_id: str
    user_id: Optional[str] = None
    chat_history: List[Dict[str, Any]]


class ChatRequest(BaseModel):
    message: str
    run_id: Optional[str] = None
    user_id: Optional[str] = None


class ChatHistoryRequest(BaseModel):
    run_id: str
    user_id: Optional[str] = None


class GetAssistantRunRequest(BaseModel):
    run_id: str
    user_id: Optional[str] = None
