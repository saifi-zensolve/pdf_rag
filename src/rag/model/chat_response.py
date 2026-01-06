from pydantic import BaseModel


class ChatResponse(BaseModel):
    answer: str
    history: list[dict]
    session_id: str
