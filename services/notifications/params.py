from dataclasses import dataclass

from common.base_params import PaginationParams, ReadableParams


@dataclass(repr=False)
class GetNotificationsParams(PaginationParams, ReadableParams):
    is_read:bool = None



@dataclass(repr=False)
class GetNotificationsParamsByRoleTestCase(ReadableParams):
    role: str
    params: GetNotificationsParams
