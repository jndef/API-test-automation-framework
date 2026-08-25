import allure
import pytest
from config.base_test import BaseTest

@allure.epic("Auth")
@allure.feature("Auth")
@pytest.mark.registration
class TestUsers(BaseTest):
    @allure.title("Login as user")
    def test_login_user(self):
        credentials = self.get_user_info("user_alice")
        self.public.auth_api.login(credentials.email, credentials.password)

    @allure.title("Get me")
    def test_get_me(self):
        self.admin.auth_api.get_me()

    @allure.title("Refresh token")
    def test_refresh_token(self):
        credentials = self.get_user_info("user_alice")
        tokens = self.public.auth_api.login(credentials.email, credentials.password)
        self.admin.auth_api.refresh(tokens.refresh_token)

    @allure.title("Refresh token - expired")
    def test_refresh_token(self):
        self.admin.auth_api.refresh(
            refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMDAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDMiLCJleHAiOjE3Nzk4MzUxMTUsInR5cGUiOiJyZWZyZXNoIn0.-eneFfh7P8ICRZAED_Eab3S02wASDY-MgzzYLCrf_Fo", expected_success=False, status_code=401)


    @allure.title("Logout")
    def test_logout(self):
        credentials = self.get_user_info("user_alice")
        tokens = self.public.auth_api.login(credentials.email, credentials.password)
        self.public.auth_api.logout(token=tokens.access_token, refresh_token=tokens.refresh_token)


