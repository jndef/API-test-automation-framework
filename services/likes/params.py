from dataclasses import dataclass
from common.base_params import PaginationParams, ReadableParams


class GetPostLikesParams(PaginationParams, ReadableParams):
    ...

@dataclass(repr=False)
class GetPostLikesByRoleTestCase(ReadableParams):
    role: str
    params: GetPostLikesParams
    status_code: int = None
    expected_success: bool = True

