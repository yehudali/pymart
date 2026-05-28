from fastapi import APIRouter, Depends, HTTPException
from app.core.redis_client import get_redis_client
from app.core.security import checking_basic_user_permissions
from app.service.creating_orders import create_order_service



router = APIRouter()

@router.post("/create_order/{user_id}", tags=["orders"])
async def create_order(user_id: str, redis_client = Depends(get_redis_client)):
    try:
        await create_order_service(user_id=user_id, redis_client=redis_client) 
        return {"success": True, "message": "order created successfully"}
        
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
        
    except Exception as err:
        print(f"Unexpected error: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")