from dataclasses import dataclass
from typing import Union, Literal

from pydantic import BaseModel

from common.base_params import ReadableParams

RoleType = Union[Literal["user", "moderator", "admin"], None, str]

@dataclass(repr=False)
class UpdateUserByAdminPayload(BaseModel, ReadableParams):
    role: RoleType = None
    is_active: bool | None = None
    is_verified: bool | None = None


@dataclass(repr=False)
class UpdateUserByAdminPayloadByRoleTestCase(ReadableParams):
    case_role: str
    payload: UpdateUserByAdminPayload
    updated_user: str = None
