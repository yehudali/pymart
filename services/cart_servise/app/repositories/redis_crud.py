import redis.asyncio as redis

async def get_items(redis: redis.Redis, name):
    return redis.get(name=name)

