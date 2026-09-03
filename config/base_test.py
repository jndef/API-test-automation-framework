import allure

from auth.credentials import Credentials, UserProfile
from services.auth.api import AuthAPI
import pytest

from utils.data_helper import DataHelper


class BaseTest:

    # def setup_method(self):
    #     self.users_api = UsersAPI()
    #     self.wishlists_api = WishlistAPI()

    _service_by_role = {}

    data_helper = DataHelper()

    def get_actor(self, role: str):
        with allure.step(f'Setup - Get multi services factory for certain user {role}'):
            return self._service_by_role(role)

    @staticmethod
    def get_user_info(alias: str) -> UserProfile:
        return Credentials().get_user(alias)

    @property
    def admin(self):
        return self._service_by_role('admin')

    @property
    def user_eve(self):
        return self._service_by_role('user_eve')

    @property
    def user_bob(self):
        return self._service_by_role('user_bob')

    @property
    def moderator(self):
        return self._service_by_role('moderator')

    @property
    def user_banned(self):
        return self._service_by_role('user_banned')


    @property
    def public(self):
        return self._service_by_role(role=None)



    @pytest.fixture(autouse=True)
    @allure.title("Setup - Get multi services factory for tests")
    def _inject_services(self, get_service_by_role):
        self._service_by_role = get_service_by_role

