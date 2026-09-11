from dataclasses import dataclass

from faker import Faker
from pydantic import BaseModel, Field

from common.base_params import ReadableParams
from utils.data_helper import DataHelper

fake = Faker()


class CreateConversationPayload(BaseModel, ReadableParams):
    participant_ids: list[str] = Field(default=[])
    is_group: bool = Field(default=False)
    name: str = Field(default=DataHelper().generate_text(15))


@dataclass(repr=False)
class CreateConversationByRoleTestCase(ReadableParams):
    role: str
    payload: CreateConversationPayload
    participant_role: str = None


@dataclass(repr=False)
class CreateMessageByRoleTestCase(ReadableParams):
    role: str
    participant_role: str
    payload: CreateMessagePayload


class CreateMessagePayload(BaseModel, ReadableParams):
    content: str = None
    image_url: str | None = None
