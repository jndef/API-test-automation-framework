from pydantic import UUID4

from dataclasses import dataclass
from typing import Optional, Annotated
from common.base_params import PaginationParams, SortParams, BaseParams, ReadableParams


class GetFeedParams(PaginationParams, ReadableParams):
    ...


class DeletePostParams(BaseParams, ReadableParams):
    reason: Optional[str] = None


@dataclass(repr=False)
class GetPostsParams(PaginationParams, SortParams, ReadableParams):
    hashtag: Optional[str] = None
    author_id: Optional[Annotated[str, UUID4]] = None
    sort_by: str = None


@dataclass(repr=False)
class GetPostsByRoleTestCase(ReadableParams):
    role: str
    params: GetPostsParams


@dataclass(repr=False)
class GetFeedByRoleTestCase(ReadableParams):
    role: str
    params: GetFeedParams


@dataclass(repr=False)
class DeletePostByRoleTestCase(ReadableParams):
    role: str
    params: DeletePostParams
