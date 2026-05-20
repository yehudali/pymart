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


# class InsertProduct(BaseModel):
#     name:str = Field(min_length=2)
#     description:str = Field(default="empty", min_length=5)
#     price:float = Field(ge=0.0)
#     category:str = Field()
#     stock_count:int = Field(ge=0)
#     image_url:Optional[str] = None




