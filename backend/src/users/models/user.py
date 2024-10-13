from bson import ObjectId
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from src.models.pyobjectid import PyObjectId


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hevy_user_id: str = Field(...)
    username: str = Field(...)
    email: str = Field(...)
    sex: str = Field(...)
    birthday: str = Field(...)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
        json_encoders = {ObjectId: str}
