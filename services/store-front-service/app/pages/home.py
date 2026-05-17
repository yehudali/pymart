from api.front_conf import Settings
import streamlit as st
import requests
import os

CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL")

def show_catalog_product(CATALOG_SERVICE_URL):
    try:
        products = requests.get(f"{CATALOG_SERVICE_URL}/product/").json()
    except:
        st.error("לא ניתן להתחבר לשרת")
        products = []
    if products:
        for p in products:
            with st.container(border=True):
                st.write(f"**{p['_source']['name']}**")
                st.write(f"price{p['_source']['price']}")
                st.write(f"category: {p['_source']['category']}")
                st.write(f"id_product: {p['_id']}")
                # st.image("/home/yehuda_linker/pymart/services/store-front-service/app/46")

st.title("PyMart 🏰⚡☁️")
st.title("product catalog:")

show_catalog_product(CATALOG_SERVICE_URL)

