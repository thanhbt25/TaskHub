from fastapi import APIRouter, HTTPException
from schemas.item_schema import ItemCreate, ItemResponse
from services import item_service

router = APIRouter()


@router.get("/", response_model=list[ItemResponse])
def get_items():
    return item_service.get_items()


@router.post("/", response_model=ItemResponse)
def create_item(item: ItemCreate):
    try:
        return item_service.add_item(item)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
