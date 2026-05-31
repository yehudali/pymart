from fastapi import APIRouter, Depends, HTTPException

from app.service.cart_communication import send_request_to_cart_management_service
from app.core.security import checking_basic_user_permissions
from app.schemas.order import Order

router = APIRouter()

@router.post("/create_order/{user_id}", tags=["orders"])
async def create_new_order(user_id: str):
    try:
        cart = await send_request_to_cart_management_service(user_id=user_id)
        new_order = Order(
        user_id=user_id,
        cart=cart.cart
    )
        
        # TODO הוספת לוגיקה של יצירת הזמנה ב-ES, ופרסום RABBITMQ



    except Exception as err:
        print(f"order creation failed for user {user_id}.. error: {err}")
        raise HTTPException(status_code=400, detail="unable to process order")
    