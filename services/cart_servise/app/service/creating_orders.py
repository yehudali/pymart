from app.repositories.redis_crud import get_all_product
import redis.asyncio
import httpx
import os
from app.schemas.product import CreateItemDTO
from app.schemas.order import OrderItem 


CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL", "http://catalog_management:8000")


async def get_products_id_and_quantity(products_data: dict[str,CreateItemDTO])-> list[tuple[str, int]]:
    """
    פונקצית עזר שמקבלת את המוצרים בעגלהת מחזירה רשימה של טאפלים עם מזהה המוצר והכמות שהוזמנה
    """
    product_quantity_list = []
    for key, value in products_data.items():
        product_quantity_list.append((key, value.quantity))
    
    return product_quantity_list


async def creating_orders(user_id:str, redis_client:redis.asyncio.Redis)-> bool:
    try:
        products_data = await get_all_product(user_id=user_id, redis_client=redis_client)

        if not products_data:
            raise Exception("cart is empty, cannot create order")
          
    except  Exception as err:
        print(f"error: {err}")
        raise ValueError("error while getting cart from redis, show logs")
    
    """נרצה רשימה של טאפלים, עם מזהה המוצר והכמות שהוזמנה,ניצור בעזרת הפונקציה הבאה"""
    product_quantity_list = await get_products_id_and_quantity(products_data=products_data)
    
    payload = [
        OrderItem(product_id=pid, quantity=qty).model_dump() 
        for pid, qty in product_quantity_list
    ]

    """נשלח את הרשימה לבדיקה בסרוויס של ניהול קטלוג המוצרים-(ומלאי)"""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{CATALOG_SERVICE_URL}/create_order", json=payload) # TODO: להחליף בכתובת הנכונה של הסרוויס של הקטלוג, 
    if response:
        return True
    else:
        raise Exception(f"Unable to produce order: {response.text}")
        