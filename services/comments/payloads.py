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
    payload: CreateCommentBodyQuery
    status_code: int = 200
    expected_success: bool = True

@dataclass
class CreateCommentTestCase:
    payload: CreateCommentBodyQuery
    status_code: int = 200
    expected_success: bool = True

class CreateCommentBodyQuery(BaseModel):
    content: str | int = None

class CreateCommentBody(BaseModel):
    content: str

@dataclass
class UpdateCommentByRoleTestCase:
    role:str
    payload: UpdateCommentBodyQuery
    status_code: int = 200
    expected_success: bool = True

@dataclass
class UpdateCommentTestCase:
    payload: UpdateCommentBodyQuery
    status_code: int = 200
    expected_success: bool = True

class UpdateCommentBodyQuery(BaseModel):
    content: str | int = None

class UpdateCommentBody(BaseModel):
    content: str

@dataclass
class DeleteCommentByRoleTestCase:
    role: str
    params: DeleteCommentParams
    status_code: int = 204
    expected_success: bool = True

@dataclass
class DeleteCommentTestCase:
    params: DeleteCommentParams
    status_code: int = 204
    expected_success: bool = True

@dataclass
class DeleteCommentParams(BaseParams):
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
