from pydantic import UUID4

from dataclasses import dataclass
from typing import Literal, Optional, Annotated
from common.base_params import PaginationParams, SortParams, BaseParams


@dataclass
class GetPostsParams(PaginationParams, SortParams):
    hashtag: Optional[str] = None
    author_id: Optional[Annotated[str, UUID4]] = None
    sort_by: str = None


@dataclass
class GetFeedParams(PaginationParams):
    ...


@dataclass
class DeletePostParams(BaseParams):
    reason: Optional[str] = None


@dataclass
class GetPostsByRoleTestCase:
    role: str
    params: GetPostsParams
    status_code: int = 200
    expected_success: bool = True


@dataclass
class GetFeedByRoleTestCase:
    role: str
    params: GetFeedParams
    status_code: int = 200
    expected_success: bool = True


@dataclass
class DeletePostByRoleTestCase:
    role: str
    params: DeletePostParams
    status_code: int = 200
    expected_success: bool = True
