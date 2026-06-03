import aio_pika
from fastapi import FastAPI
from contextlib import asynccontextmanager
from elasticsearch import AsyncElasticsearch
from app.core.config import settings
from app.routes.order_process import router as order_process_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.elastic_client = AsyncElasticsearch(settings.elasticsearch_url)

    # יצירת חיבור אסנכרוני לרביט
    app.state.rabbitmq_client_async = await aio_pika.connect_robust(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        login=settings.RABBITMQ_DEFAULT_USER,
        password=settings.RABBITMQ_DEFAULT_PASS,
    )
    # יצירת קיו ברביט
    await app.state.rabbitmq_client_async.channel().declare_queue(
        name="order.place", durable=True
    )

    yield

    await app.state.elastic_client.close()
    await app.state.rabbitmq_client_async.close()


app = FastAPI(
    debug=True,
    lifespan=lifespan,
    title="Order Management Service API",
    description="API for managing order processing, publishing, and status updates",
)

app.include_router(router=order_process_router)


# # יצירת חיבור  סנכרוני לרביט
# app.state.rabbitmq_client_sync = pika.BlockingConnection(
#     pika.ConnectionParameters(
#         host=settings.RABBITMQ_HOST,
#         port=settings.RABBITMQ_PORT,
#         credentials=pika.PlainCredentials(
#             username=settings.RABBITMQ_DEFAULT_USER,
#             password=settings.RABBITMQ_DEFAULT_PASS,
#         ),
#     )
# )
