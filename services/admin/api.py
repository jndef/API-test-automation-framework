import allure
from common.base_api import BaseAPI
from config.headers import Headers
from services.admin.endpoints import Endpoints
from services.admin.models.model_get_stats import ResponseStatisticsModel
from services.admin.models.model_posts_list import ResponseAdminPostsListModel
from services.admin.models.model_users_list import ResponseUsersListModel
from services.admin.models.model_users_update_user import ResponseUpdateUserByAdminModel
from services.admin.params import AdminGetAllUsersParams, AdminDeletePostParams
from services.admin.payloads import UpdateUserByAdminPayload


class AdminAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.headers = Headers()
        self.endpoints = Endpoints()

    def get_stats(self, status_code: int = 200, expected_success: bool = True):
        with allure.step(f"API Request - get stats by admin"):
            response = self.request() \
                .set_url(self.endpoints.get_stats) \
                .set_headers(self.headers.basic) \
                .send("GET")
            return self.validate_response(response, ResponseStatisticsModel, status_code, expected_success)

    def get_list_all_users(self, search_query=None, params: AdminGetAllUsersParams = None, status_code: int = 200,
                           expected_success: bool = True):
        with allure.step(f"API Request - get all users list with query params ({params}) by admin"):
            response = self.request() \
                .set_url(self.endpoints.get_list_users_all(search_query)) \
                .set_query_params(**(params.to_dict() if params else {})) \
                .set_headers(self.headers.basic) \
                .send("GET")
            return self.validate_response(response, ResponseUsersListModel, status_code, expected_success)

    def update_user_by_admin(self, user_id: str, payload: UpdateUserByAdminPayload = None, status_code: int = 200,
                             expected_success: bool = True):
        with allure.step(f"API PATCH Request - update certain user ({user_id}) using data ({payload}) by admin"):
            response = self.request() \
                .set_url(self.endpoints.update_user_by_admin(user_id)) \
                .set_request_body(payload.model_dump(exclude_none=True)) \
                .set_headers(self.headers.basic) \
                .send("PATCH")
            return self.validate_response(response, ResponseUpdateUserByAdminModel, status_code, expected_success)

    def deactivate_user_by_admin(self, user_id: str, status_code: int = 204, expected_success: bool = True):
        with allure.step(f"API DELETE Request - deactivate certain user ({user_id}) by admin"):
            response = self.request() \
                .set_url(self.endpoints.deactivate_user_by_admin(user_id)) \
                .set_headers(self.headers.basic) \
                .send("DELETE")
            return self.validate_response(response, None, status_code, expected_success)

    def get_list_all_posts(self, params: AdminGetAllUsersParams = None, status_code: int = 200,
                           expected_success: bool = True):
        with allure.step(f"API Request - get all posts list with query params ({params}) by admin"):
            response = self.request() \
                .set_url(self.endpoints.get_list_posts_all) \
                .set_query_params(**(params.to_dict() if params else {})) \
                .set_headers(self.headers.basic) \
                .send("GET")
            return self.validate_response(response, ResponseAdminPostsListModel, status_code, expected_success)

    def remove_post_by_admin(self, post_id: str, params: AdminDeletePostParams = None, status_code: int = 204,
                             expected_success: bool = True):
        with allure.step(f"API DELETE Request - moderate remove certain post ({post_id}) by admin"):
            response = self.request() \
                .set_url(self.endpoints.remove_post_by_admin(post_id)) \
                .set_query_params(**(params.to_dict() if params else {})) \
                .set_headers(self.headers.basic) \
                .send("DELETE")
            return self.validate_response(response, None, status_code, expected_success)
