from dataclasses import dataclass

from faker import Faker
from pydantic import BaseModel

fake = Faker()

@dataclass(repr=False)
class CreateAccountPayload(BaseModel):
    email: str
    display_name: str
    username: str
    password: str | int = None


@dataclass(repr=False)
class LoginToAccountPayload(BaseModel):
    password: str
    email: str


@dataclass(repr=False)
class LoginToAccountPayloadByRoleTestCase:
    role: str

@dataclass(repr=False)
class RefreshTokenPayload(BaseModel):
    refresh_token: str



@dataclass(repr=False)
class LogoutPayload(BaseModel):
    refresh_token: str

class Payloads:

    def login_account(self, email: str, password: str):
        return {
            "email": email,
            "password": password
        }

    def refresh(self, refresh_token: str):
        return {
            "refresh_token": f"{refresh_token}"
        }

    def logout(self, refresh_token: str):
        return {
            "refresh_token": f"{refresh_token}"
        }
