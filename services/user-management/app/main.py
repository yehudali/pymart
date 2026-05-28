from fastapi import FastAPI
from router import router
import uvicorn

app = FastAPI(debug=True, title="User Management Service API", description="API for managing user registration, authentication, and profile management")
app.include_router(router=router)

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)