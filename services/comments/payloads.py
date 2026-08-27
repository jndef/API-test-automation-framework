from dataclasses import dataclass
from typing import Optional

from dotenv.variables import Literal
from faker import Faker
from pydantic import BaseModel

from common.base_params import BaseParams

fake = Faker()

@dataclass
class CreateCommentByRoleTestCase:
    role:str
    payload: CreateCommentPayloadQuery
    status_code: int = 200
    expected_success: bool = True

@dataclass
class CreateCommentTestCase:
    payload: CreateCommentPayloadQuery
    status_code: int = 200
    expected_success: bool = True

class CreateCommentPayloadQuery(BaseModel):
    content: str | int = None

class CreateCommentBody(BaseModel):
    content: str

@dataclass
class UpdateCommentByRoleTestCase:
    role:str
    payload: UpdateCommentPayloadQuery
    status_code: int = 200
    expected_success: bool = True

@dataclass
class UpdateCommentTestCase:
    payload: UpdateCommentPayloadQuery
    status_code: int = 200
    expected_success: bool = True

class UpdateCommentPayloadQuery(BaseModel):
    content: str | int = None

class UpdateCommentBody(BaseModel):
    content: str

@dataclass
class DeleteCommentByRoleTestCase:
    role: str
    params: DeleteCommentPayload
    status_code: int = 204
    expected_success: bool = True

@dataclass
class DeleteCommentTestCase:
    params: DeleteCommentPayload
    status_code: int = 204
    expected_success: bool = True

@dataclass
class DeleteCommentPayload(BaseParams):
    reason: Optional[str] = None


class Payloads:

    def create_comment(self, content: str=None) -> dict:
        payload = {}
        if content:
            return {
                "content": content,
            }
        return payload

    def update_comment(self, content: str=None) -> dict:
        payload = {}
        if content:
            return {
                "content": content,
            }
        return payload


    def create_reply(self, content: str=None) -> dict:
        payload = {}
        if content:
            return {
                "content": content,
            }
        return payload
