from pydantic import BaseModel

@dataclass(repr=False)
class UploadImageByRoleTestCase(BaseModel):
    role: str
    file: str
