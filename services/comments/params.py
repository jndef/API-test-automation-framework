from pydantic import UUID4



# users/params.py
from dataclasses import dataclass
from typing import Literal, Optional, Annotated
from common.base_params import PaginationParams, SortParams, BaseParams

@dataclass
class GetCommentsQueryParams(BaseParams):
    sort_order: Optional[str] = None
    page: Optional[int] = None
    per_page: Optional[int] = None
    sort_by: Optional[str] = None

@dataclass
class GetCommentsByRoleTestCase:
    role: str
    params: GetCommentsQueryParams
    status_code: int = 200
    expected_success: bool = True


@dataclass
class GetRepliesQueryParams(BaseParams):
    page: Optional[int] = None
    per_page: Optional[int] = None


@dataclass
class GetRepliesByRoleTestCase:
    role: str
    params: GetRepliesQueryParams
    status_code: int = 200
    expected_success: bool = True

# @dataclass
# class GetCommentsByRoleTestCase:
#     role:str



@dataclass
class GetCommentsParams(PaginationParams, SortParams):
    post_id: Annotated[str, UUID4] = None
    sort_by: Optional[Literal["created_at", "likes_count"]] = None


@dataclass
class GetRepliesParams(PaginationParams):
    comment_id : Annotated[str, UUID4] = None
    sort_by: Optional[Literal["created_at", "likes_count"]] = None
