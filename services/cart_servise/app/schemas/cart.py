from typing import Dict
from pydantic import BaseModel

class product(BaseModel):
    name:str
    # description:str
    price:float
    category:str
    # stock_count:int
    quantity:int

class cart(BaseModel):
    id:str
    products:list[product]

class ProductData(BaseModel):
    name:str
    price:float
    quantity:int

class CartInfoResponse(BaseModel):
    sum_products:int
    cart_amount:float
    product:Dict[str,ProductData]



