from schemas.item_schema import ItemCreate, ItemResponse
from repositories import item_repo

def get_items() -> list[ItemResponse]:
    # Có thể thêm logic kiểm tra quyền (auth) hoặc tính toán ở đây
    return item_repo.get_all_items()

def add_item(item: ItemCreate) -> ItemResponse:
    # Ví dụ: Thêm logic báo lỗi nếu giá tiền âm
    if item.price < 0:
        raise ValueError("Giá sản phẩm không được âm")
    
    return item_repo.create_item(item)