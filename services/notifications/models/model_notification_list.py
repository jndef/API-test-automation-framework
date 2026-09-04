from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import BaseModel, UUID4, Field


class ResponseUserModel(BaseModel):
    id: Annotated[str, UUID4]
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    is_verified: bool


class ResponseNotificationModel(BaseModel):
    id: Annotated[str, UUID4]
    actor: ResponseUserModel
    type: str
    target_type: Optional[str] = None
    target_id: Optional[Annotated[str, UUID4]] = None
    is_read: bool
    created_at: datetime


class ResponseNotificationsModel(BaseModel):
    items: List[ResponseNotificationModel]
    total: int= Field(ge=0)
    page: int= Field(ge=1)
    per_page: int = Field(ge=1)
    pages: int = Field(ge=0)