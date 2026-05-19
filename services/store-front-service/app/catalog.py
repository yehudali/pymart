import streamlit as st
import extra_streamlit_components as stx
from minio import Minio
import os
import requests

MINIO_URL = os.getenv("MINIO_URL")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL", "http://catalog_management:8000")

cookie_manager = stx.CookieManager()
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
token = cookie_manager.get(SECRET_KEY)

COLS = 3  ## מספר המוצרים בכל שורה

def render_product(product):
    src = product.get("_source", {})
    with st.container(border=True):
        image_url = f"{CATALOG_SERVICE_URL}/image/{src.get('name', '')}.png"
        response = requests.get(image_url)
        if response.status_code == 200:
            st.image(response.content, use_container_width=True)
        else:
            st.image("https://placehold.co/300x200?text=No+Image", use_container_width=True)

        st.subheader(src.get("name", "—"))
        st.caption(f" {src.get('category')}")
        st.metric("מחיר", f"₪{src.get('price')}")
        st.caption(f" {product.get('_id')}")

def main():
    if token:
        st.warning(token)
        st.sidebar.success("☑️סטטוס: מחובר")
    if token == None:
        st.sidebar.warning("❌סטטוס: לא מחובר כרגע")
    

    st.title("pymart 🏰⚡☁️")

    try:
        products = requests.get(
            f"{CATALOG_SERVICE_URL}/product/").json()
    except Exception:
        st.error("לא ניתן להתחבר לשרת")
        return

    if not products:
        st.info("אין מוצרים להצגה.")
        return

    cols = st.columns(COLS)
    for i, product in enumerate(products):
        with cols[i % COLS]:
            render_product(product)

if __name__ == "__main__":
    main()