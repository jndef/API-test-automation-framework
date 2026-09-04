import allure
from common.base_api import BaseAPI
from config.headers import Headers
from services.notifications.endpoints import Endpoints
from services.notifications.models.model_notification_list import ResponseNotificationsModel
from services.notifications.models.model_notification_unread_count import ResponseNotificationsCountModel
from services.notifications.params import GetNotificationsParams


class NotificationsAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.headers = Headers()
        self.endpoints = Endpoints()

    def get_notification_list(self, params: GetNotificationsParams = None, status_code: int = 200,
                              expected_success: bool = True):
        with allure.step(f"API Request - get notification list"):
            response = self.request() \
                .set_url(self.endpoints.get_notifications) \
                .set_query_params(**(params.to_dict() if params else {})) \
                .set_headers(self.headers.basic) \
                .send("GET")
            return self.validate_response(response, ResponseNotificationsModel, status_code, expected_success)

    def get_unread_count(self, status_code: int = 200, expected_success: bool = True):
        with allure.step(f"API Request - get notification unread count"):
            response = self.request() \
                .set_url(self.endpoints.get_notifications) \
                .set_headers(self.headers.basic) \
                .send("GET")
            return self.validate_response(response, ResponseNotificationsCountModel, status_code, expected_success)

    def mark_read_notification(self, notification_id: str, status_code: int = 204, expected_success: bool = True):
        with allure.step(f"API POST Request - mark notification read"):
            response = self.request() \
                .set_url(self.endpoints.mark_read(notification_id)) \
                .set_headers(self.headers.basic) \
                .send("POST")
            return self.validate_response(response, None, status_code, expected_success)

    def mark_read_all_notifications(self, status_code: int = 204, expected_success: bool = True):
        with allure.step(f"API POST Request - mark all notifications read"):
            response = self.request() \
                .set_url(self.endpoints.mark_read_all) \
                .set_headers(self.headers.basic) \
                .send("POST")
            return self.validate_response(response, None, status_code, expected_success)
