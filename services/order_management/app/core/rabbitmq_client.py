from fastapi import Request
from aio_pika.abc import AbstractRobustConnection, AbstractChannel

# החזרת חיבור
def get_rabbitmq_client(request: Request)-> AbstractRobustConnection:
    return request.app.state.rabbitmq_client_async

# החזרת צ'אנל
def get_rabbitmq_channel(request: Request)-> AbstractChannel:
    return request.app.state.rabbitmq_channel