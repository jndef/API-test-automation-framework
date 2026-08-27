from dataclasses import dataclass

from faker import Faker
from pydantic import BaseModel

fake = Faker()

@dataclass
class LikePostByRoleTestCase:
    role:str
    payload: LikePostPayload
    status_code: int = None
    expected_success: bool = True

class LikePostPayload(BaseModel):
    reaction: str = None

@dataclass
class LikeCommentByRoleTestCase:
    role:str
    payload: LikeCommentPayload
    status_code: int = None
    expected_success: bool = True

class LikeCommentPayload(BaseModel):
    reaction: str | int = None


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
