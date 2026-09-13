from dataclasses import dataclass, asdict
from typing import Optional, Literal, Union

SortOrderType = Union[Literal["asc", "desc"], None, str]
SortByType = Union[Literal["created_at", "username", "display_name"], None, str]

from dataclasses import fields

class ReadableParams:
    """
    Class to make readable params at allure reporting
    """
    def __repr_args__(self):
        info =  {}
        for f in fields(self):
            info[f.name] = getattr(self, f.name)
        return ",\n ".join(f"{f.name}={getattr(self, f.name)}" for f in fields(self) if getattr(self, f.name) is not None)


@dataclass(repr=False)
class BaseParams:
    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}




@dataclass(repr=False)
class PaginationParams(BaseParams):
    page: Optional[int] = None
    per_page: Optional[int] = None


@dataclass(repr=False)
class SortParams(BaseParams):
    sort_order: Optional[SortOrderType] = None

@dataclass(repr=False)
class SortByParam(BaseParams):
    sort_by: Optional[SortByType] = None
