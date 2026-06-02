from fastapi import Request
from pika import BlockingConnection



def get_rabbitmq_client(request: Request)-> BlockingConnection:
    return request.app.state.rabbitmq_client