from fastapi import FastAPI
from contextlib import asynccontextmanager 
import redis
from app.routes.example_router import router

def lifespan(app: FastAPI):
    app.state.redis_client = redis.Redis(host='localhost',port= 6379)

    yield

    app.state.redis_client.close()

app = FastAPI(debug=True)
app.include_router(router=router)