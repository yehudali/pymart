import extra_streamlit_components as stx
from catalog import cookie_manager
import streamlit as st
import requests
import os

USER_SERVICE_HOST = os.getenv("USER_SERVICE_HOST", "user_management")
API_URL = f"http://{USER_SERVICE_HOST}:8001/"

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
token = cookie_manager.get(SECRET_KEY)

st.title("צור משתמש")
with st.form("create_user_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password")
    is_manager = st.checkbox("Is Manager?")
    address = st.text_input("Address")
    
    submit_button = st.form_submit_button("צור משתמש")

if submit_button:
    payload = {
        "name": name,
        "email": email,
        "password": password,
        "is_manager": is_manager,
        "address": address
    }
    
    response = requests.post(f"{API_URL}user", json=payload, cookies={SECRET_KEY: token})
    
    if response.status_code == 200:
        st.success(f"המשתמש {payload['name']} נוצר בהצלחה!")
        st.json(response.json())
    else:
        st.error(f"נכשל: {response.status_code}")
        st.write(response.text)


st.title("התחברות (Login)")


with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password")

    submit_button = st.form_submit_button("התחבר")

if submit_button:
    if email and password:
        payload = {
            "email": email,
            "password": password
        }
        
        response = requests.post(f"{API_URL}login", json=payload, cookies={SECRET_KEY: token})
        
        if response.status_code == 200:
            st.success("התחברת בהצלחה!")
            response_data = response.json()
            st.json(response_data)

            token = response_data.get("token")
            if token:
                cookie_manager.set(SECRET_KEY, token)
                st.info("הטוקן נשמר בקוקיז!")
        else:
            st.error(f"התחברות נכשלה: {response.status_code}")
            st.write(response.text)



