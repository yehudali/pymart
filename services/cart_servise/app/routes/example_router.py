import redis.asyncio as redis
from fastapi import APIRouter, Depends

# from app.repositories.redis_crud import get_item
from app.service.service import add_or_update_product_to_user_cart
from app.core.redis_client import get_redis_client
from app.core.security import checking_basic_user_permissions
from app.schemas.product import AddProductToCart, DeleteProduct, UpdateQuantityProduct, CreateItemDTO

router = APIRouter()

@router.get("/healthcheck")
async def healthcheck_test(redis_client:redis.Redis = Depends(get_redis_client)):
    return await redis_client.ping() # type: ignore

@router.get("/cart")
async def get_all_cart(user_id=Depends(checking_basic_user_permissions)):
    '''מוצרים, כמות מוצרים, ומחיר כולל'''
    pass

@router.post("/cart/product")
async def add_product_to_cart(product:AddProductToCart, user_id=Depends(checking_basic_user_permissions), redis_client:redis.Redis = Depends(get_redis_client)):
    product_data = CreateItemDTO(name=product.name, price=product.price, quantity=product.quantity)
    return await add_or_update_product_to_user_cart(user_id=user_id, product_id=product.id, data=product_data, redis_client=redis_client)

@router.delete("/cart/product")
async def delete_product_from_cart(product_id:DeleteProduct, user_id=Depends(checking_basic_user_permissions), redis_client:redis.Redis = Depends(get_redis_client)):
    pass

@router.delete("/cart")
async def delete_cart(user_id=Depends(checking_basic_user_permissions), redis_client:redis.Redis = Depends(get_redis_client)):
    pass

@router.put("/cart/product/quantity")
async def update_quantity(update:UpdateQuantityProduct ,user_id=Depends(checking_basic_user_permissions), redis_client:redis.Redis = Depends(get_redis_client)):
    pass

