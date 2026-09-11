from pydantic import BaseModel


class CreateAccountPayload(BaseModel):
    email: str
    display_name: str
    username: str
    password: str | int = None


class LoginToAccountPayload(BaseModel):
    password: str
    email: str


class RefreshTokenPayload(BaseModel):
    refresh_token: str


class LogoutPayload(BaseModel):
    refresh_token: str
