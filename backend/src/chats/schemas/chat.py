from typing import Optional
from pydantic import BaseModel, Field

from src.models.pyobjectid import PyObjectId
from ..models.chat import ChatMessageModel


class MessageSchema(BaseModel):
    temp_id: str = Field(...)
    content: str = Field(...)

class MessageResponseSchema(BaseModel):
    temp_id: str = Field(...)
    message: Optional[ChatMessageModel] = Field(default=None)

class FindNMessagesSchema(BaseModel):
    last_n_id: Optional[PyObjectId] = Field(default=None)
    n_messages: int = Field(...)

class FindNMessagesResSchema(BaseModel):
    messages: list[ChatMessageModel]