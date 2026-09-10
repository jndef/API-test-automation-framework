from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, UUID4


class ResponseUpdateUserByAdminModel(BaseModel):
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
    followers_count: int
    following_count: int
    posts_count: int
    is_following: bool
    is_followed_by: bool
