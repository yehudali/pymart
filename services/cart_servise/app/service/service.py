from app.schemas.product import CreateItemDTO
from app.repositories.redis_crud import  product_exists, save_product_in_cart, update_product_quantity, delete_product_from_cart, delete_cart, get_all_product
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
    

async def delete_product_from_cart1(user_id:str, product_id:str, redis_client:redis.asyncio.Redis):
    """הפעלת הפונקציה שעובדת מול רדיס, אם החזירה 1 נחיז תרוו אחרת פאלס"""
    res = await delete_product_from_cart(user_id=user_id, product_id=product_id, redis_client=redis_client)
    if res:
        return True
    else:
        return False
    

async def delete_cart1(user_id:str, redis_client:redis.asyncio.Redis):
    res = await delete_cart(user_id=user_id,redis_client=redis_client)
    if res:
        return True
    else:
        return False
    

async def update_quantity1(user_id:str, product_id:str, quantity:int, redis_client:redis.asyncio.Redis):
    return await update_product_quantity(user_id=user_id, product_id=product_id, quantity=quantity, redis_client=redis_client)

async def calculate_cart_amount(product_dict : dict[str,CreateItemDTO])-> tuple[float, int]:
    """
    פונקצית עזר לחישוב סכום העלויות של 
    המוצרים בעגלה שמתקבלים מרדיס
    """
    amount=0.0
    sum_items = 0
    for key, value in product_dict.items():
        amount+=value.price
        sum_items += 1

    return amount, sum_items

async def get_cart_product_and_information(user_id:str, redis_client:redis.asyncio.Redis):
    product_dict = await get_all_product(user_id=user_id, redis_client=redis_client)
    cart_amount, sum_product = await calculate_cart_amount(product_dict)
    return {
        "sum_products":sum_product,
        "cart_amount":cart_amount,
        "product" : product_dict
    }
