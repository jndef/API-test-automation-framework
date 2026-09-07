from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import BaseModel, UUID4, Field


class ResponseUserModel(BaseModel):
    id: Annotated[str, UUID4]
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    is_verified: bool


class ResponseHashtagModel(BaseModel):
    id: Annotated[str, UUID4]
    name: str
    posts_count: int = Field(ge=0)


class ResponsePostModel(BaseModel):
    id: Annotated[str, UUID4]
    author: ResponseUserModel
    content: str
    image_url: Optional[str] = None
    is_pinned: bool
    is_deleted: bool
    parent_id: Optional[Annotated[str, UUID4]] = None
    repost_type: str | None
    visibility: str
    likes_count: int = Field(ge=0)
    comments_count: int = Field(ge=0)
    reposts_count: int = Field(ge=0)
    hashtags: List[ResponseHashtagModel] = []
    created_at: datetime
    updated_at: datetime
    is_liked: bool
    is_bookmarked: bool
    user_reaction: Optional[str] = None


class ResponseSearchPostsModel(BaseModel):
    items: List[ResponsePostModel]
    total: int = Field(ge=0)
    page: int = Field(ge=1)
    per_page: int = Field(ge=1)
    pages: int = Field(ge=0)
