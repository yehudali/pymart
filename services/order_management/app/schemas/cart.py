

from pydantic import BaseModel
from typing import Dict


class ProductData(BaseModel):
    name:str
    price:float
    quantity:int

class CartResponse(BaseModel):
    cart: Dict[str, ProductData]


