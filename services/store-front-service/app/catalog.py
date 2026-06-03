import streamlit as st
import extra_streamlit_components as stx
from minio import Minio
import os
import requests

MINIO_URL = os.getenv("MINIO_URL")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL", "http://catalog_management:8000")
CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://cart-service:8003")

st.set_page_config(page_title="Pymart", page_icon="🏰", layout="wide")

cookie_manager = stx.CookieManager()
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
token = cookie_manager.get(SECRET_KEY)

COLS = 3  ## מספר המוצרים בכל שורה


def search_by_name():
    with st.expander("חיפוש מוצר לפי שם"):
        product_name = st.text_input("הכנס שם מוצר", key="search_name_input")

        if st.button("שלוף מוצר", key="search_name_btn"):
            if not product_name:
                st.warning("נדרש שם מוצר")
                return

            response = requests.get(
                f"{CATALOG_SERVICE_URL}/product/name/{product_name}",
                cookies={SECRET_KEY: token},
            )

            if response.status_code != 200:
                st.error(f"מוצר לא נמצא ({response.status_code})")
                return

            product = response.json()
            product_src = product.get("_source", {})

            image_url = f"{CATALOG_SERVICE_URL}/image/{product_src.get('name', '')}.png"
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                st.image(img_response.content, width=250)
            else:
                st.image("https://placehold.co/300x200?text=No+Image", width=250)

            st.subheader(product_src.get("name", "—"))
            st.caption(f"קטגוריה: {product_src.get('category', '—')}")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("מחיר", f"₪{product_src.get('price')}")
            with col2:
                stock = product_src.get("stock_count", 0)
                st.metric("מלאי", "✅ במלאי" if stock > 0 else "❌ אזל")

            st.markdown(f"**תיאור** {product_src.get('description', 'אין תיאור')}")


@st.dialog("פרטי מוצר")
def show_product_dialog(product):
    product_src = product.get("_source", {})
    product_id = product.get("_id")

    image_url = f"{CATALOG_SERVICE_URL}/image/{product_src.get('name', '')}.png"
    response = requests.get(image_url)
    if response.status_code == 200:
        st.image(response.content, use_container_width=True)
    else:
        st.image("https://placehold.co/300x200?text=No+Image", use_container_width=True)

    st.subheader(product_src.get("name", "—"))
    st.caption(f"קטגוריה: {product_src.get('category', '—')}")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("מחיר", f"₪{product_src.get('price')}")
    with col2:
        stock = product_src.get("stock_count", 0)
        st.metric("מלאי", "✅ במלאי" if stock > 0 else "❌ אזל")

    st.markdown(f"** תיאור:** {product_src.get('description', 'אין תיאור')}")

    st.divider()

    quantity = st.number_input(
        "כמות:", min_value=1, value=1, key=f"dialog_qty_{product_id}"
    )
    if st.button("הוסף לעגלה", key=f"dialog_btn_{product_id}"):
        payload = {
            "id": product_id,
            "name": product_src.get("name"),
            "price": product_src.get("price"),
            "quantity": quantity,
        }
        response = requests.post(
            f"{CART_SERVICE_URL}/cart/product",
            json=payload,
            cookies={SECRET_KEY: token},
        )
        if response.status_code == 200:
            st.success(f"נבחרו {quantity} יחידות להוספה!")
        else:
            st.error("נכשל בהוספת המוצר לעגלה")


def render_product(product):
    product_src = product.get("_source", {})
    product_id = product.get("_id")

    with st.container(border=True):
        image_url = f"{CATALOG_SERVICE_URL}/image/{product_src.get('name', '')}.png"
        response = requests.get(image_url)
        if response.status_code == 200:
            st.image(response.content, use_container_width=True)
        else:
            st.image(
                "https://placehold.co/300x200?text=No+Image", use_container_width=True
            )

        st.subheader(product_src.get("name", "—"))
        st.caption(f"קטגוריה: {product_src.get('category', '—')}")
        st.metric("מחיר", f"₪{product_src.get('price')}")

        stock = product_src.get("stock_count", 0)
        st.caption("✅ במלאי" if stock > 0 else "❌ אזל")

        st.caption(f"id: {product_id}")

        quantity = st.number_input("כמות:", min_value=1, value=1, key=f"a_{product_id}")
        if st.button("הוסף לעגלה", key=f"button_{product_id}"):
            payload = {
                "id": product_id,
                "name": product_src.get("name"),
                "price": product_src.get("price"),
                "quantity": quantity,
            }
            response = requests.post(
                f"{CART_SERVICE_URL}/cart/product",
                json=payload,
                cookies={SECRET_KEY: token},
            )
            if response.status_code == 200:
                st.write(f"נבחרו {quantity} יחידות להוספה!")
            else:
                st.write("נכשל בהוספת המוצר לעגלה")

        if st.button("מפרט המוצר", key=f"details_{product_id}"):
            show_product_dialog(product)


def main():
    # חיווי התחברות למשתמש
    if token:
        st.sidebar.success("☑️סטטוס: מחובר")
    if token is None:
        st.sidebar.warning("❌סטטוס: לא מחובר כרגע")

    st.title("pymart")

    # שליפת כל המוצרים מהקטלוג
    try:
        products = requests.get(f"{CATALOG_SERVICE_URL}/product/").json()
    except Exception:
        st.error("לא ניתן להתחבר לשרת")
        return

    if not products:
        st.info("אין מוצרים להצגה.")
        return

    # הוספת אפשרות חיפוש מוצר לפי name
    search_by_name()

    # תצוגת כל המוצרים  מחולקים לעמודות
    cols = st.columns(COLS)
    for i, product in enumerate(products):
        with cols[i % COLS]:
            render_product(product)


if __name__ == "__main__":
    main()
