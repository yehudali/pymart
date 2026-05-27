from fastapi import FastAPI
from contextlib import asynccontextmanager 
import redis.asyncio
from elasticsearch import AsyncElasticsearch
from app.routes.cart_router import router as cart_router
from app.routes.order_router import router as order_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO הוצאת ההוסטים והפורטים למשתני סביבה שיתאימו להרצה בסביבות נוספות
    app.state.redis_client =  redis.asyncio.Redis(host='redis',port= 6379, decode_responses=True)
    app.state.elastic_client = AsyncElasticsearch("http://elasticsearch:9200")
    
    yield

    await app.state.redis_client.close()
    await app.state.elastic_client.close()

app = FastAPI(debug=True, lifespan=lifespan, title="Cart Service API", description="API for managing shopping cart and creating orders")

app.include_router(router=order_router)
app.include_router(router=cart_router)