from fastapi import FastAPI
from contextlib import asynccontextmanager
from elasticsearch import AsyncElasticsearch
from app.core.config import settings
from app.routes.order_process import router as order_process_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    
    app.state.elastic_client = AsyncElasticsearch(settings.elasticsearch_url)
    
    yield

    await app.state.elastic_client.close()

app = FastAPI(debug=True, lifespan=lifespan, title="Order Management Service API", description="API for managing order processing, publishing, and status updates")

app.include_router(router=order_process_router)