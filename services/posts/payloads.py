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


class Payloads:

    def create_post(self, content: str, visibility: str, image_url: str = None):
        return {
            "content": content,
            "image_url": image_url,
            "visibility": visibility
        }

    def update_post(self, content: str, visibility: str = None, image_url: str = None):
        payload = {}
        if content:
            payload["content"] = f"{content}"
        if visibility:
            payload["visibility"] = f"{visibility}"
        if image_url:
            payload["image_url"] = f"{image_url}"
        return payload

    def create_repost(self, repost_type: str = None, content: str = None):
        payload = {}
        if repost_type:
            payload["repost_type"] = f"{repost_type}"
        if content:
            payload["content"] = content

        return payload
