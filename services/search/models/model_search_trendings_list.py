from typing import Annotated

from pydantic import BaseModel, UUID4, Field


class ResponseTrendingHashtagModel(BaseModel):
    id: Annotated[str, UUID4]
    name: str
    posts_count: int = Field(ge=0)
