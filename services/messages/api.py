from common.base_api import BaseAPI
from config.headers import Headers
from services.messages.endpoints import Endpoints
from services.messages.models.model_conversation_create import ResponseCreateConversationModel
from services.messages.models.model_conversation_find_or_create import ResponseFindOrCreateConversationModel
from services.messages.models.model_conversation_get import ResponseGetConversationModel
from services.messages.models.model_conversation_list import ResponseConversationsListModel
from services.messages.models.model_conversation_message_create import ResponseCreateMessageModel
from services.messages.models.model_conversation_messages_list import ResponseGetMessagesListModel
from services.messages.params import GetConversationsListParams, GetConversationMessagesListParams
from services.messages.payloads import CreateConversationPayload, \
    CreateMessagePayload


class MessagesAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.headers = Headers()
        self.endpoints = Endpoints()

    def get_conversations_list(self, params: GetConversationsListParams, status_code: int = 200,
                               expected_success: bool = True):
        response = self.request() \
            .set_url(self.endpoints.get_conversations_list) \
            .set_query_params(**(params.to_dict() if params else {})) \
            .set_headers(self.headers.basic) \
            .send("GET")
        return self.validate_response(response, ResponseConversationsListModel, status_code=status_code,
                                      expected_success=expected_success)

    def create_conversation(self, payload: CreateConversationPayload, status_code: int = 201,
                            expected_success: bool = True):
        response = self.request() \
            .set_url(self.endpoints.create_conversation) \
            .set_headers(self.headers.basic) \
            .set_request_body(payload.model_dump(exclude_none=True)) \
            .send("POST")
        return self.validate_response(response, ResponseCreateConversationModel, status_code=status_code,
                                      expected_success=expected_success)

    def find_or_create_dm(self, username: str, status_code: int = 200, expected_success: bool = True):
        response = self.request() \
            .set_url(self.endpoints.find_or_create_dm(username)) \
            .set_headers(self.headers.basic) \
            .send("POST")
        return self.validate_response(response, ResponseFindOrCreateConversationModel, status_code=status_code,
                                      expected_success=expected_success)

    def get_conversation(self, conversation_id: str, status_code: int = 200, expected_success: bool = True):
        response = self.request() \
            .set_url(self.endpoints.get_conversation(conversation_id)) \
            .set_headers(self.headers.basic) \
            .send("GET")
        return self.validate_response(response, ResponseGetConversationModel, status_code=status_code,
                                      expected_success=expected_success)

    def get_conversation_messages(self, conversation_id: str, params: GetConversationMessagesListParams = None,
                                  status_code: int = 200,
                                  expected_success: bool = True):
        response = self.request() \
            .set_url(self.endpoints.get_conversation_messages(conversation_id)) \
            .set_headers(self.headers.basic) \
            .set_query_params(**(params.to_dict() if params else {})) \
            .send("GET")
        return self.validate_response(response, ResponseGetMessagesListModel, status_code=status_code,
                                      expected_success=expected_success)

    def send_message(self, conversation_id: str, payload: CreateMessagePayload, status_code: int = 201,
                     expected_success: bool = True):
        response = self.request() \
            .set_url(self.endpoints.create_messages(conversation_id)) \
            .set_headers(self.headers.basic) \
            .set_request_body(payload.model_dump(exclude_none=True)) \
            .send("POST")
        return self.validate_response(response, ResponseCreateMessageModel, status_code=status_code,
                                      expected_success=expected_success)

    def remove_message(self, message_id: str, status_code: int = 204, expected_success: bool = True):
        response = self.request() \
            .set_url(self.endpoints.remove_message(message_id)) \
            .set_headers(self.headers.basic) \
            .send("DELETE")
        return self.validate_response(response, None, status_code=status_code,
                                      expected_success=expected_success)

    def read_conversation(self, conversation_id: str, status_code: int = 204, expected_success: bool = True):
        response = self.request() \
            .set_url(self.endpoints.mark_conversation_read(conversation_id)) \
            .set_headers(self.headers.basic) \
            .send("POST")
        return self.validate_response(response, None, status_code=status_code,
                                      expected_success=expected_success)
