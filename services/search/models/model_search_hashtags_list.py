from typing import Annotated, List

from pydantic import BaseModel, UUID4, Field


class ResponseHashtagModel(BaseModel):
    id: Annotated[str, UUID4]
    name: str
    posts_count: int = Field(ge=0)


class ResponseHashtagsModel(BaseModel):
    items: List[ResponseHashtagModel]
    total: int = Field(ge=0)
    page: int = Field(ge=1)
    per_page: int = Field(ge=1)
    pages: int = Field(ge=0)
