from fastapi import FastAPI
import uvicorn
import router_product
import router_image


from elasticsearch_file import elasticsearch_helthchack



app = FastAPI()


@app.get("/")
async def tetsing():
    return {"message": "catalog api"}

@app.get("/health")
async def health_check():
    elastic_response = elasticsearch_helthchack()
    return {"elasticsearch is connected?": elastic_response}

app.include_router(router_product.router)
app.include_router(router_image.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)