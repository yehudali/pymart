    
import os
import httpx

from app.schemas.cart import CartResponse

CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://cart-service:8003")  # Default to cart-service if not set

async def send_request_to_cart_management_service(user_id) -> CartResponse:
    """שליחת בקשה לסרוויס העגלה בכדי ליצור 'תהליך יצירת הזמנה' שכוללת לקיחת כל הפרטים מהעגלה, ועדכון המלאי"""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{CART_SERVICE_URL}/create_order/{user_id}")
        
        response.raise_for_status() 
        if response.status_code == 200:
            cart_data = response.json()
            return CartResponse(cart=cart_data)
        
        else:
            raise Exception('the status code of response from order service is not 200')
