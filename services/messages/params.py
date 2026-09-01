from dataclasses import dataclass
from common.base_params import PaginationParams


@dataclass
class GetConversationsListParamsByRoleTestCase:
    role: str
    params: GetConversationsListParams


@dataclass
class GetConversationMessagesListParamsByRoleTestCase:
    role: str
    params: GetConversationMessagesListParams


@dataclass
class GetConversationsListParams(PaginationParams):
    ...


@dataclass
class GetConversationMessagesListParams(PaginationParams):
    ...
