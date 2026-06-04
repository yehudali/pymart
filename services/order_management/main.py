import asyncio
import aio_pika
from fastapi import FastAPI
from contextlib import asynccontextmanager
from elasticsearch import AsyncElasticsearch
from app.core.config import settings
from app.routes.order_process import router as order_process_router


async def init_rabbitmq(app, queue_name: str):
    """אתחול חיבור עם מנגנון רה-טריי לרביט, ויצירת תור"""
    retries = 5
    for i in range(retries):
        try:
            app.state.rabbitmq_client_async = await aio_pika.connect_robust(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                login=settings.RABBITMQ_DEFAULT_USER,
                password=settings.RABBITMQ_DEFAULT_PASS,
            )

            channel = await app.state.rabbitmq_client_async.channel()
            
            # 3. יצירת התור
            await channel.declare_queue(name=queue_name, durable=True)
            
            
            app.state.rabbitmq_channel = channel

            # אם התהליך הושלם:
            break

        except Exception:
            print("RabbitMQ is not ready yet. Retrying in 3 seconds...")
            await asyncio.sleep(5)
    else:
        # העלאת חריג במידה וכל הנסיונות כשלו
        raise Exception("Failed to connect to RabbitMQ after maximum retries.")



@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.elastic_client = AsyncElasticsearch(hosts=settings.ELASTICSEARCH_URL)

    await init_rabbitmq(app, queue_name="order.place")

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


# למחוק בסוף הבדיקות:
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
