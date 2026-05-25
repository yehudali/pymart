import redis.asyncio as redis
import json
from dataclasses import dataclass, asdict
from app.schemas.product import CreateItemDTO

# async def get_items(redis_client: redis.Redis, name):
#     return redis_client.get(name=name)


async def save_product_in_cart(user_id:str, product_id:str, product_data:CreateItemDTO, redis_client: redis.Redis):

    product_json_data = json.dumps(asdict(product_data))

    async with redis_client.pipeline() as pipe:

        pipe.hset(name=user_id, key=product_id, value=product_json_data)        # type: ignore
        pipe.expire(name=user_id ,time=86000)

        await pipe.execute()
        return asdict(product_data)
    

async def product_exists(user_id:str, product_id:str, redis_client:redis.Redis)->bool:
    return await redis_client.hexists(name=user_id, key=product_id) # type: ignore


async def delete_product_from_cart(user_id:str, product_id:str, redis_client:redis.Redis):
    return await redis_client.hdel(user_id, product_id)  # type: ignore

async def delete_cart(user_id:str, redis_client:redis.Redis):
    return await redis_client.delete(user_id)

async def update_product_quantity(user_id:str, product_id:str, quantity:int, redis_client:redis.Redis):
    """
    עדכון כמות של מוצר
    1.קבלת המידע מרדיס
    2. אם לא קיים החזר שגיאה
    3. עדכון השדה
    4. עדכון המוצר עם הכמות (בלבד..) המעודכנת
    5. עדכון TTL
    """
    raw_data = await redis_client.hget(name=user_id, key=product_id) # type: ignore
    if not raw_data:
        raise ValueError(f"product {product_id} not found in cart of user {user_id}")
    try:
        product_data_json = json.loads(raw_data)
        product_data_json['quantity']= quantity
        product_data_str = json.dumps(product_data_json)
    except Exception as e:
        raise ValueError(e)
    
    async with redis_client.pipeline() as pipe:
        pipe.hset(name=user_id, key=product_id, value=product_data_str)
        pipe.expire(name=user_id, time=86000)

        await pipe.execute()

        return product_data_json

