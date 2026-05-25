import redis.asyncio as redis
from fastapi import APIRouter, Depends, HTTPException

# from app.repositories.redis_crud import get_item
from app.service.service import add_or_update_product_to_user_cart,delete_product_from_cart1, delete_cart1, update_quantity1, get_cart_product_and_information
from app.core.redis_client import get_redis_client
from app.core.security import checking_basic_user_permissions
from app.schemas.product import AddProductToCart, DeleteProduct, UpdateQuantityProduct, CreateItemDTO
from app.schemas.cart import CartInfoResponse

router = APIRouter()

@router.get("/healthcheck")
async def healthcheck_test(redis_client:redis.Redis = Depends(get_redis_client)):
    return await redis_client.ping() # type: ignore


@router.post("/cart/product")
async def add_product_to_cart(product:AddProductToCart, user_id=Depends(checking_basic_user_permissions), redis_client:redis.Redis = Depends(get_redis_client)):
    try:
        product_data = CreateItemDTO(name=product.name, price=product.price, quantity=product.quantity)
        return await add_or_update_product_to_user_cart(user_id=user_id, product_id=product.id, data=product_data, redis_client=redis_client)
    except Exception as err:
         print(f"error: {err}")
         raise HTTPException(status_code=500, detail="something went wrong show logs")
    
@router.delete("/cart/product")
async def delete_product_from_cart(product_id:DeleteProduct, user_id=Depends(checking_basic_user_permissions), redis_client:redis.Redis = Depends(get_redis_client)):
        try:
            return await delete_product_from_cart1(user_id=user_id, product_id=product_id.id, redis_client=redis_client)
        except Exception as err:
         print(f"error: {err}")
         raise HTTPException(status_code=500, detail="something went wrong show logs")
        
@router.delete("/cart")
async def delete_cart(user_id=Depends(checking_basic_user_permissions), redis_client:redis.Redis = Depends(get_redis_client)):
    try:
        return await delete_cart1(user_id=user_id, redis_client=redis_client)
    except Exception as err:
         print(f"error: {err}")
         raise HTTPException(status_code=500, detail="something went wrong show logs")
         
@router.put("/cart/product/quantity")
async def update_quantity(update:UpdateQuantityProduct ,user_id=Depends(checking_basic_user_permissions), redis_client:redis.Redis = Depends(get_redis_client)):
    try:
        return await update_quantity1(user_id=user_id, product_id=update.product_id, quantity=update.quantity,redis_client=redis_client)
    except Exception as err:
         print(f"error: {err}")
         raise HTTPException(status_code=500, detail="something went wrong show logs")

@router.get("/cart", response_model=CartInfoResponse)
async def get_cart_and_information(user_id = Depends(checking_basic_user_permissions), redis_client:redis.Redis = Depends(get_redis_client)):
    try:
        return await get_cart_product_and_information(user_id=user_id, redis_client=redis_client)
    except Exception as err:
        print(f"error: {err}")
        return HTTPException(status_code=500, detail="somthin went worng show logs")
