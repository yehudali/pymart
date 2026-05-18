from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
import router_product
import router_image
import route_healthcheck


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("dhe app is starting up...")
    yield
    print("dhe app is shutting down...")

app = FastAPI(lifespan=lifespan)


app.include_router(route_healthcheck.router)
app.include_router(router_product.router)
app.include_router(router_image.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)