from dataclasses import dataclass
from typing import Literal, Optional, Union

from pydantic import BaseModel

from common.base_params import ReadableParams

RepostOptionsType = Union[Literal["repost", "quote"], None, str]


class CreatePostPayload(BaseModel, ReadableParams):
    content: str = "A"
    visibility: str = "public"
    image_url: Optional[str] = None


class UpdatePostPayload(BaseModel, ReadableParams):
    content: str | int
    image_url: Optional[str] = None
    visibility: Optional[str] = None


class CreateRepostPayload(BaseModel, ReadableParams):
    repost_type: RepostOptionsType = None
    content: str = None


@dataclass(repr=False)
class CreatePostByRoleTestCase(ReadableParams):
    role: str
    payload: CreatePostPayload


@dataclass(repr=False)
class UpdatePostByRoleTestCase(ReadableParams):
    role: str
    payload: UpdatePostPayload


@dataclass(repr=False)
class CreateRepostByRoleTestCase(ReadableParams):
    role: str
    payload: CreateRepostPayload
