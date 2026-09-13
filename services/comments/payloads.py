from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(repr=False)
class CreateCommentPayload(BaseModel):
    content: str | int = None


@dataclass(repr=False)
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
