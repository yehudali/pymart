from pydantic import BaseModel


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
