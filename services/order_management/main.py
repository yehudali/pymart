from fastapi import FastAPI
from contextlib import asynccontextmanager 
import redis.asyncio
from elasticsearch import AsyncElasticsearch
from app.routes.order_process import router as order_process_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO הוצאת ההוסטים והפורטים למשתני סביבה שיתאימו להרצה בסביבות נוספות
    app.state.elastic_client = AsyncElasticsearch("http://elasticsearch:9200")
    
    yield

    await app.state.elastic_client.close()

app = FastAPI(debug=True, lifespan=lifespan, title="Order Management Service API", description="API for managing order processing, publishing, and status updates")

app.include_router(router=order_process_router)