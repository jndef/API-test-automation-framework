import requests

from common.base_api import BaseAPI
from services.users.endpoints import Endpoints
from services.users.models.model_profile_update import ResponseProfileUpdateModel
from services.users.models.model_profile_update_avatar import ResponseProfileAvatarUpdateModel
from services.users.models.model_user_followers import ResponseUserFollowersModel
from services.users.models.model_user_following import ResponseUserFollowingModel
from services.users.models.model_user_posts import ResponseUserPostsModel
from services.users.models.model_user_profile import ResponseUserProfileModel
from services.users.models.model_user_suggestions import ResponseUserModel
from services.users.models.model_users import ResponseUserItemsModel
from services.users.params import GetUsersParams, GetUserPostsParams
from common.base_params import BaseParams, PaginationParams
from utils.helper import Helper
from services.users.payloads import Payloads
from config.headers import Headers


class UsersAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.headers = Headers()
        self.endpoints = Endpoints()


    def get_list_users(self, params: GetUsersParams = None, status_code: int = 200, expected_success: bool = True):
        response =  self.request()\
            .set_url(self.endpoints.get_users) \
            .set_headers(self.headers.basic) \
            .set_query_params(params.to_dict() if params else {})\
            .send("GET")

        return self.validate_response(response, ResponseUserItemsModel, status_code, expected_success)

    def get_user_suggestions(self, status_code: int = 200, expected_success: bool = True):
        response = requests.get(
            url=self.endpoints.get_suggestions,
            headers=self.headers.basic,
        )
        return self.validate_response(response, ResponseUserModel, status_code, expected_success)

    def get_user_profile(self, username: str, status_code: int = 200, expected_success: bool = True):
        response = requests.get(
            url=self.endpoints.get_profile_by_username(username),
            headers=self.headers.basic,
        )
        return self.validate_response(response, ResponseUserProfileModel, status_code, expected_success)

    def update_profile(self, display_name: str = None, bio: str = None, is_private: bool = None,
                       status_code: int = 200, expected_success: bool = True):
        response = requests.patch(
            url=self.endpoints.update_me,
            json=self.payloads.update_me(display_name, bio, is_private),
            headers=self.headers.basic
        )
        return self.validate_response(response, ResponseProfileUpdateModel, status_code, expected_success)

    def update_profile_avatar(self, file_name_with_ext:str, image_type:str="image/jpeg", status_code: int = 200, expected_success: bool = True):
        response = requests.post(

            url=self.endpoints.update_avatar,
            files={
                "file": (f"{file_name_with_ext}", open(f"temp_data/{file_name_with_ext}", "rb"), f"{image_type}")
            },
            headers=self.headers.basic,
        )
        return self.validate_response(response, ResponseProfileAvatarUpdateModel, status_code, expected_success)

    def delete_profile_avatar(self, status_code: int = 204, expected_success: bool = True):
        response = requests.delete(
            url=self.endpoints.delete_avatar,
            headers=self.headers.basic,
        )
        return self.validate_response(response, None, status_code, expected_success)

    def get_user_posts(self, username:str, params:dict=None, status_code: int = 200, expected_success: bool = True):
        response = requests.get(
            url=self.endpoints.get_user_posts(username),
            params= GetUserPostsParams(**(params or {})).to_dict(),
            headers = self.headers.basic

        )
        return self.validate_response(response, ResponseUserPostsModel, status_code, expected_success)

    def get_user_followers(self, username:str, params:dict=None, status_code: int = 200, expected_success: bool = True):
        response = requests.get(
            url=self.endpoints.get_user_followers(username),
            params=params,
            headers = self.headers.basic,
        )
        return self.validate_response(response, ResponseUserFollowersModel, status_code, expected_success)


    def get_user_following(self, username:str, params:dict=None, status_code: int = 200, expected_success: bool = True):
        response = requests.get(
            url=self.endpoints.get_user_following(username),
            params=params,
            headers=self.headers.basic,
        )
        return self.validate_response(response, ResponseUserFollowingModel, status_code, expected_success)
