import allure
import pytest
from config.base_test import BaseTest
from services.auth.payloads import LoginToAccountPayload, RefreshTokenPayload, LogoutPayload


@allure.epic("Auth")
@allure.feature("Auth")
@pytest.mark.registration
class TestUsers(BaseTest):
    @allure.title("Login as user")
    @pytest.mark.parametrize("user_case", [
        pytest.param("user_alice", id="Login as user"),
        pytest.param("moderator", id="Login as moderator"),
        pytest.param("admin", id="Login as admin"),
    ])
    def test_login_user(self, user_case):
        credentials = self.get_user_info(user_case)
        public_client = self.get_actor(None)
        payload = LoginToAccountPayload(email=credentials.email, password=credentials.password)
        public_client.auth_api.login(payload=payload)

    @allure.title("Get me")
    @pytest.mark.parametrize("user_case", [
        pytest.param("user_alice", id="Get me as user"),
        pytest.param("moderator", id="Get me as moderator"),
        pytest.param("admin", id="Get me as admin"),
    ])
    def test_get_me(self, user_case):
        auth_service = self.get_actor(user_case).auth_api
        auth_service.get_me()

    @allure.title("Refresh token")
    @pytest.mark.parametrize("user_case", [
        pytest.param("user_alice", id="Refresh token as user"),
    ])
    def test_refresh_token(self, user_case):
        auth_service = self.get_actor(user_case).auth_api

        credentials = self.get_user_info(user_case)
        login_payload = LoginToAccountPayload(email=credentials.email, password=credentials.password)
        tokens = self.public.auth_api.login(payload=login_payload)
        refresh_payload = RefreshTokenPayload(refresh_token=tokens.refresh_token)
        auth_service.refresh(payload=refresh_payload)

    @pytest.mark.parametrize("user_case", [
        pytest.param("admin", id="Login as admin"),
    ])
    @allure.title("Refresh token - expired")
    def test_refresh_token(self, user_case):
        auth_service = self.get_actor(user_case).auth_api
        refresh_payload = RefreshTokenPayload(
            refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMDAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDMiLCJleHAiOjE3Nzk4MzUxMTUsInR5cGUiOiJyZWZyZXNoIn0.-eneFfh7P8ICRZAED_Eab3S02wASDY-MgzzYLCrf_Fo")
        auth_service.refresh(payload=refresh_payload, expected_success=False, status_code=401)

    @allure.title("Logout")
    @pytest.mark.parametrize("user_case", [
        pytest.param("user_alice", id="Refresh token as user"),
    ])
    def test_logout(self, user_case):
        credentials = self.get_user_info(user_case)
        login_payload = LoginToAccountPayload(email=credentials.email, password=credentials.password)

        tokens = self.public.auth_api.login(payload=login_payload)
        logout_payload = LogoutPayload(refresh_token=tokens.refresh_token)
        self.public.auth_api.logout(payload=logout_payload)
