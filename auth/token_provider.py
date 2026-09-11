import allure
from dotenv import load_dotenv

from auth.credentials import Credentials
from services.auth.api import AuthAPI
from services.auth.payloads import LoginToAccountPayload

load_dotenv()
credentials = Credentials()


class TokenProvider:
    _token_cache = {}  # cash on class lvl, not instance

    def get_token_for_role(self, role: str) -> str:
        """
        Method to get token for given role. Requests POST /login using credentials of certain user.
        Then puts token in cache (token_cache:dict) for given role to reuse in test session
        Next test will check, if token is present in cache. If yes, retrieve from cache
        :param role: alias of the user, who performs login
        :return: token from response / cache (str)
        """
        if role in self._token_cache:
            with allure.step(f"Setup - Authenticate as: {role} (cashed)"):
                return self._token_cache[role]
        creds = credentials.get_user(role)
        auth_api_client = AuthAPI()

        with allure.step(f"Setup - Authenticate as: {creds.email}"):
            # response =  auth_api_client.login(creds.email,creds.password)
            payload = LoginToAccountPayload(email=creds.email, password=creds.password)
            response = auth_api_client.request() \
                .set_url(auth_api_client.endpoints.login_account) \
                .set_headers(auth_api_client.headers.basic) \
                .set_request_body(payload.model_dump(exclude_none=True)) \
                .send("POST")
            if response.status_code == 200:
                token = response.json()["access_token"]
                self._token_cache[role] = token
                return token
            raise BaseException(f"Authentication failed {response.status_code}\nResponse text: {response.text}")
