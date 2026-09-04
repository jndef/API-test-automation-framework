from dataclasses import dataclass
from typing import Literal, Union

from faker import Faker
from pydantic import BaseModel

ReactionsOptionsType = Union[Literal["like", "love", "laugh", "wow", "sad", "angry"], None, str]

fake = Faker()

class LikePostPayload(BaseModel):
    reaction: ReactionsOptionsType = None

class LikeCommentPayload(BaseModel):
    reaction: ReactionsOptionsType = None

@dataclass
class LikePostByRoleTestCase:
    role:str
    payload: LikePostPayload
    status_code: int = None
    expected_success: bool = True

@dataclass
class LikeCommentByRoleTestCase:
    role:str
    payload: LikeCommentPayload
    status_code: int = None
    expected_success: bool = True


class Payloads:

    def like_post(self, reaction: str=None) -> dict:
        payload = {}
        if reaction:
            return {
                "reaction": reaction,
            }
        return payload

    def like_comment(self, reaction: str=None) -> dict:
        payload = {}
        if reaction:
            return {
                "reaction": reaction,
            }
        return payload
