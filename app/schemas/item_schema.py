from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int