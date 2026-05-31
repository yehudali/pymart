# pydantic moduls
from pydantic import BaseModel, Field
from typing import Optional


class InsertProduct(BaseModel):
    name:str = Field(min_length=2)
    description:str = Field(default="empty", min_length=5)
    price:float = Field(ge=0.0)
    category:str = Field()
    stock_count:int = Field(ge=0)
    image_url:Optional[str] = None



class UpdateProduct(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    stock_count: Optional[int] = None
    image_url: Optional[str] = None


class Source(BaseModel):
    name:str
    description:Optional[str] = None
    price: float
    category: str
    stock_count: int
    image_url: Optional[str] = None

class ResponseProduce(BaseModel):
    # id: int
    id: str = Field(alias="_id")
    source: Source = Field(alias="_source")


# קבלת מוצרים מסרויס עגלה לצורך בדיקת מלאי
class OrderItemIncoming(BaseModel):
    product_id: str
    quantity: int