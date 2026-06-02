import json
from pika.adapters.blocking_connection import BlockingConnection


def publish_new_order_to_manage_queue(order: dict, rabbitmq_client: BlockingConnection):
    try:
        channel = rabbitmq_client.channel()
        order_byte = json.dumps(order).encode("utf-8")

        channel.basic_publish(exchange="", routing_key="order.place", body=order_byte)
    except Exception:
        raise
