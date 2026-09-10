from pydantic import BaseModel, Field


class ResponseStatisticsModel(BaseModel):
    total_users: int = Field(ge=0)
    active_users: int = Field(ge=0)
    total_posts: int = Field(ge=0)
    total_comments: int = Field(ge=0)
    total_conversations: int = Field(ge=0)
    total_messages: int = Field(ge=0)
