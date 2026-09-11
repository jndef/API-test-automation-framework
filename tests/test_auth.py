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
        payload = LoginToAccountPayload(email=credentials.email, password=credentials.password)
        public_client = self.get_actor(None)
        public_client.auth_api.login(payload=payload)

    @allure.title("Login as user with not existed email")
    def test_login_user_not_existed(self):
        public_client = self.get_actor(None)

        payload = LoginToAccountPayload(email=self.data_helper.generate_email(), password="password")
        public_client.auth_api.login(payload=payload, expected_success=False, status_code=401)

    @allure.title("Login as user with wrong password")
    @pytest.mark.parametrize("user_case", [
        pytest.param("user_alice", id="Login as user with wrong password"),
    ])
    def test_login_user_not_existed(self, user_case):
        credentials = self.get_user_info(user_case)
        payload = LoginToAccountPayload(email=credentials.email, password="password123")
        public_client = self.get_actor(None)
        public_client.auth_api.login(payload=payload, expected_success=False, status_code=401)

    @allure.title("Login to account as deactivated user")
    @pytest.mark.testing
    def test_login_deactivated_account(self, register_remove_new_account):
        removed_account_info = register_remove_new_account
        payload = LoginToAccountPayload(email=removed_account_info.email, password=removed_account_info.password)
        public_client = self.get_actor(None)
        public_client.auth_api.login(payload=payload, expected_success=False, status_code=400)

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
        public_client = self.get_actor(None)
        credentials = self.get_user_info(user_case)
        login_payload = LoginToAccountPayload(email=credentials.email, password=credentials.password)
        tokens = public_client.auth_api.login(payload=login_payload)
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
        public_client = self.get_actor(None)
        credentials = self.get_user_info(user_case)
        login_payload = LoginToAccountPayload(email=credentials.email, password=credentials.password)

        tokens = public_client.auth_api.login(payload=login_payload)
        logout_payload = LogoutPayload(refresh_token=tokens.refresh_token)
        public_client.auth_api.logout(payload=logout_payload)

    @allure.title("Register account")
    def test_register_account(self, account_cleaner):
        public_client = self.get_actor(None)
        register_payload = self.data_helper.get_random_register_account_payload()

        new_account = public_client.auth_api.register(payload=register_payload)

        account_cleaner(new_account.id)  # register created user id for deactivation after test by admin

        assert new_account.display_name == register_payload.display_name, f"Created account has different display name. ER/AR: {new_account.display_name}/{register_payload.display_name}"
        assert new_account.username == register_payload.username, f"Created account has different username. ER/AR: {new_account.username}/{register_payload.username}"
        assert new_account.email == register_payload.email, f"Created account has different email. ER/AR: {new_account.email}/{register_payload.email}"
        public_client.auth_api.login(
            payload=LoginToAccountPayload(email=register_payload.email, password=register_payload.password))

    @allure.title("Register account using email of existed user")
    @pytest.mark.parametrize("user_case", [
        pytest.param("user_alice", id="Register account using email of existed user"),
    ])
    def test_register_account_registered_email(self, user_case):
        credentials = self.get_user_info(user_case)
        register_payload = self.data_helper.get_random_register_account_payload()
        register_payload.email, register_payload.password = credentials.email, credentials.password
        public_client = self.get_actor(None)
        public_client.auth_api.register(payload=register_payload, expected_success=False, status_code=409)

    @allure.title("Register account using email of deactivated account")
    @pytest.mark.testing
    def test_register_account_registered_email(self, register_remove_new_account):
        register_payload = self.data_helper.get_random_register_account_payload()
        removed_account_info = register_remove_new_account
        register_payload.email = removed_account_info.email
        public_client = self.get_actor(None)
        public_client.auth_api.register(payload=register_payload, expected_success=False, status_code=409)
