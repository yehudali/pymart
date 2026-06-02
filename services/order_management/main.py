import pika
from fastapi import FastAPI
from contextlib import asynccontextmanager
from elasticsearch import AsyncElasticsearch
from app.core.config import settings
from app.routes.order_process import router as order_process_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.elastic_client = AsyncElasticsearch(settings.elasticsearch_url)

    # יצירת חיבור לרביט
    app.state.rabbitmq_client = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=pika.PlainCredentials(
                username=settings.RABBITMQ_DEFAULT_USER,
                password=settings.RABBITMQ_DEFAULT_PASS,
            ),
        )
    )
    # יצירת קיו ברביט
    app.state.rabbitmq_client.channel().queue_declare(queue="order.place", durable=True)

    yield

    await app.state.elastic_client.close()
    await app.state.elastic_client.close()


app = FastAPI(
    debug=True,
    lifespan=lifespan,
    title="Order Management Service API",
    description="API for managing order processing, publishing, and status updates",
)

app.include_router(router=order_process_router)
