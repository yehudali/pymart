import uuid
from fastapi import APIRouter, HTTPException
from elasticshearch_file import elasic_instance
from schemas import RegisterRequest, LoginRequest
from tokens_file import (
    find_user_by_email,
    make_token,
    get_user_id_from_token,
    get_user_by_id,
)

router = APIRouter()


@router.post("/user")
def create_user(data: RegisterRequest):

    # check if email is exists:
    id, user = find_user_by_email(data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # create user:
    user_id = str(uuid.uuid4())
    user_dict = data.model_dump()
    elasic_instance.es.index(index="users", id=user_id, body=user_dict)

    return {"user_id": user_id, "name": data.name, "email": data.email}


@router.post("/login")
def login(data: LoginRequest):
    user_id, user = find_user_by_email(data.email)
    if not user or not data.password == user["password"]:  # do hash!
        raise HTTPException(
            status_code=401, detail="Can't login pasword or email is wrong"
        )

    is_manager = user.get("is_manager")
    token = make_token(user_id, is_manager)
    return {"token": token}


@router.get("/profile")
def get_profile(token: str):
    user_id = get_user_id_from_token(token)
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="user not found")
    return {
        "user_id": user_id,
        "name": user.get("name"),
        "email": user.get("email"),
        "address": user.get("address"),
        "is_manager": user.get("is_manager"),
    }
