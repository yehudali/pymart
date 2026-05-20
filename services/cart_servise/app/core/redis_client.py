import redis 
from fastapi import Request


def get_redis_client(request: Request) -> redis.Redis:
    return request.app.state.redis_client