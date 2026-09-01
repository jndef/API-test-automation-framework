from dataclasses import dataclass
from typing import Literal, Optional, Annotated
from common.base_params import PaginationParams, BaseParams

@dataclass
class GetBookmarksQueryParams(PaginationParams):
    ...

@dataclass
class GetBookmarksQueryParamsTestCaseByRole:
    role: str
    params: GetBookmarksQueryParams



@dataclass
class GetBookmarksParams(PaginationParams):
    ...