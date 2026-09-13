from dataclasses import dataclass
from typing import Optional
from common.base_params import BaseParams, ReadableParams


class GetCommentsQueryParams(BaseParams, ReadableParams):
    sort_order: Optional[str] = None
    page: Optional[int] = None
    per_page: Optional[int] = None
    sort_by: Optional[str] = None


class GetRepliesQueryParams(BaseParams, ReadableParams):
    page: Optional[int] = None
    per_page: Optional[int] = None


@dataclass(repr=False)
class GetCommentsByRoleTestCase(ReadableParams):
    role: str
    params: GetCommentsQueryParams


@dataclass(repr=False)
class GetRepliesByRoleTestCase(ReadableParams):
    role: str
    params: GetRepliesQueryParams
