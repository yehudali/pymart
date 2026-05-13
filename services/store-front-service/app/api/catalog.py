import requests
# from front_conf import Settings

# service_setings = Settings()
# def healthceck_test_Connection_to_dhe_servis():
#     respons = requests.get(f"{service_setings.CATALOG_SERVICE_URL}/health")
#     respons.raise_for_status()
#     return respons.json()



#####################################################################
import requests
import os

# מומלץ בהמשך לשלוף ממשתני סביבה
BASE_URL = os.getenv("API_URL", "http://localhost:8000")

def login_user(email: str, password: str) -> str:
    """מבצע התחברות ומחזיר את הטוקן, או זורק שגיאה במקרה של כישלון"""
    url = f"{BASE_URL}/login"
    payload = {"email": email, "password": password}
    
    response = requests.post(url, json=payload)
    response.raise_for_status()  # יזרוק Exception במקרה של סטטוס 4xx או 5xx
    
    return response.json().get("token")

def get_all_products():
    url = f"{BASE_URL}/product/"
    response = requests.get(url)
    response.raise_for_status()
    
    return response.json()

def get_auth_headers(token: str) -> dict:
    """פונקציית עזר ליצירת Headers לבקשות הדורשות הרשאה בעתיד"""
    return {"Authorization": f"Bearer {token}"}