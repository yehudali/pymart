from fastapi import Depends, HTTPException, Request
import os

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")

def get_user(request: Request):
    token = request.cookies.get(SECRET_KEY)
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token

def get_admin_user(request: Request):
    token = request.cookies.get(SECRET_KEY)
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    # צריך לקבל מאלסטיק את המשתמש ולבדוק אם הוא אדמין, או לא- כן עובר, לא-נכשל
    #

    from elasticsearch_file import es
    return token