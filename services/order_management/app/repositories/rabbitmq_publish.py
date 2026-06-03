import json
from aio_pika.abc import AbstractChannel
import aio_pika


async def publish_new_order_to_manage_queue(
    order: dict, rabbitmq_channel: AbstractChannel
):
    try:
        order_byte = json.dumps(order).encode("utf-8")
        message = aio_pika.Message(
            body=order_byte, delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        await rabbitmq_channel.default_exchange.publish(
            message, routing_key="order.place"
        )
    except Exception:
        raise
