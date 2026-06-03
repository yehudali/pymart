from fastapi import Request
from aio_pika.abc import AbstractRobustConnection


def get_rabbitmq_client(request: Request)-> AbstractRobustConnection:
    return request.app.state.rabbitmq_client_async