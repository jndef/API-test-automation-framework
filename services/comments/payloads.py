from dataclasses import dataclass
from pydantic import BaseModel


class CreateCommentPayload(BaseModel):
    content: str | int = None


class UpdateCommentPayload(BaseModel):
    content: str | int = None


@dataclass(repr=False)
class CreateCommentByRoleTestCase:
    role: str
    payload: CreateCommentPayload


@dataclass(repr=False)
class UpdateCommentByRoleTestCase:
    role: str
    payload: UpdateCommentPayload
