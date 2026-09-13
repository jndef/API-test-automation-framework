import allure
import requests
from pydantic import BaseModel

from utils.allure_helper import AllureHelper
from common.http_request_builder import HttpRequestBuilder as Http_builder


class BaseAPI:
    def __init__(self):
        self.reporter = AllureHelper()
        # self.request_builder = HttpRequestBuilder()

    @staticmethod
    def request() -> Http_builder:
        return Http_builder()

    def validate_response(self, response: requests.Response, model: type[BaseModel] = None, status_code: int = 200,
                          expected_success: bool = True):
        with allure.step(f'Validate response for {response.request.method} {response.request.url}'):
            print(
                f"\nRequest to validate: {response.request.method} {response.request.url}\nExpected status code: {status_code}, actual status code: {response.status_code}\nValidate_response...")
            if response.status_code != status_code:
                self.reporter.attach_failure(response)
                if response.status_code == 403:
                    raise Exception(
                        f"Failed. Request {response.request.method} {response.request.url} returned {response.status_code} status code.\n Request headers: {response.request.headers}\nResponse text: {response.text}")
                raise Exception(
                    f"Failed. Request {response.request.method} {response.request.url} returned {response.status_code} status code.\n Request headers: {response.request.headers}\nResponse text: {response.text}")
            # if model is not None:
            if expected_success and model is not None:
                self.reporter.attach_response(response.json())
                if isinstance(response.json(), dict):
                    return model(**response.json())
                elif isinstance(response.json(), list):
                    return [model(**item) for item in response.json()]
                raise Exception("Unexpected case with API")
