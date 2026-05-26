from pydantic import BaseModel
from dataclasses import dataclass

class AddProductToCart(BaseModel):
    '''
    מידע שנקבל מסטרימליט, ברגע שהמשתמש לחץ על כפתור "הוסף לעגלה" ובחירת כמות
    ID שנוצר באלסטיקסרץ
    NAME שם המוצר להצגה למשתמש
    PRICE מחיר המוצר בשעת ההזמנה
    '''
    id:str
    name:str
    price:float
    quantity:int
    

class DeleteProduct(BaseModel):
    # מבנה בקשה מהמשתמש למחיקה של מוצר מהעגלה
    id:str


class UpdateQuantityProduct(BaseModel):
    '''כשמשתמש מעוניין לעדכן כמות מוצר בעגלה'''
    product_id:str
    quantity:int 


@dataclass
class CreateItemDTO:
    """
    מבנה המידע שנשמר בואליו של המוצר ברדיס
    save_product_in_cart(user_id:str, product_id:str, product_data:CreateItemDTO
    """
    name:str
    price:float
    quantity:int