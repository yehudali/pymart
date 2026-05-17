import streamlit as st
import extra_streamlit_components as stx
from minio import Minio
import os
import requests

MINIO_URL = os.getenv("MINIO_URL")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

CATALOG_SERVICE_URL= os.getenv("CATALOG_SERVICE_URL", "http://catalog_management:8000")


cookie_manager = stx.CookieManager()

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
token = cookie_manager.get(SECRET_KEY)


minio_client = Minio(MINIO_URL, 
               access_key=MINIO_ACCESS_KEY,
                secret_key=MINIO_SECRET_KEY, 
                secure=False
                )


def main():
    st.title("pymart 🏰⚡☁️")


    try:
        products = requests.get(f"{CATALOG_SERVICE_URL}/product/", cookies={SECRET_KEY: token}).json()
    except:
        st.error("לא ניתן להתחבר לשרת")
        products = []
    if products:
        for p in products:
            with st.container(border=True):
                st.write(p)


                st.write(f"price{p['_source']['price']}")
                st.write(f"category: {p['_source']['category']}")
                st.write(f"id_product: {p['_id']}")
                image = minio_client.presigned_get_object("product", "Bananas.png") # object_name=f"{p['_source']['name']}.png"
                st.write(image)
                st.image(image, width=100)

if __name__ == "__main__":
    main()
