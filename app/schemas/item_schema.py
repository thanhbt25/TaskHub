
from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    price: float
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int
