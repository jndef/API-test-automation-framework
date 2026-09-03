from dataclasses import dataclass

from faker import Faker
from pydantic import BaseModel, Field

from common.base_params import ReadableParams

fake = Faker()

class UpdateMePayload(BaseModel, ReadableParams):
    display_name: str | None = None
    bio: str | None = None
    is_private: bool = None


@dataclass(repr=False)
class UpdateMePayloadByRoleTestCase(ReadableParams):
    role: str
    payload: UpdateMePayload

class UpdateAvatarFilePayload(BaseModel, ReadableParams):
    file_name: str

@dataclass(repr=False)
class UpdateAvatarByRoleTestCase(ReadableParams):
    role: str
    file: UpdateAvatarFilePayload




class Payloads:

    def update_me(self, display_name: str, bio: str, is_private:bool):
        return {"display_name": display_name,
                "bio": bio,
                "is_private": is_private
                }

    def update_avatar(self, file_path: str):
        return {
            "file": f"{file_path}"
        }