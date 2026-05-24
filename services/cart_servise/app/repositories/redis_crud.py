import redis.asyncio as redis
import json

async def get_items(redis_client: redis.Redis, name):
    return redis_client.get(name=name)

async def save_product_in_cart(user_id:str, product_id:str, quantity_product:int,  product_price:float, product_name:str, redis_client: redis.Redis):
    product_data = {
        "name":product_name,
        "price": product_price,
        "quantity":quantity_product
    }
    product_data_json= json.dumps(product_data)
   
    async with redis_client.pipeline() as pipe:
        redis_client.hset(name=user_id, key=product_id, value=product_data_json)        # type: ignore
        redis_client.expire(name=user_id ,time=86000)

        await pipe.execute()
    
