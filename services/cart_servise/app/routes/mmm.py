import redis.asyncio as redis

from app.repositories.redis_crud import get_items 
from app.core.redis_client import get_redis_client

from fastapi import APIRouter, Depends 

router = APIRouter()

@router.get('/')
def get_all(name: str, redis_client: redis.Redis = Depends(get_redis_client)):
    return get_items(redis=redis_client, name=name)