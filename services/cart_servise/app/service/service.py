from app.schemas.product import CreateItemDTO
from app.repositories.redis_crud import  product_exists, save_product_in_cart, update_product_quantity
import redis.asyncio

async def add_or_update_product_to_user_cart(user_id:str, product_id:str, data:CreateItemDTO, redis_client:redis.asyncio.Redis):
    """מוסיף מוצר ואם קיים מעדכן את המוצר לעגלה
    צריך לבדוק אם המוצר קיים בסרוויס של הקטלוג, ואם לא להחזיר שגיאה
    """
    ## בדיקה מול הסרוויס של הקטלוג
    res = await product_exists(user_id=user_id, product_id=product_id, redis_client=redis_client)
    if not res:
        return await save_product_in_cart(user_id=user_id, product_id=product_id, product_data=data, redis_client=redis_client)
    else:
        return await update_product_quantity(user_id=user_id, product_id=product_id, quantity=data.quantity, redis_client=redis_client)
    

    
