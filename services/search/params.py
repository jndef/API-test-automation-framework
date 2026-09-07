from dataclasses import dataclass
from typing import Union, Literal

from common.base_params import PaginationParams, ReadableParams, BaseParams

PeriodType = Union[Literal["week", "day"], None, str]


@dataclass(repr=False)
class SearchUsersParams(PaginationParams, ReadableParams):
    ...


@dataclass(repr=False)
class SearchUsersParamsByRoleTestCase(ReadableParams):
    role: str
    params: SearchUsersParams
    searched_user_alias: str = None


@dataclass(repr=False)
class SearchPostsParams(PaginationParams, ReadableParams):
    ...


@dataclass(repr=False)
class SearchPostsParamsByRoleTestCase(ReadableParams):
    role: str
    params: SearchPostsParams
    searched_post_info: str = None


@dataclass(repr=False)
class SearchHashtagsParams(PaginationParams, ReadableParams):
    ...


@dataclass(repr=False)
class SearchHashtagsParamsByRoleTestCase(ReadableParams):
    role: str
    params: SearchHashtagsParams
    searched_hashtag: str = None


@dataclass(repr=False)
class SearchTrendingParams(BaseParams, ReadableParams):
    period: PeriodType = None
    limit: int = None


@dataclass(repr=False)
class SearchTrendingParamsByRoleTestCase(ReadableParams):
    role: str
    params: SearchTrendingParams
