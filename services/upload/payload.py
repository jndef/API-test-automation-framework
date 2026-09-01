from dataclasses import dataclass

from pydantic import BaseModel



class UploadImageByRoleTestCase(BaseModel):
    role: str
    file:str
