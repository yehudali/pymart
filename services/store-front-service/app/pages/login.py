import extra_streamlit_components as stx
import streamlit as st
import os
import requests
from schemas import LoginRequest
from main import cookie_manager





def get_login_service_name():
    return os.getenv("LOGIN_SERVICE_URL", "http://localhost:8001")

def login_process(data:LoginRequest):
    LOGIN_SERVICE_NAME = get_login_service_name()

    SECRET_KEY = os.getenv("SECRET_KEY")
    token = requests.post(f"http://{LOGIN_SERVICE_NAME}:8001/login", json=data.model_dump()).json().get("token")

    cookie_manager.set(SECRET_KEY, token)

    

with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("PAssword")
        submitted = st.form_submit_button("התחבר")
        if submitted:
            if not email or not password:
                st.warning("!מלא את 2 השדות")
            else:
                try:
                    login_process(LoginRequest(email=email, password=password)) 
                    st.success("התחברת בהצלחה!")   
                except Exception as e:
                    st.error(f"התחברות נכשלה: {e}")































########################
#########################3
#####################
# import streamlit as st
# import sys
# import os

# # הוספת תיקיית app לנתיב כדי לאפשר יבוא נקי של שכבת ה-API
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from api.catalog import login_user

# st.title("🔐 התחברות למערכת")

# with st.form("login_form"):
#     email = st.text_input("אימייל")
#     password = st.text_input("סיסמה")
#     submitted = st.form_submit_button("התחבר")

# if submitted:
#     if not email or not password:
#         st.warning("מלא את 2 השדות")
#     else:
#         try:
#             with st.spinner("מתחבר..."):
#                 token = login_user(email, password)
#                 print("Received token:", token)  # Debug log

#                 st.session_state.token = token
#                 st.success("התחברת בהצלחה!")
#         except Exception as e:
#             st.error("התחברות נכשלה. אנא בדוק את פרטי הגישה.")




            # הרשמה 
            # והתחברות

