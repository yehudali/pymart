from fastapi import APIRouter, Depends, HTTPException
from aio_pika.abc import AbstractChannel

from app.core.elastic_search_client import get_elastic_search_client
from app.core.rabbitmq_client import get_rabbitmq_channel

from app.service.cart_communication import send_request_to_cart_management_service
from app.core.security import checking_basic_user_permissions
from app.schemas.order import Order

from app.repositories.elastic_crud import save_order
from app.repositories.rabbitmq_publish import publish_new_order_to_manage_queue

router = APIRouter()

@router.post("/create_order", tags=["orders"])
async def create_new_order(user_id=Depends(checking_basic_user_permissions), elastic_search_client=Depends(get_elastic_search_client), rabbitmq_channel: AbstractChannel = Depends(get_rabbitmq_channel)):
    try:
        cart = await send_request_to_cart_management_service(user_id=user_id)
        new_order = Order(
        user_id=user_id,
        cart=cart.cart
    )   
        await save_order(elastic_client=elastic_search_client, order=new_order.model_copy().model_dump())
        await publish_new_order_to_manage_queue(order=new_order.model_copy().model_dump(), rabbitmq_channel=rabbitmq_channel)
        
        # TODO הוספת לוגיקה של יצירת הזמנה ב-ES, ופרסום RABBITMQ


    except Exception as err:
        print(f"order creation failed for user {user_id}.. error: {err}")
        raise HTTPException(status_code=400, detail="unable to process order")



@router.get("/orders", tags=["orders"])
async def get_orders(user_id: str = Depends(checking_basic_user_permissions)):
    try:
        # TODO הוספת לוגיקה של getting orders from ES
        pass

        return {"message": "orders retrieved successfully"}
    except Exception as err:
        print(f"failed to retrieve orders for user {user_id}.. error: {err}")
        raise HTTPException(status_code=400, detail="unable to retrieve orders at this time")


@router.put("/orders/{order_id}/status", tags=["orders"])
async def update_order_status(order_id: str, new_status: str, user_id: str = Depends(checking_basic_user_permissions)):
    try:
        # TODO הוספת לוגיקה של עדכון סטטוס הזמנה ב-ES, ופרסום RABBITMQ
        pass

        return {"message": "order status updated successfully"}
    except Exception as err:
        print(f"order status update failed for order {order_id}.. error: {err}")
        raise HTTPException(status_code=400, detail="unable to update order status at this time")
    