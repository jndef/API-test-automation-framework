import json
import pprint
from dataclasses import dataclass, asdict
from typing import Optional, Literal, Union

SortOrderType = Union[Literal["asc", "desc"], None, str]


from dataclasses import fields

class ReadableParams:
    def __repr__(self):
        info =  {}
        for f in fields(self):
            info[f.name] = getattr(self, f.name)
        # parsed_response = json.dumps(info, indent=4)

        # return str(info)
        # g = {getattr(self, f.name) for f in fields(self)}
        # a:list[dict] = [{f.name:getattr(self, f.name)} for f in fields(self)]
        # b = [(k, v) for i in a for k, v in i.items()]
        # return pprint.pformat(info)
        return ",\n ".join(f"{f.name}={getattr(self, f.name)}" for f in fields(self) if getattr(self, f.name) is not None)
        # return ",\n ".join(f"{f.name}={getattr(self, f.name)}" for f in fields(self))

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
