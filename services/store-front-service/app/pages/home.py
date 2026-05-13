# from api.front_conf import Settings
# import streamlit as st
# import requests

# env = Settings()

# def show_catalog_product(CATALOG_SERVICE_URL):
#     try:
#         products = requests.get(f"{CATALOG_SERVICE_URL}/product/").json()
#     except:
#         st.error("לא ניתן להתחבר לשרת")
#         products = []

#     for p in products:
#         with st.container(border=True):
#             st.write(f"**{p['_source']['name']}**")
#             st.write(f"price{p['_source']['price']}")
#             st.write(f"category: {p['_source']['category']}")
#             st.write(f"id_product: {p['_id']}")
#             # st.image("/home/yehuda_linker/pymart/services/store-front-service/app/46")

# st.title("PyMart 🏰⚡☁️")
# st.title("product catalog:")

# show_catalog_product(env.CATALOG_SERVICE_URL)



##################################################################3
################################################################
import streamlit as st

st.title("🏠 עמוד הבית")

# שימוש ב-get ימנע את השגיאה גם אם המשתנה טרם אותחל
token = st.session_state.get("token")

if token:
    st.success("אתה מחובר למערכת!")
    st.info("כעת תוכל לגשת לעמודי הניהול (למשל, הוספת מוצרים) שיתווספו בהמשך.")
else:
    st.info("לא מחובר כרגע")
