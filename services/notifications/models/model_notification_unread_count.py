from pydantic import BaseModel, Field


class ResponseNotificationsCountModel(BaseModel):
    count: int= Field(ge=1)