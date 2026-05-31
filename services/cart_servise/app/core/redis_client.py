import redis.asyncio 
from fastapi import Request


async def get_redis_client(request: Request) -> redis.asyncio.Redis:
    return await request.app.state.redis_client