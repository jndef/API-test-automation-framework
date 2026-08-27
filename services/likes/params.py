from dataclasses import dataclass
from common.base_params import PaginationParams


@dataclass
class GetPostLikesByRoleTestCase:
    role: str
    params: GetPostLikesParams
    status_code: int = None
    expected_success: bool = True

@dataclass
class GetPostLikesParams(PaginationParams):
    ...