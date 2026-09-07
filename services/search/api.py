import allure
from common.base_api import BaseAPI
from config.headers import Headers
from services.search.endpoints import Endpoints
from services.search.models.model_search_hashtags_list import ResponseHashtagsModel
from services.search.models.model_search_posts_list import ResponseSearchPostsModel
from services.search.models.model_search_trendings_list import ResponseTrendingHashtagModel
from services.search.models.model_search_users_list import ResponseSearchUsersModel
from services.search.params import SearchUsersParams, SearchHashtagsParams, SearchTrendingParams


class SearchAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.headers = Headers()
        self.endpoints = Endpoints()

    def search_users(self, search_query, params: SearchUsersParams = None, status_code: int = 200,
                     expected_success: bool = True):
        with allure.step(f"API Request - get users list by search query({search_query})"):
            response = self.request() \
                .set_url(self.endpoints.search_users(search_query)) \
                .set_query_params(**(params.to_dict() if params else {})) \
                .set_headers(self.headers.basic) \
                .send("GET")
            return self.validate_response(response, ResponseSearchUsersModel, status_code, expected_success)

    def search_posts(self, search_query, params: SearchUsersParams = None, status_code: int = 200,
                     expected_success: bool = True):
        with allure.step(f"API Request - get posts list by search query({search_query})"):
            response = self.request() \
                .set_url(self.endpoints.search_posts(search_query)) \
                .set_query_params(**(params.to_dict() if params else {})) \
                .set_headers(self.headers.basic) \
                .send("GET")
            return self.validate_response(response, ResponseSearchPostsModel, status_code, expected_success)

    def search_hashtags(self, search_query, params: SearchHashtagsParams = None, status_code: int = 200,
                        expected_success: bool = True):
        with allure.step(f"API Request - get hashtags  list by search query({search_query})"):
            response = self.request() \
                .set_url(self.endpoints.search_hashtags(search_query)) \
                .set_query_params(**(params.to_dict() if params else {})) \
                .set_headers(self.headers.basic) \
                .send("GET")
            return self.validate_response(response, ResponseHashtagsModel, status_code, expected_success)

    def search_trending(self, params: SearchTrendingParams = None, status_code: int = 200,
                        expected_success: bool = True):
        with allure.step(f"API Request - get trending hashtags list with params({params})"):
            response = self.request() \
                .set_url(self.endpoints.search_trending) \
                .set_query_params(**(params.to_dict() if params else {})) \
                .set_headers(self.headers.basic) \
                .send("GET")
            return self.validate_response(response, ResponseTrendingHashtagModel, status_code, expected_success)
