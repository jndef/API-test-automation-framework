import allure
from auth.credentials import Credentials, UserProfile
import pytest
from utilits.data_helper import DataHelper


class BaseTest:
    _service_by_role = {}

    data_helper = DataHelper()

    def get_actor(self, role: str | None):
        """
        Setup - Get multi services factory for certain user
        :param role: provided alias used get certain user for test
        :return:
        """
        with allure.step(f'Setup - Get multi services factory for certain user {role}'):
            return self._service_by_role(role)

    @staticmethod
    def get_user_info(alias: str) -> UserProfile:
        """
        Get user info (cred info) for user by provided alias
        :param alias:
        :return:
        """
        return Credentials().get_user(alias)

    @pytest.fixture(autouse=True)
    @allure.title("Setup - Get multi services factory for tests")
    def _inject_services(self, get_service_by_role):
        """Fixture. Technical method to inject services factory info tests session"""
        self._service_by_role = get_service_by_role
