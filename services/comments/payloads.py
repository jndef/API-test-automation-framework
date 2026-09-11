from dataclasses import dataclass
from pydantic import BaseModel


class CreateCommentPayload(BaseModel):
    content: str | int = None


@dataclass
class CreateCommentByRoleTestCase:
    role: str
    payload: CreateCommentPayload


class UpdateCommentPayload(BaseModel):
    content: str | int = None


@dataclass
class UpdateCommentByRoleTestCase:
    role: str
    payload: UpdateCommentPayload
