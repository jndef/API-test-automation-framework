from dataclasses import dataclass
from common.base_params import PaginationParams, ReadableParams


@dataclass(repr=False)
class GetFollowRequestsParams(PaginationParams, ReadableParams):
    ...


@dataclass(repr=False)
class GetFollowRequestsParamsByRoleTestCase(ReadableParams):
    role: str
    params: GetFollowRequestsParams
