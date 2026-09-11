from dataclasses import dataclass
from typing import Union, Literal, Optional

from common.base_params import PaginationParams, ReadableParams, SortParams, BaseParams

RoleOptions = Union[Literal["admin", "moderator", "user"], None, str]
SortByAdminOptions = Union[Literal["created_at", "username", "email"], None, str]


@dataclass(repr=False)
class AdminGetAllUsersParams(PaginationParams, SortParams, ReadableParams):
    role: RoleOptions = None
    is_active: bool | None = None
    sort_by: SortByAdminOptions = None


@dataclass(repr=False)
class AdminGetAllUsersParamsByRoleTestCase(ReadableParams):
    role: str
    params: AdminGetAllUsersParams
    search_query: str = None


@dataclass(repr=False)
class AdminGetAllPostsParams(PaginationParams, ReadableParams):
    is_deleted: bool | None = None


@dataclass(repr=False)
class AdminGetAllPostsParamsByRoleTestCase(ReadableParams):
    role: str
    params: AdminGetAllPostsParams


class AdminDeletePostParams(BaseParams, ReadableParams):
    reason: Optional[str] = None


@dataclass(repr=False)
class AdminDeletePostParamsByRoleTestCase(ReadableParams):
    role: str
    params: AdminDeletePostParams
