from pydantic import BaseModel
from typing import Optional

class LabelBase(BaseModel):
    name: str
    color: Optional[str] = None

class LabelCreate(LabelBase):
    project_id: str

class LabelResponse(LabelBase):
    id: str
    project_id: str

    class Config:
        from_attributes = True