import requests

from common.base_api import BaseAPI
from config.headers import Headers
from services.likes.endpoints import Endpoints
from services.likes.models.model_comment_add_like import ResponseCommentReactionModel
from services.likes.models.model_post_add_like import ResponsePostReactionModel
from services.likes.models.model_post_likes_list import ResponsePostReactionsListModel
from services.likes.params import GetPostLikesParams
from services.likes.payloads import LikePostPayload, LikeCommentPayload
from utils.logger import logger


class LikesAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        # self.payloads = Payloads()
        self.headers = Headers()
        self.endpoints = Endpoints()

    def like_post(self, post_id:str, payload: LikePostPayload, status_code: int = 201, expected_success: bool = True):
        logger.info(f"Sending POST request to {self.endpoints.like_post(post_id)}")
        response =  self.request()\
            .set_url(self.endpoints.like_post(post_id))\
            .set_request_body(payload.model_dump(exclude_none=True))\
            .set_headers(self.headers.basic)\
            .send("POST")
        logger.debug(f"Received response: {response.json()}")
        return self.validate_response(response, ResponsePostReactionModel, status_code=status_code, expected_success=expected_success)



    def unlike_post(self, post_id:str, status_code: int = 204, expected_success: bool = True):
        response =  self.request()\
            .set_url(self.endpoints.unlike_post(post_id))\
            .set_headers(self.headers.basic)\
            .send("DELETE")
        return self.validate_response(response, None, status_code=status_code, expected_success=expected_success)

    def get_post_likes(self, post_id:str, params: GetPostLikesParams, status_code: int = 200, expected_success: bool = True):
        response =  self.request()\
            .set_url(self.endpoints.get_post_likes(post_id))\
            .set_query_params(**(params.to_dict() if params else {}))\
            .set_headers(self.headers.basic)\
            .send("GET")
        return self.validate_response(response, ResponsePostReactionsListModel, status_code=status_code, expected_success=expected_success)


    def like_comment(self, comment_id:str,  payload: LikeCommentPayload,  status_code: int = 201, expected_success: bool = True):
        logger.info(f"Sending POST request to {self.endpoints.like_post(comment_id)}")
        response =  self.request()\
            .set_url(self.endpoints.like_comment(comment_id)) \
            .set_headers(self.headers.basic) \
            .set_request_body(payload.model_dump(exclude_none=True))\
            .send("POST")
        logger.debug(f"Received response: {response.json()}")
        return self.validate_response(response, ResponseCommentReactionModel, status_code=status_code, expected_success=expected_success)


    def unlike_comment(self, comment_id:str, status_code: int = 204, expected_success: bool = True):
        response =  self.request()\
            .set_url(self.endpoints.unlike_comment(comment_id))\
            .set_headers(self.headers.basic)\
            .send("DELETE")
        return self.validate_response(response, None, status_code=status_code, expected_success=expected_success)
