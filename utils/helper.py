import json

import allure
import requests
from pydantic import BaseModel


class Helper:



    def validate_response(self, response:requests.Response, model:type[BaseModel]=None,status_code:int=200, expected_success:bool=True):
        print(f"\nRequest to validate: {response.request.method} {response.request.url}\nExpected status code: {status_code}, actual status code: {response.status_code}\nValidate_response...")
        if response.status_code == 500:
            self.attach_failure(response)
            raise Exception(f"BE returns 500 error. Info:\n{response.request.method}. {response.request.url}\nRequest body:{response.request.body if response.request.method == "POST" else None}\nResponse text: {response.text}")
        if model is not None:
            self.attach_response(response.json())
        assert response.status_code == status_code, f"Failed status code check. \nER/AR: {status_code}/{response.status_code}.\nRequest: {response.request.method}. {response.request.url} \nRequest body:{response.request.body if response.request.method == "POST" else None} \nResponse: {response.text}"
        if expected_success and model is not None:
            if isinstance(response.json(), dict):
                return model(**response.json())
            elif isinstance(response.json(), list):
                return [model(**item) for item in response.json()]
            raise Exception("Unexpected response from API")


