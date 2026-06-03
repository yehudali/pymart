import streamlit as st
import extra_streamlit_components as stx
import os
import requests

ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://order-service:8004")

cookie_manager = stx.CookieManager()
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
token = cookie_manager.get(SECRET_KEY)


def get_orders():
    response = requests.get(
        f"{ORDER_SERVICE_URL}/orders",
        cookies={SECRET_KEY: token}
    )
    if response.status_code == 200:
        return response.json()
    return None


def main():
    if token:
        st.sidebar.success("☑️סטטוס: מחובר")
    if token is None:
        st.sidebar.warning("❌סטטוס: לא מחובר כרגע")
        st.warning("יש להתחבר כדי לצפות בהזמנות")
        return

    st.title("ההזמנות שלי")

    orders = get_orders()

    if orders is None:
        st.error("לא ניתן להתחבר לשרת ההזמנות")
        return

    if not orders:
        st.info("אין הזמנות עדיין")
        return

    st.caption(f"סך הזמנות: {len(orders)}")
    st.write("פירוט הזמנות")
    st.divider()

    for order in orders:
        with st.expander(f"הזמנה: {order.get('order_id', '—')} | סטטוס: {order.get('status', '—')}"):
            
    
            st.markdown(f"**תאריך יצירה:** {order.get('created_at', '—')}")
            st.markdown(f"**אימייל:** {order.get('email', '—')}")
            
            st.divider()
            st.markdown("**מוצרים:**")
            
            cart = order.get("cart", {})
    
            for product in cart.values():
                name = product.get('name', '—')
                quantity = product.get('quantity', 0)
                price = product.get('price', 0.0)
                
                st.markdown(f"- **{name}** | כמות: {quantity} | מחיר: {price}")

if __name__ == "__main__":
    main()
