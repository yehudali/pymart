import streamlit as st
import requests
import os
from catalog import cookie_manager


st.title("פרופיל משתמש")

USER_SERVICE_HOST = os.getenv("USER_SERVICE_HOST", "user_management")
API_URL = f"http://{USER_SERVICE_HOST}:8001/"

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")

token = cookie_manager.get(SECRET_KEY)

if token:
    st.info("זוהה משתמש מחובר במערכת.")
    
    if st.button("הצג את הפרופיל שלי"):
        response = requests.get(f"{API_URL}profile", params={"token": token})
        
        if response.status_code == 200:
            st.success("הפרופיל נשלף בהצלחה!")
            st.json(response.json())
        else:
            st.error(f"שגיאה בשליפה: {response.status_code}")
            st.write(response.text)
else:
    st.warning("לא נמצא טוקן פעיל! אנא התחבר קודם בחלונית ההתחברות.")