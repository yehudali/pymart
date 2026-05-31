from pydantic import BaseModel
from typing import Optional


class RegisterRequest(BaseModel):
    name: Optional[str] = None
    email: str
    password: str
    is_manager: bool = False  # בהמשך לשנות את זה כדי לא לתת גישה חיצונית להגדרה הזו, אלא רק מתוך המערכת
    address: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str
