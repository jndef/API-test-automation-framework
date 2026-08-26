from common.base_api import BaseAPI
from config.headers import Headers
from services.posts.endpoints import Endpoints
from services.posts.models.model_post import ResponsePostModel
from services.posts.models.model_post_create import ResponseCreatePostModel
from services.posts.models.model_post_update import ResponsePostUpdateModel
from services.posts.models.model_posts_feed import ResponsePostsFeedModel
from services.posts.models.model_posts_list import ResponsePostsModel
from services.posts.params import GetPostsParams, GetFeedParams, DeletePostParams
from services.posts.payloads import CreatePostBodyParams, UpdatePostBodyParams, CreateRepostParams


class PostsAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        # self.payloads = Payloads()
        self.headers = Headers()
        self.endpoints = Endpoints()

    def get_list_posts(self, params: GetPostsParams = None, status_code: int = 200, expected_success: bool = True):
        response =  self.request()\
            .set_url(self.endpoints.get_list_posts)\
            .set_query_params(**(params.to_dict() if params else {}))\
            .set_headers(self.headers.basic)\
            .send("GET")

        return self.validate_response(response, ResponsePostsModel,status_code=status_code, expected_success=expected_success)


    def create_post(self, payload: CreatePostBodyParams, status_code: int = 201, expected_success: bool = True):
        response =  self.request()\
            .set_url(self.endpoints.create_post) \
            .set_headers(self.headers.basic) \
            .set_request_body(payload.model_dump(exclude_none=True))\
            .send("POST")

        return self.validate_response(response, ResponseCreatePostModel, status_code=status_code, expected_success=expected_success)

    def get_posts_feed(self, params: GetFeedParams = None, status_code: int = 200, expected_success: bool = True):
        response =  self.request()\
            .set_url(self.endpoints.get_feed)\
            .set_query_params(**(params.to_dict() if params else {}))\
            .set_headers(self.headers.basic)\
            .send("GET")

        return self.validate_response(response, ResponsePostsFeedModel, status_code=status_code, expected_success=expected_success)

    def get_post(self, post_id:str, status_code: int = 200, expected_success: bool = True):
        response =  self.request()\
            .set_url(self.endpoints.get_post(post_id))\
            .set_headers(self.headers.basic)\
            .send("GET")

        return self.validate_response(response, ResponsePostModel, status_code=status_code, expected_success=expected_success)

    def update_post(self, post_id:str,  payload: UpdatePostBodyParams, status_code: int = 200, expected_success: bool = True):
        response =  self.request()\
            .set_url(self.endpoints.update_post(post_id)) \
            .set_headers(self.headers.basic) \
            .set_request_body(payload.model_dump(exclude_none=True))\
            .send("PATCH")

        return self.validate_response(response, ResponsePostUpdateModel, status_code=status_code, expected_success=expected_success)

    def delete_post(self, post_id:str, params: DeletePostParams = None, status_code: int = 204, expected_success: bool = True):
        response =  self.request()\
            .set_url(self.endpoints.delete_post(post_id)) \
            .set_query_params(**(params.to_dict() if params else {})) \
            .set_headers(self.headers.basic) \
            .send("DELETE")

        return self.validate_response(response, None, status_code=status_code, expected_success=expected_success)


    def repost_post(self, post_id:str, payload: CreateRepostParams, status_code: int = 201, expected_success: bool = True):
        response =  self.request()\
            .set_url(self.endpoints.repost_post(post_id)) \
            .set_headers(self.headers.basic) \
            .set_request_body(payload.model_dump(exclude_none=True))\
            .send("POST")

        return self.validate_response(response, ResponsePostUpdateModel, status_code=status_code, expected_success=expected_success)

    def pin_post(self, post_id:str, status_code: int = 204, expected_success: bool = True):
        response =  self.request()\
            .set_url(self.endpoints.pin_post(post_id)) \
            .set_headers(self.headers.basic) \
            .send("POST")
        #
        # response = requests.post(
        #     url=self.endpoints.pin_post(post_id),
        #     headers=self.headers.basic,
        # )
        return self.validate_response(response, None, status_code, expected_success)

    def unpin_post(self, post_id:str, status_code: int = 204, expected_success: bool = True):
        response =  self.request()\
            .set_url(self.endpoints.unpin_post(post_id)) \
            .set_headers(self.headers.basic) \
            .send("POST")

        return self.validate_response(response, None, status_code, expected_success)
