from typing import Optional, Literal
from bson import ObjectId
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from src.models.pyobjectid import PyObjectId


class MessageAuthor(BaseModel):
    author_id: PyObjectId = Field(default=None)
    author_type: Literal["user", "assistant"] = Field(...)


class ChatMessageModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    author: MessageAuthor = Field(...)
    content: str = Field(default="")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
        json_encoders = {ObjectId: str}


class ChatModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId = Field(...)
    assistant_id: Optional[PyObjectId] = Field(default=None)
    messages: list[ChatMessageModel] = Field(default=[])
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
        json_encoders = {ObjectId: str}
