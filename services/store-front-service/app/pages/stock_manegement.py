import streamlit as st
import extra_streamlit_components as stx
import os
import requests

CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL", "http://catalog_management:8000")

cookie_manager = stx.CookieManager()
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
token = cookie_manager.get(SECRET_KEY)


def get_all_products():
    response = requests.get(f"{CATALOG_SERVICE_URL}/product/")
    if response.status_code == 200:
        return response.json()
    return None


def update_stock(product_id, stock_count):
    response = requests.put(
        f"{CATALOG_SERVICE_URL}/product/{product_id}",
        json={"stock_count": stock_count},
        cookies={SECRET_KEY: token}
    )
    return response.status_code == 200


def main():
    if token:
        st.sidebar.success("☑️סטטוס: מחובר")
    if token is None:
        st.sidebar.warning("❌סטטוס: לא מחובר כרגע")
        st.warning("יש להתחבר כדי לגשת לדף זה")
        return

    st.title("🏭 ניהול מלאי")

    products = get_all_products()

    if products is None:
        st.error("לא ניתן להתחבר לשרת הקטלוג")
        return

    if not products:
        st.info("אין מוצרים במערכת")
        return

    st.caption(f"סה״כ מוצרים: {len(products)}")
    st.divider()

    for product in products:
        product_src = product.get("_source", {})
        product_id = product.get("_id")

        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                st.subheader(product_src.get("name", "—"))
                st.caption(f"קטגוריה: {product_src.get('category', '—')}")
                st.caption(f"id: {product_id}")

            with col2:
                st.metric("מחיר", f"₪{product_src.get('price')}")
                current_stock = product_src.get("stock_count", 0)
                st.caption("✅ במלאי" if current_stock > 0 else "❌ אזל")

            with col3:
                new_stock = st.number_input(
                    "מלאי",
                    min_value=0,
                    value=current_stock,
                    key=f"stock_{product_id}"
                )
                if st.button("עדכן", key=f"update_{product_id}"):
                    if update_stock(product_id, new_stock):
                        st.success("עודכן!")
                        st.rerun()
                    else:
                        st.error("נכשל — אין הרשאת אדמין?")


if __name__ == "__main__":
    main()