from pydantic import BaseModel

# מייצג פריט בודד שיועבר לסרוויס הקטלוג
class OrderItem(BaseModel):
    product_id: str
    quantity: int
