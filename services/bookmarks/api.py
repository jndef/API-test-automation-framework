from common.base_api import BaseAPI
from config.headers import Headers
from services.bookmarks.endpoints import Endpoints
from services.bookmarks.models.model_bookmark_list import ResponseBookmarksModel
from services.bookmarks.params import GetBookmarksParams


class BookmarksAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        # self.payloads = Payloads()
        self.headers = Headers()
        self.endpoints = Endpoints()

    def get_bookmarks(self, params: GetBookmarksParams, status_code: int = 200, expected_success: bool = True):
        response =  self.request()\
            .set_url(self.endpoints.get_bookmarks_list)\
            .set_query_params(**(params.to_dict() if params else {}))\
            .set_headers(self.headers.basic)\
            .send("GET")
        return self.validate_response(response, ResponseBookmarksModel, status_code=status_code,
                                      expected_success=expected_success)

    def bookmark_post(self, post_id: str, status_code: int = 201, expected_success: bool = True):
        response =  self.request()\
            .set_url(self.endpoints.bookmark_post(post_id))\
            .set_headers(self.headers.basic)\
            .send("POST")
        return self.validate_response(response, None, status_code=status_code, expected_success=expected_success)

    def remove_bookmark(self, post_id: str, status_code: int = 204, expected_success: bool = True):
        response =  self.request()\
            .set_url(self.endpoints.unbookmark_post(post_id))\
            .set_headers(self.headers.basic)\
            .send("DELETE")
        return self.validate_response(response, None, status_code=status_code, expected_success=expected_success)
