import allure

from common.base_api import BaseAPI
from config.headers import Headers
from services.comments.endpoints import Endpoints
from services.comments.models.model_comment_create import ResponseCommentCreateModel
from services.comments.models.model_comment_update import ResponseCommentUpdateModel
from services.comments.models.model_comments_list import ResponseCommentsModel
from services.comments.models.model_reply_create import ResponseCreateReplyModel
from services.comments.params import GetCommentsParams, GetRepliesParams, GetCommentsQueryParams, GetRepliesQueryParams
from services.comments.payloads import  CreateCommentPayload, UpdateCommentPayloadQuery


class CommentsAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        # self.payloads = Payloads()
        self.headers = Headers()
        self.endpoints = Endpoints()

    def get_list_comments(self, post_id:str, params: GetCommentsQueryParams = None, status_code: int = 200, expected_success: bool = True):
        with allure.step(f"API Request - get list of comments to post ({post_id})"):
            response =  self.request()\
                .set_url(self.endpoints.get_list_comments(post_id))\
                .set_query_params(**(params.to_dict() if params else {}))\
                .set_headers(self.headers.basic)\
                .send("GET")
            return self.validate_response(response, ResponseCommentsModel,status_code=status_code, expected_success=expected_success)

    def create_comment(self, post_id:str, payload: CreateCommentPayload, status_code: int = 201, expected_success: bool = True):
        with allure.step(f"API POST Request - create comment to post ({post_id})"):
            response =  self.request()\
                .set_url(self.endpoints.create_comment(post_id)) \
                .set_headers(self.headers.basic) \
                .set_request_body(payload.model_dump(exclude_none=True))\
                .send("POST")
            return self.validate_response(response, ResponseCommentCreateModel, status_code=status_code, expected_success=expected_success)


    def update_comment(self, comment_id:str,  payload: UpdateCommentPayloadQuery, status_code: int = 200, expected_success: bool = True):
        with allure.step(f"API PATCH Request - updated comment({comment_id})"):
            response =  self.request()\
                .set_url(self.endpoints.update_comment(comment_id)) \
                .set_headers(self.headers.basic) \
                .set_request_body(payload.model_dump(exclude_none=True))\
                .send("PATCH")
            return self.validate_response(response, ResponseCommentUpdateModel, status_code=status_code, expected_success=expected_success)

    def delete_comment(self, comment_id:str,  status_code: int = 204, expected_success: bool = True):
        with allure.step(f"API DELETE Request - remove comment({comment_id})"):
            response =  self.request()\
                .set_url(self.endpoints.delete_comment(comment_id)) \
                .set_headers(self.headers.basic) \
                .send("DELETE")
            return self.validate_response(response, None, status_code=status_code, expected_success=expected_success)

    def get_list_replies(self, comment_id:str, params: GetRepliesQueryParams = None, status_code: int = 200, expected_success: bool = True):
        with allure.step(f"API Request - get list of replies to comment ({comment_id})"):
            response =  self.request()\
                .set_url(self.endpoints.get_list_replies(comment_id))\
                .set_query_params(**(params.to_dict() if params else {}))\
                .set_headers(self.headers.basic)\
                .send("GET")
            return self.validate_response(response, ResponseCommentsModel,status_code=status_code, expected_success=expected_success)

    def create_reply(self, comment_id:str, payload: CreateCommentPayload, status_code: int = 201, expected_success: bool = True):
        with allure.step(f"API POST Request - create reply to comment({comment_id})"):
            response =  self.request()\
                .set_url(self.endpoints.create_reply(comment_id)) \
                .set_headers(self.headers.basic) \
                .set_request_body(payload.model_dump(exclude_none=True))\
                .send("POST")
            return self.validate_response(response, ResponseCreateReplyModel, status_code=status_code, expected_success=expected_success)
