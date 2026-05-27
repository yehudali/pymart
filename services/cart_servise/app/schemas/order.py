from pydantic import BaseModel
# from typing import List

# מייצג פריט בודד שיועבר לסרוויס הקטלוג
class OrderItem(BaseModel):
    product_id: str
    quantity: int
