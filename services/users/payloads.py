from dataclasses import dataclass
from pydantic import BaseModel

from common.base_params import ReadableParams


class UpdateMePayload(BaseModel, ReadableParams):
    display_name: str | None = None
    bio: str | None = None
    is_private: bool = None


class UpdateAvatarFilePayload(BaseModel, ReadableParams):
    file_name: str


@dataclass(repr=False)
class UpdateMePayloadByRoleTestCase(ReadableParams):
    role: str
    payload: UpdateMePayload


@dataclass(repr=False)
class UpdateAvatarByRoleTestCase(ReadableParams):
    role: str
    file: UpdateAvatarFilePayload
