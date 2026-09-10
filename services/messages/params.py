from dataclasses import dataclass
from common.base_params import PaginationParams, ReadableParams


@dataclass(repr=False)
class GetConversationsListParamsByRoleTestCase(ReadableParams):
    role: str
    params: GetConversationsListParams


@dataclass(repr=False)
class GetConversationMessagesListParamsByRoleTestCase(ReadableParams):
    role: str
    params: GetConversationMessagesListParams


@dataclass(repr=False)
class GetConversationsListParams(PaginationParams,ReadableParams):
    ...


@dataclass(repr=False)
class GetConversationMessagesListParams(PaginationParams,ReadableParams):
    ...
