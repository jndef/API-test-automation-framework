from common.base_api import BaseAPI
from services.auth.endpoints import Endpoints
from services.auth.models.model_login import LoginResponse
from services.auth.models.model_me import GetMe
from services.auth.payloads import Payloads
from config.headers import Headers


class AuthAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.headers = Headers()
        self.endpoints = Endpoints()

    def login(self, email: str, password: str, status_code: int = 200, expected_success: bool = True):
        response =  self.request()\
            .set_url(self.endpoints.login_account)\
            .set_headers({"Content-Type": "application/json"})\
            .set_request_body(self.payloads.login_account(email, password))\
            .send("POST")
        return self.validate_response(response, LoginResponse, status_code=status_code, expected_success=expected_success)

    def refresh(self, refresh_token: str, status_code: int = 200, expected_success: bool = True):
        response =  self.request()\
            .set_url(self.endpoints.refresh)\
            .set_headers({"Content-Type": "application/json"})\
            .set_request_body(self.payloads.refresh(refresh_token))\
            .send("POST")
        return self.validate_response(response, LoginResponse, status_code=status_code, expected_success=expected_success)

    def logout(self, token:str, refresh_token: str, status_code: int = 204, expected_success: bool = True):
        response =  self.request()\
            .set_url(self.endpoints.logout)\
            .set_headers({"Content-Type": "application/json","Authorization": f"Bearer {token}"})\
            .set_request_body(self.payloads.logout(refresh_token))\
            .send("POST")
        return self.validate_response(response, None, status_code=status_code, expected_success=expected_success)


    def get_me(self, status_code: int = 200, expected_success: bool = True) -> GetMe:
        response =  self.request()\
            .set_url(self.endpoints.get_me)\
            .set_headers(self.headers.basic)\
            .send("GET")
        return self.validate_response(response, GetMe, status_code, expected_success)
