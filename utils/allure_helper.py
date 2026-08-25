import json

import allure


class AllureHelper:

    def attach_response(self, response):
        # print(f"attach_response: {response.request.url}")
        parsed_response = json.dumps(response, indent=4)
        allure.attach(
            body=parsed_response,
            name='API Response',
            attachment_type=allure.attachment_type.JSON)
    def attach_failure(self, response):
        # print(f"attach_response: {response.request.url}")
        allure.attach(
            body=f"{response.request.method}. {response.request.url}\nRequest body:{response.request.body if response.request.method == "POST" else None}\nResponse text: {response.text}",
            name='API Failure',
            attachment_type=allure.attachment_type.TEXT)