import requests
import os
from front_conf import Settings
#####################################################################
import requests
import os

BASE_URL = os.getenv("API_URL", "http://localhost:8000")

def login_user(email: str, password: str) -> str:
    url = f"{BASE_URL}/login"
    payload = {"email": email, "password": password}
    
    response = requests.post(url, json=payload)
    response.raise_for_status() 
    
    return response.json().get("token")

def get_all_products():
    url = f"{BASE_URL}/product/"
    response = requests.get(url)
    response.raise_for_status()
    
    return response.json()


###################################

CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL")

def healthceck_test_Connection_to_dhe_servis():
    respons = requests.get(f"{CATALOG_SERVICE_URL}/health")
    respons.raise_for_status()
    return respons.json()

