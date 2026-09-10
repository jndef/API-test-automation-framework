from  pydantic import BaseModel
from typing import Literal

class LogoutResponse(BaseModel):
    detail: Literal["Not authenticated"]
