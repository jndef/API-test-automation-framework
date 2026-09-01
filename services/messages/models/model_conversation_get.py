from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import BaseModel, UUID4


class ResponseUserModel(BaseModel):
    id: Annotated[str, UUID4]
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    is_verified: bool


class ResponseMessageModel(BaseModel):
    id: Annotated[str, UUID4]
    conversation_id: Annotated[str, UUID4]
    sender: ResponseUserModel
    content: str
    image_url: Optional[str] = None
    is_deleted: bool
    created_at: datetime


class ResponseGetConversationModel(BaseModel):
    id: Annotated[str, UUID4]
    is_group: bool
    name: str | None
    participants: List[ResponseUserModel] = []
    last_message: Optional[ResponseMessageModel] = None
    unread_count: int
    created_at: datetime
    updated_at: datetime