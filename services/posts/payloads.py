from dataclasses import dataclass
from typing import Literal, Optional, Union

from pydantic import BaseModel


RepostOptionsType = Union[Literal["repost", "quote"], None, str]

class CreatePostPayload(BaseModel):
    content: str = "A"
    visibility: str = "public"
    image_url: Optional[str] = None

@dataclass
class CreatePostByRoleTestCase:
    role: str
    payload: CreatePostPayload
    status_code: int = None
    expected_success: bool = True



class UpdatePostPayload(BaseModel):
    content: str | int
    image_url: Optional[str] = None
    visibility: Optional[str] = None

@dataclass
class UpdatePostByRoleTestCase:
    role:str
    payload: UpdatePostPayload
    status_code: int = None
    expected_success: bool = True


class CreateRepostPayload(BaseModel):
    repost_type: RepostOptionsType = None
    content: str = None


@dataclass
class CreateRepostByRoleTestCase:
    role: str
    payload: CreateRepostPayload
    status_code: int = None
    expected_success: bool = True


