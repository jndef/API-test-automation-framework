from dataclasses import dataclass, asdict
from typing import Optional, Literal

@dataclass
class BaseParams:
    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}

@dataclass
class PaginationParams(BaseParams):
    page: Optional[int] = None
    per_page: Optional[int] = None

@dataclass
class SortParams(BaseParams):
    sort_order: Optional[str] = None

