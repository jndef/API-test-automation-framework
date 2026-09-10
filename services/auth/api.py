import allure

from common.base_api import BaseAPI
from services.auth.endpoints import Endpoints
from services.auth.models.model_login import LoginResponse
from services.auth.models.model_me import GetMe
from services.auth.models.model_register import RegisterAccountResponse
from services.auth.payloads import CreateAccountPayload, LoginToAccountPayload, RefreshTokenPayload, \
    LogoutPayload
from config.headers import Headers


class AuthAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.headers = Headers()
        self.endpoints = Endpoints()

    def login(self, payload: LoginToAccountPayload, status_code: int = 200, expected_success: bool = True):
        with allure.step(f"API POST request. Login to account ({payload.email})"):
            response = self.request() \
                .set_url(self.endpoints.login_account) \
                .set_headers(self.headers.basic) \
                .set_request_body(payload.model_dump(exclude_none=True)) \
                .send("POST")
            return self.validate_response(response, LoginResponse, status_code=status_code,
                                          expected_success=expected_success)

    def register(self, payload: CreateAccountPayload, status_code: int = 201, expected_success: bool = True):
        with allure.step(f"API POST request. Register to account ({payload})"):
            response = self.request() \
                .set_url(self.endpoints.register_account) \
                .set_headers(self.headers.basic) \
                .set_request_body(payload.model_dump(exclude_none=True)) \
                .send("POST")
            return self.validate_response(response, RegisterAccountResponse, status_code=status_code,
                                          expected_success=expected_success)

    def refresh(self, payload: RefreshTokenPayload, status_code: int = 200, expected_success: bool = True):
        with allure.step(f"API POST Request - Refresh token"):
            response = self.request() \
                .set_url(self.endpoints.refresh) \
                .set_headers(self.headers.basic) \
                .set_request_body(payload.model_dump(exclude_none=True)) \
                .send("POST")
            return self.validate_response(response, LoginResponse, status_code=status_code,
                                          expected_success=expected_success)

    def logout(self, token: str, payload: LogoutPayload, status_code: int = 204, expected_success: bool = True):
        with allure.step(f"API POST Request - Logout from account"):
            response = self.request() \
                .set_url(self.endpoints.logout) \
                .set_headers(self.headers.basic({"Authorization": f"Bearer {token}"})) \
                .set_request_body(payload.model_dump(exclude_none=True)) \
                .send("POST")
            return self.validate_response(response, None, status_code=status_code, expected_success=expected_success)

    def get_me(self, status_code: int = 200, expected_success: bool = True) -> GetMe:
        with allure.step(f"API Request - Get me profile"):
            response = self.request() \
                .set_url(self.endpoints.get_me) \
                .set_headers(self.headers.basic) \
                .send("GET")
            return self.validate_response(response, GetMe, status_code, expected_success)
