from fastapi import FastAPI
from contextlib import asynccontextmanager 
import redis
from app.routes.mmm import router

def lifespan(app: FastAPI):
    app.state.redis_client = redis.Redis()

    yield

    app.state.redis_client.close()

app = FastAPI(debug=True)
app.include_router(router=router)