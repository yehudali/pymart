import json
from aio_pika.abc import AbstractRobustConnection
import aio_pika


async def publish_new_order_to_manage_queue(
    order: dict, rabbitmq_client: AbstractRobustConnection
):
    try:
        channel = rabbitmq_client.channel()
        order_byte = json.dumps(order).encode("utf-8")
        message = aio_pika.Message(
            body=order_byte, delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        await channel.default_exchange.publish(message, routing_key="order.place")
    except Exception:
        raise
