from fastapi import FastAPI
from contextlib import asynccontextmanager 
import redis.asyncio
from app.routes.cart_router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis_client =  redis.asyncio.Redis(host='localhost',port= 6379, decode_responses=True)

    yield

    await app.state.redis_client.close()

app = FastAPI(debug=True, lifespan=lifespan)
app.include_router(router=router)