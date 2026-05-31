
from typing import Dict
import uuid
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.cart import ProductData

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

class Order(BaseModel):
    order_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    user_id: str
    cart: Dict[str, ProductData]
    status: OrderStatus = OrderStatus.PENDING
