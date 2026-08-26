from dataclasses import dataclass
from typing import Literal, Optional

from pydantic import BaseModel

@dataclass
class CreatePostTestCase:
    payload: CreatePostBodyParams
    status_code: int = 200
    expected_success: bool = True

@dataclass
class CreatePostByRoleTestCase:
    role: str
    payload: CreatePostBodyParams
    status_code: int = 201
    expected_success: bool = True



class CreatePostBodyParams(BaseModel):
    content: str = "A"
    visibility: str = "public"
    image_url: Optional[str] = None



@dataclass
class UpdatePostByRoleTestCase:
    role:str
    payload: UpdatePostBodyParams
    status_code: int = 200
    expected_success: bool = True

@dataclass
class UpdatePostTestCase:
    payload: UpdatePostBodyParams
    status_code: int = 200
    expected_success: bool = True


class UpdatePostBodyParams(BaseModel):
    content: str | int
    image_url: Optional[str] = None
    visibility: Optional[str] = None


@dataclass
class CreateRepostByRoleTestCase:
    role: str
    payload: CreateRepostParams
    status_code: int = 200
    expected_success: bool = True

@dataclass
class CreateRepostTestCase:
    payload: CreateRepostParams
    status_code: int = 200
    expected_success: bool = True


class CreateRepostParams(BaseModel):
    repost_type: Optional[str] = None
    content: str = None
