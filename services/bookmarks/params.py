from dataclasses import dataclass
from common.base_params import PaginationParams, ReadableParams


class GetBookmarksQueryParams(PaginationParams, ReadableParams):
    ...


class GetBookmarksParams(PaginationParams, ReadableParams):
    ...


@dataclass(repr=False)
class GetBookmarksQueryParamsTestCaseByRole(ReadableParams):
    role: str
    params: GetBookmarksQueryParams

