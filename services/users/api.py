import mimetypes

import allure

from common.base_api import BaseAPI
from services.upload.api import data_helper
from services.users.endpoints import Endpoints
from services.users.models.model_profile_update import ResponseProfileUpdateModel
from services.users.models.model_profile_update_avatar import ResponseProfileAvatarUpdateModel
from services.users.models.model_user_followers import ResponseUserFollowersModel
from services.users.models.model_user_following import ResponseUserFollowingModel
from services.users.models.model_user_posts import ResponseUserPostsModel
from services.users.models.model_user_profile import ResponseUserProfileModel
from services.users.models.model_user_suggestions import ResponseUserModel
from services.users.models.model_users import ResponseUserItemsModel
from services.users.params import GetUsersParams, GetUserPostsParams, GetFollowersParams, GetFollowingParams
from services.users.payloads import UpdateMePayload
from config.headers import Headers


class UsersAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.headers = Headers()
        self.endpoints = Endpoints()

    def get_list_users(self, params: GetUsersParams, status_code: int = 200, expected_success: bool = True):
        with allure.step(f"API Request - Get Users list"):
            response =  self.request()\
                .set_url(self.endpoints.get_users)\
                .set_query_params(**(params.to_dict() if params else {}))\
                .set_headers(self.headers.basic)\
                .send("GET")
        return self.validate_response(response, ResponseUserItemsModel, status_code, expected_success)

    def get_user_suggestions(self, status_code: int = 200, expected_success: bool = True):
        with allure.step(f"API Request - Get Users Suggestions"):
            response =  self.request()\
                .set_url(self.endpoints.get_suggestions)\
                .set_headers(self.headers.basic)\
                .send("GET")
        return self.validate_response(response, ResponseUserModel, status_code, expected_success)

    def get_user_profile(self, username: str, status_code: int = 200, expected_success: bool = True):
        with allure.step(f"API Request - Get user Profile by username: {username}"):
            response =  self.request()\
                .set_url(self.endpoints.get_profile_by_username(username))\
                .set_headers(self.headers.basic)\
                .send("GET")
        return self.validate_response(response, ResponseUserProfileModel, status_code, expected_success)

    def update_profile(self, payload:UpdateMePayload, status_code: int = 200, expected_success: bool = True):
        with allure.step(f"API Request - Update Profile"):
            # self.reporter.attach_payload(payload)
            response =  self.request()\
                .set_url(self.endpoints.update_me)\
                .set_headers(self.headers.basic) \
                .set_request_body(payload.model_dump(exclude_none=True)) \
                .send("PATCH")
            self.reporter.attach_payload(payload)
            return self.validate_response(response, ResponseProfileUpdateModel, status_code, expected_success)

    def update_profile_avatar(self, image_name:str, status_code: int = 200, expected_success: bool = True):
        with allure.step(f"API Request - Update avatar by: {image_name}"):

            bin_file = data_helper.get_file_as_binary(image_name)
            content_type, _ = mimetypes.guess_type(image_name)
            response =  self.request()\
                .set_url(self.endpoints.update_avatar) \
                .set_headers(self.headers.basic) \
                .set_multipart_file(
                    file_name=image_name,
                    content_type=content_type,
                    file_content=bin_file,
                    )\
                .send("POST")
            return self.validate_response(response, ResponseProfileAvatarUpdateModel, status_code, expected_success)

    def delete_profile_avatar(self, status_code: int = 204, expected_success: bool = True):
        with allure.step(f"API Request - Remove profile avatar"):
            response =  self.request()\
                .set_url(self.endpoints.delete_avatar)\
                .set_headers(self.headers.basic) \
                .send("DELETE")
            return self.validate_response(response, None, status_code, expected_success)

    def get_user_posts(self, user_name:str, params:GetUserPostsParams=None, status_code: int = 200, expected_success: bool = True):
        with allure.step(f"API Request - Get posts of user by username: {user_name}"):
            response =  self.request()\
                .set_url(self.endpoints.get_user_posts(username=user_name))\
                .set_query_params(**(params.to_dict() if params else {}))\
                .set_headers(self.headers.basic)\
                .send("GET")
            return self.validate_response(response, ResponseUserPostsModel, status_code, expected_success)

    def get_user_followers(self, user_name:str, params:GetFollowersParams=None, status_code: int = 200, expected_success: bool = True):
        with allure.step(f"API Request - Get followers list of user: {user_name}"):
            response =  self.request()\
                .set_url(self.endpoints.get_user_followers(user_name))\
                .set_query_params(**(params.to_dict() if params else {}))\
                .set_headers(self.headers.basic)\
                .send("GET")
            return self.validate_response(response, ResponseUserFollowersModel, status_code, expected_success)


    def get_user_following(self, user_name:str, params:GetFollowingParams=None, status_code: int = 200, expected_success: bool = True):
        with allure.step(f"API Request - Get following list of user: {user_name}"):
            response =  self.request()\
                .set_url(self.endpoints.get_user_following(user_name))\
                .set_query_params(**(params.to_dict() if params else {}))\
                .set_headers(self.headers.basic)\
                .send("GET")
            return self.validate_response(response, ResponseUserFollowingModel, status_code, expected_success)
