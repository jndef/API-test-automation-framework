from dataclasses import dataclass
from common.base_params import PaginationParams, ReadableParams


class GetConversationsListParams(PaginationParams, ReadableParams):
    ...


class GetConversationMessagesListParams(PaginationParams, ReadableParams):
    ...


@dataclass(repr=False)
class GetConversationsListParamsByRoleTestCase(ReadableParams):
    role: str
    params: GetConversationsListParams


@dataclass(repr=False)
class GetConversationMessagesListParamsByRoleTestCase(ReadableParams):
    role: str
    params: GetConversationMessagesListParams
