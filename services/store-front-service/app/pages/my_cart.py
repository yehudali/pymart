import streamlit as st
import extra_streamlit_components as stx
import os
import requests

CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://cart-service:8003")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://order-management:8004")

cookie_manager = stx.CookieManager()
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
token = cookie_manager.get(SECRET_KEY)


def get_cart():
    response = requests.get(
        f"{CART_SERVICE_URL}/cart",
        cookies={SECRET_KEY: token}
    )
    if response.status_code == 200:
        return response.json()
    
    # טיפול בשגיאות שנזרקו בהפעלה
    if response.status_code == 401:
        st.warning(" אתה לא מחובר, התחבר מחדש:")
        st.stop()
    response.raise_for_status()
    
    return None


def delete_product(product_id):
    response = requests.delete(
        f"{CART_SERVICE_URL}/cart/product",
        json={"id": product_id},
        cookies={SECRET_KEY: token}
    )
    return response.status_code == 200


def delete_cart():
    response = requests.delete(
        f"{CART_SERVICE_URL}/cart",
        cookies={SECRET_KEY: token}
    )
    return response.status_code == 200


def update_quantity(product_id, quantity):
    response = requests.put(
        f"{CART_SERVICE_URL}/cart/product/quantity",
        json={"product_id": product_id, "quantity": quantity},
        cookies={SECRET_KEY: token}
    )
    return response.status_code == 200


def create_order():
    response = requests.post(
        f"{ORDER_SERVICE_URL}/create_order",
        cookies={SECRET_KEY: token}
    )
    return response.status_code == 200

def main():
    if token:
        st.sidebar.success("☑️סטטוס: מחובר")
    if token is None:
        st.sidebar.warning("❌סטטוס: לא מחובר כרגע")
        st.warning("יש להתחבר כדי לצפות בעגלה")
        return

    st.title("🛒 עגלת הקניות")

    cart = get_cart()

    if cart is None:
        st.error("לא ניתן להתחבר לשרת העגלה")
        return

    products = cart.get("product", {})

    if not products:
        st.info("העגלה ריקה")
        return

    # סיכום עגלה
    col1, col2 = st.columns(2)
    with col1:
        st.metric("סה״כ פריטים", cart.get("sum_products", 0))
    with col2:
        st.metric("סה״כ לתשלום", f"₪{cart.get('cart_amount', 0)}")

    st.divider()

    # רשימת המוצרים
    for product_id, product_data in products.items():
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                st.subheader(product_data.get("name", "—"))
                st.caption(f"id: {product_id}")
                st.metric("מחיר ליחידה", f"₪{product_data.get('price')}")

            with col2:
                new_quantity = st.number_input(
                    "כמות",
                    min_value=1,
                    value=product_data.get("quantity", 1),
                    key=f"qty_{product_id}"
                )
                if st.button("עדכן כמות", key=f"update_{product_id}"):
                    if update_quantity(product_id, new_quantity):
                        st.success("עודכן!")
                        st.rerun()
                    else:
                        st.error("נכשל בעדכון")

            with col3:
                if st.button("🗑️", key=f"delete_{product_id}", help="הסר מוצר"):
                    if delete_product(product_id):
                        st.success("המוצר הוסר!")
                        st.rerun()
                    else:
                        st.error("נכשל בהסרה")

    st.divider()

    if st.button("✅ בצע הזמנה", type="primary"):
        if create_order():
            st.success("ההזמנה בוצעה בהצלחה!")
            st.rerun()
        else:
            st.error("נכשל בביצוע ההזמנה")

    # ריקון עגלה
    if st.button("🗑️ רוקן עגלה", type="secondary"):
        if delete_cart():
            st.success("העגלה רוקנה!")
            st.rerun()
        else:
            st.error("נכשל בריקון העגלה")


if __name__ == "__main__":
    main()