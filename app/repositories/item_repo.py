from schemas.item_schema import ItemCreate, ItemResponse

# Mock database tạm thời
FAKE_DB = []
CURRENT_ID = 1


def get_all_items() -> list[ItemResponse]:
    return FAKE_DB


def create_item(item: ItemCreate) -> ItemResponse:
    global CURRENT_ID
    new_item = ItemResponse(id=CURRENT_ID, **item.model_dump())
    FAKE_DB.append(new_item)
    CURRENT_ID += 1
    return new_item
