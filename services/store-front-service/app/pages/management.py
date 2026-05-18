import streamlit as st
import requests
import os
from catalog import cookie_manager


CATALOG_SERVICE_HOST = os.getenv("CATALOG_SERVICE_HOST", "catalog_management")
API_URL = f"http://{CATALOG_SERVICE_HOST}:8000/"

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
token = cookie_manager.get(SECRET_KEY)
st.info({"token":token})
    
st.title("הוספת מוצר-לאלסטיק")

with st.form("product_form"):
    name = st.text_input("Name")
    description = st.text_area("Description")
    price = st.number_input("Price", min_value=0)
    category = st.text_input("Category")
    stock_count = st.number_input("Stock Count", min_value=0)
    image_url = st.text_input("Image URL")
    
    submit_button = st.form_submit_button("Add Product")

if submit_button:
    payload = {
        "name": name,
        "description": description,
        "price": price,
        "category": category,
        "stock_count": stock_count,
        "image_url": image_url
    }
    
    response = requests.post(f"{API_URL}product/", json=payload, cookies={SECRET_KEY: token})


    if response.status_code == 200:
        st.success(f"המוצר  {payload['name']} התווסף בהצלחה!")
        st.json(response.json())
    else:
        st.error(f"נכשל: {response.status_code}")
        st.write(response.text)



st.title("מחיקת מוצר מאלסטיק")

with st.form("delete_product"):
    product_id = st.text_input("הכנס ID:")
    

    submit_button = st.form_submit_button("מחק מוצר")

if submit_button:

    delete_url = f"{API_URL}product/{product_id}"
    
    response = requests.delete(delete_url, cookies={SECRET_KEY: token})
    
    if response.status_code == 200:
        st.success("המוצר נמחק בהצלחה!")
        st.json(response.json())
    else:
        st.error(f"נכשל במחיקה?: {response.status_code}")
        st.write(response.text)



#######

st.title("עדכון מוצר באלסטיק")

with st.form("update_product"):
    product_id = st.text_input("id")
    name = st.text_input("name")
    description = st.text_area("description")
    price = st.number_input("price")
    category = st.text_input("category")
    stock_count = st.number_input("stock Count")
    image_url = st.text_input("image URL")
    
    submit_button = st.form_submit_button("עדכן מוצר")

if submit_button:
    if product_id.strip():
        payload = {
            "name": name,
            "description": description,
            "price": price,
            "category": category,
            "stock_count": stock_count,
            "image_url": image_url
        }
        
        update_url = f"{API_URL}product/{product_id.strip()}"
        response = requests.put(update_url, json=payload, cookies={SECRET_KEY: token})
        
        if response.status_code == 200:
            st.success("המוצר עודכן בהצלחה!")
            st.json(response.json())
        else:
            st.error(f"נכשל בעדכון: {response.status_code}")
            st.write(response.text)
    else:
        st.warning("לא הוכנס ID ")
# צריך לטפל בעדכון חלקי של מוצר







st.title("שליפת מוצר  לפי ID")

with st.form("get_product_form"):
    product_id = st.text_input("ID")
    
    submit_button = st.form_submit_button("שלוף מוצר")

if submit_button:
    if product_id:
        get_url = f"{API_URL}product/{product_id}"
        
        response = requests.get(get_url, cookies={SECRET_KEY: token})
        
        if response.status_code == 200:
            st.success("המוצר נשלף בהצלחה!")
            st.json(response.json())
        else:
            st.error(f"נכשל : {response.status_code}")
            st.write(response.text)
    else:
        st.warning("נדרש ID ")


st.title("העלאת תמונה")

with st.form("upload_image_form"):
    uploaded_file = st.file_uploader("בחר קובץ PNG", type="png")
    submit_button = st.form_submit_button("העלה תמונה")

if submit_button and uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    
    response = requests.post(f"{API_URL}image", files=files,  cookies={SECRET_KEY: token})
    
    if response.status_code == 200:
        st.success("התמונה הועלתה בהצלחה!")
        st.json(response.json())
    else:
        st.error(f"נכשל בהעלאה: {response.status_code}")
        st.write(response.text)