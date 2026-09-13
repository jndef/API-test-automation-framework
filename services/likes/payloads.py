from dataclasses import dataclass
from typing import Literal, Union

from faker import Faker
from pydantic import BaseModel

from common.base_params import ReadableParams

ReactionsOptionsType = Union[Literal["like", "love", "laugh", "wow", "sad", "angry"], None, str]

fake = Faker()

@dataclass(repr=False)
class LikePostPayload(BaseModel, ReadableParams):
    reaction: ReactionsOptionsType = None

@dataclass(repr=False)
class LikeCommentPayload(BaseModel, ReadableParams):
    reaction: ReactionsOptionsType = None


@dataclass(repr=False)
class LikePostByRoleTestCase(ReadableParams):
    role: str
    payload: LikePostPayload


@dataclass(repr=False)
class LikeCommentByRoleTestCase(ReadableParams):
    role: str
    payload: LikeCommentPayload
