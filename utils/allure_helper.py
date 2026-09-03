import json

import allure


class AllureHelper:

    def attach_payload(self, payload):
        with allure.step("Attach request payload"):
            formatted_payload = payload.model_dump(exclude_none=True)
            parsed_response = json.dumps(formatted_payload, indent=4)
            allure.attach(
                body=parsed_response,
                name='Request payload',
                attachment_type=allure.attachment_type.JSON)

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
            body=f"{response.request.body}",
            name='API Request payload',
            attachment_type=allure.attachment_type.TEXT)
        # allure.attach(
        #     body=f"\nResponse text: {response.text}",
        #     name='API Failure',
        #     attachment_type=allure.attachment_type.TEXT)