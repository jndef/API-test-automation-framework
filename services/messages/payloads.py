from dataclasses import dataclass

from faker import Faker
from pydantic import BaseModel, Field

from utils.data_helper import DataHelper

fake = Faker()


@dataclass
class CreateConversationByRoleTestCase:
    role: str
    payload: CreateConversationPayload
    participant_role: str = None


class CreateConversationPayload(BaseModel):
    participant_ids: list[str] = Field(default=[])
    is_group: bool = Field(default=False)
    name: str = Field(default=DataHelper().generate_text(15))


@dataclass
class CreateMessageByRoleTestCase:
    role: str
    participant_role: str
    payload: CreateMessagePayload


class CreateMessagePayload(BaseModel):
    content: str = None
    image_url: str | None = None


class Payloads:

    def create_conversation(self, participant_ids: list[str], name: str = None) -> dict:
        if name is None:
            name = "Test-" + DataHelper().generate_text(15)
        return {
            "participant_ids": participant_ids,
            "is_group": False,
            "name": name,
        }

    def create_message(self, content: str, image_url: str = None) -> dict:
        return {
            "content": content,
            "image_url": image_url
        }
