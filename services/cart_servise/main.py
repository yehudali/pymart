from fastapi import FastAPI
from contextlib import asynccontextmanager 
import redis.asyncio
from elasticsearch import AsyncElasticsearch
from app.routes.cart_router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO הוצאת ההוסטים והפורטים למשתני סביבה שיתאימו להרצה בסביבות נוספות
    app.state.redis_client =  redis.asyncio.Redis(host='localhost',port= 6379, decode_responses=True)
    app.state.elastic_client = AsyncElasticsearch([{'host': 'localhost', 'port': 9200}])
    yield

    await app.state.redis_client.close()
    await app.state.elastic_client.close()

app = FastAPI(debug=True, lifespan=lifespan)
app.include_router(router=router)