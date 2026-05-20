import redis.asyncio as redis
from fastapi import APIRouter, Depends

from app.repositories.redis_crud import get_items 
from app.core.redis_client import get_redis_client
from app.core.security import checking_basic_user_permissions
from app.schemas.product import AddProductToCart

router = APIRouter()

#meir example:
@router.get('/')
def get_all(name: str, redis_client: redis.Redis = Depends(get_redis_client)):
    return get_items(redis=redis_client, name=name)


@router.post("/cart/product")
def add_product_to_cart(prduct:AddProductToCart, user_id=Depends(checking_basic_user_permissions)):
    pass

