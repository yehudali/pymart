from fastapi import APIRouter, Depends, HTTPException

from app.service.cart_communication import send_request_to_cart_management_service
from app.core.security import checking_basic_user_permissions

router = APIRouter()

@router.post("/orders/", tags=["orders"])
async def create_new_order(user_id: str = Depends(checking_basic_user_permissions)):
    try:
        await send_request_to_cart_management_service(user_id=user_id)
        return {"success": True, "message": "order processing started successfully"}
        
    except Exception as err:
        print(f"Order creation failed for user {user_id}.. error: {err}")
        raise HTTPException(status_code=400, detail="unable to process order at this time")