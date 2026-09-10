from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import BaseModel, UUID4, Field


class ResponseUserModel(BaseModel):
    id: Annotated[str, UUID4]
    email: str
    username: str
    display_name: str
    bio: str
    avatar_url: Optional[str] = None
    cover_url: Optional[str] = None
    role: str
    is_active: bool
    is_verified: bool
    is_private: bool
    created_at: datetime
    updated_at: datetime
    followers_count: int = Field(ge=0)
    following_count: int = Field(ge=0)
    posts_count: int = Field(ge=0)
    is_following: bool
    is_followed_by: bool


class ResponseUsersListModel(BaseModel):
    items: List[ResponseUserModel]
    total: int = Field(ge=0)
    page: int = Field(ge=0)
    per_page: int = Field(ge=0)
    pages: int = Field(ge=0)
