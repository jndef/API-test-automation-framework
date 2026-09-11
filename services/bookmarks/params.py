from dataclasses import dataclass
from common.base_params import PaginationParams, ReadableParams


@dataclass(repr=False)
class GetBookmarksQueryParams(PaginationParams, ReadableParams):
    ...


@dataclass(repr=False)
class GetBookmarksQueryParamsTestCaseByRole(ReadableParams):
    role: str
    params: GetBookmarksQueryParams


@dataclass(repr=False)
class GetBookmarksParams(PaginationParams, ReadableParams):
    ...
