from dataclasses import dataclass
from typing import Optional
from common.base_params import BaseParams, ReadableParams


@dataclass(repr=False)
class GetCommentsQueryParams(BaseParams, ReadableParams):
    sort_order: Optional[str] = None
    page: Optional[int] = None
    per_page: Optional[int] = None
    sort_by: Optional[str] = None


@dataclass(repr=False)
class GetCommentsByRoleTestCase(ReadableParams):
    role: str
    params: GetCommentsQueryParams


@dataclass(repr=False)
class GetRepliesQueryParams(BaseParams, ReadableParams):
    page: Optional[int] = None
    per_page: Optional[int] = None


@dataclass(repr=False)
class GetRepliesByRoleTestCase(ReadableParams):
    role: str
    params: GetRepliesQueryParams

# @dataclass
# class GetCommentsByRoleTestCase:
#     role:str

#
# @dataclass(repr=False)
# class GetCommentsParams(PaginationParams, SortParams):
#     post_id: Annotated[str, UUID4] = None
#     sort_by: Optional[Literal["created_at", "likes_count"]] = None
#
#
# @dataclass(repr=False)
# class GetRepliesParams(PaginationParams):
#     comment_id: Annotated[str, UUID4] = None
#     sort_by: Optional[Literal["created_at", "likes_count"]] = None
