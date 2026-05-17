from fastapi import Depends, HTTPException, Request
import os
from jose import jwt

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")

# בדיקת הטוקן
# פונקציות זהות שצריכות להיות משותפות בין  2  סרוויסים
def get_user_id_from_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except Exception as err:
        print(err)
        return None
    
def check_administrator_by_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY,  algorithms=["HS256"])
        return payload["is_manager"]
    except Exception as err:
        print(err)
        return None




# 
def checking_basic_user_permissions(request: Request):
    token = request.cookies.get(SECRET_KEY)
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_id = get_user_id_from_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized- Token not supported")
    return user_id

def check_if_is_admin_user(request: Request):
    token = request.cookies.get(SECRET_KEY)
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized not token")
    
    is_manager = check_administrator_by_token(token)
    if is_manager == True:
        return True
    else:
        raise HTTPException(status_code=401, detail="Unauthorized-No administrative permission ")
    