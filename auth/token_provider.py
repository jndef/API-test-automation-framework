import os

import allure
import requests
from dotenv import load_dotenv

from auth.credentials import Credentials
from services.auth.api import AuthAPI

load_dotenv()
credentials = Credentials()


class  TokenProvider:
    _token_cache = {}  # кэш на уровне класса, не инстанса


    def get_token_for_role(self, role:str):
        if role in self._token_cache:
            with allure.step(f"Setup - Authenticate as: {role} (cashed)"):
                return self._token_cache[role]
        creds = credentials.get_user(role)
        auth_api_client = AuthAPI()

        with allure.step(f"Setup - Authenticate as: {creds.email}"):
            # response =  auth_api_client.login(creds.email,creds.password)
            response = auth_api_client.request() \
                .set_url(auth_api_client.endpoints.login_account) \
                .set_headers(auth_api_client.headers.basic) \
                .set_request_body(auth_api_client.payloads.login_account(creds.email, creds.password)) \
                .send("POST")
            if response.status_code == 200:
                token = response.json()["access_token"]
                self._token_cache[role] = token
                print(f"\nAuthenticated as: {role}")
                return token
            raise BaseException(f"Authentication failed {response.status_code}\nResponse text: {response.text}")
