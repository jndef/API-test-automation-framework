import allure
from common.base_api import BaseAPI
from config.headers import Headers
from services.follows.endpoints import Endpoints
from services.follows.models.model_follow_requests import ResponseFollowersListModel
from services.follows.models.model_follow_user import ResponseFollowRequestModel
from services.follows.models.model_follow_request_accept import ResponseFollowRequestModel
from services.follows.params import GetFollowRequestsParams


class FollowsAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.headers = Headers()
        self.endpoints = Endpoints()

    def follow_user(self, user_name, status_code: int = 201, expected_success: bool = True):
        with allure.step(f"API POST Request - follow user: {user_name}"):
            response = self.request() \
                .set_url(self.endpoints.follow_user(user_name)) \
                .set_headers(self.headers.basic) \
                .send("POST")
            return self.validate_response(response, ResponseFollowRequestModel, status_code, expected_success)

    def unfollow_user(self, user_name, status_code: int = 204, expected_success: bool = True):
        with allure.step(f"API DELETE Request - unfollow user: {user_name}"):
            response = self.request() \
                .set_url(self.endpoints.unfollow_user(user_name)) \
                .set_headers(self.headers.basic) \
                .send("DELETE")
            return self.validate_response(response, None, status_code, expected_success)

    def get_follow_requests(self, params: GetFollowRequestsParams = None, status_code: int = 200,
                            expected_success: bool = True):
        with allure.step(f"API Request - get follow request list"):
            response = self.request() \
                .set_url(self.endpoints.get_follow_req) \
                .set_query_params(**(params.to_dict() if params else {})) \
                .set_headers(self.headers.basic) \
                .send("GET")
            return self.validate_response(response, ResponseFollowersListModel, status_code, expected_success)

    def accept_follow_request(self, follow_id: str, status_code: int = 200, expected_success: bool = True):
        with allure.step(f"API POST Request - accept follow request: {follow_id}"):
            response = self.request() \
                .set_url(self.endpoints.accept_follow_req(follow_id)) \
                .set_headers(self.headers.basic) \
                .send("POST")
            return self.validate_response(response, ResponseFollowRequestModel, status_code, expected_success)

    def reject_follow_request(self, follow_id: str, status_code: int = 204, expected_success: bool = True):
        with allure.step(f"API POST Request - reject follow request: {follow_id}"):
            response = self.request() \
                .set_url(self.endpoints.reject_follow_req(follow_id)) \
                .set_headers(self.headers.basic) \
                .send("POST")
            return self.validate_response(response, None, status_code, expected_success)
