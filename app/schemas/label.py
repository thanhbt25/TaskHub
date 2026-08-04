
from pydantic import BaseModel


class LabelBase(BaseModel):
    name: str
    color: str | None = None

class LabelCreate(LabelBase):
    project_id: str

class LabelResponse(LabelBase):
    id: str
    project_id: str

    class Config:
        from_attributes = True