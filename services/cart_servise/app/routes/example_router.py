import redis.asyncio as redis
from fastapi import APIRouter, Depends

from app.repositories.redis_crud import get_items 
from app.core.redis_client import get_redis_client
from app.core.security import checking_basic_user_permissions
from app.schemas.product import AddProductToCart, DeleteProduct, UpdateQuantityProduct

router = APIRouter()

#meir example:
@router.get('/')
def get_all(name: str, redis_client: redis.Redis = Depends(get_redis_client)):
    return get_items(redis=redis_client, name=name)

@router.get("/cart")
def get_all_cart(user_id=Depends(checking_basic_user_permissions)):
    '''מוצרים, כמות מוצרים, ומחיר כולל'''
    pass

@router.post("/cart/product")
def add_product_to_cart(product:AddProductToCart, user_id=Depends(checking_basic_user_permissions), redis_client:redis.Redis = Depends(get_redis_client)):
    pass

@router.delete("/cart/product")
def delete_product_from_cart(product_id:DeleteProduct, user_id=Depends(checking_basic_user_permissions), redis_client:redis.Redis = Depends(get_redis_client)):
    pass

@router.delete("/cart")
def delete_cart(user_id=Depends(checking_basic_user_permissions), redis_client:redis.Redis = Depends(get_redis_client)):
    pass

@router.put("/cart/product/quantity")
def update_quantity(update:UpdateQuantityProduct ,user_id=Depends(checking_basic_user_permissions), redis_client:redis.Redis = Depends(get_redis_client)):
    pass

