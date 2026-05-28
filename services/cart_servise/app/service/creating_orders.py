from app.repositories.redis_crud import get_all_product
import redis.asyncio
import httpx

from app.repositories.communication_with_catalog import CATALOG_SERVICE_URL, send_order_to_catalog
from app.schemas.product import CreateItemDTO
from app.schemas.order import OrderItem 


async def create_order_service(user_id: str, redis_client: redis.asyncio.Redis) -> bool:
    # שלב א': הבאת נתוני המוצרים שבעגלה-מרדיס
    products_data = await get_all_product(user_id=user_id, redis_client=redis_client)
    
    if not products_data:
        raise ValueError("Cart is empty, cannot create order") 
    
    #  יצירת רשימה לשליחה לסרוויס של ניהול קטלוג
    payload = [
        OrderItem(product_id=pid, quantity=item.quantity).model_dump() 
        for pid, item in products_data.items()
    ]

    # העברה לסרוויס ניהול קטלוג לבדיקה (ועדכון אם קיימים כל המוצרים) יחזיר תגובה בוליאנית 
    try:
        # 1. הקריאה  לקטלוג לוודא מלאי ולעדכן
        await send_order_to_catalog(payload)
        
        # 2. אם לא היתה שגיאה עד כה, פרסום האירוע בתור של ההזמנות
        # await publish_order_event(topic="order.created", payload=payload) # TODO: לממש מול המסג' ברוקר הנבחר

        return True
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"Catalog service error: {e.response.text}")
    except Exception as e:
        raise RuntimeError(f"Error: {str(e)}")



















# async def creating_orders(user_id:str, redis_client:redis.asyncio.Redis)-> bool:
#     try:
#         products_data = await get_all_product(user_id=user_id, redis_client=redis_client)

#         if not products_data:
#             raise Exception("cart is empty, cannot create order")
          
#     except  Exception as err:
#         print(f"error: {err}")
#         raise ValueError()
    
    # """נרצה רשימה של טאפלים, עם מזהה המוצר והכמות שהוזמנה,ניצור בעזרת הפונקציה הבאה"""
    # product_quantity_list = await get_products_id_and_quantity(products_data=products_data)
    
    # payload = [
    #     OrderItem(product_id=pid, quantity=qty).model_dump() 
    #     for pid, qty in product_quantity_list
    # ]

    # """נשלח את הרשימה לבדיקה בסרוויס של ניהול קטלוג המוצרים-(ומלאי)"""
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(f"{CATALOG_SERVICE_URL}/create_order", json=payload) # TODO: להחליף בכתובת הנכונה של הסרוויס של הקטלוג, 
    # if response:
    #     return True
    # else:
    #     raise Exception(f"Unable to produce order: {response.text}")
        