from faker import Faker

fake = Faker()

from dataclasses import dataclass
from typing import Optional
from common.base_params import PaginationParams, SortParams, ReadableParams, SortByParam

@dataclass(repr=False)
class GetUsersParams(PaginationParams, SortParams, SortByParam, ReadableParams):
    search: Optional[str] = None

@dataclass(repr=False)
class GetUserPostsParams(PaginationParams, ReadableParams):
    ...

@dataclass(repr=False)
class GetFollowersParams(PaginationParams, ReadableParams):
    ...

@dataclass(repr=False)
class GetFollowingParams(PaginationParams, ReadableParams):
    ...


@dataclass(repr=False)
class GetUsersParamsByRoleTestCase(ReadableParams):
    role: str
    params: GetUsersParams


@dataclass(repr=False)
class GetUserPostsParamsByRoleTestCase(ReadableParams):
    role: str
    params: GetUserPostsParams
    requested_user: str = None


@dataclass(repr=False)
class GetFollowersParamsByRoleTestCase(ReadableParams):
    role: str
    params: GetFollowersParams
    requested_user: str = None


@dataclass(repr=False)
class GetFollowingParamsByRoleTestCase(ReadableParams):
    role: str
    params: GetFollowingParams = None
    requested_user: str = None
