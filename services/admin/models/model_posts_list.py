from datetime import datetime
from typing import Annotated, List, Optional, Literal

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
    content: str = Field(min_length=1, max_length=2000)
    image_url: Optional[str] = None
    is_pinned: bool
    is_deleted: bool
    parent_id: Optional[Annotated[str, UUID4]]
    repost_type: Optional[Literal["repost", "quote"]] = None
    visibility: Literal["public", "followers_only"]
    likes_count: int
    comments_count: int
    reposts_count: int
    hashtags: List[ResponseHashtagModel] = []
    created_at: datetime
    updated_at: datetime
    is_liked: bool
    is_bookmarked: bool
    user_reaction: Optional[str] = None


class ResponseAdminPostsListModel(BaseModel):
    items: List[ResponsePostModel]
    total: int = Field(ge=0)
    page: int = Field(ge=0)
    per_page: int = Field(ge=0)
    pages: int = Field(ge=0)
