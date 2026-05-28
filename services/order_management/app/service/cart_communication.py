    
import os
import httpx

CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://cart-service:8003")  # Default to cart-service if not set

async def send_request_to_cart_management_service(user_id) -> bool:
    """שליחת בקשה לסרוויס העגלה בכדי ליצור 'תהליך יצירת הזמנה' שכוללת לקיחת כל הפרטים מהעגלה, ועדכון המלאי, אם זה קרה יחזור קוד 200"""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{CART_SERVICE_URL}/create_order/{user_id}")
        
        response.raise_for_status() 

        return True