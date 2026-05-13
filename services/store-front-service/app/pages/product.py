######################################
# ################################
# 
import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.catalog import get_all_products

st.title("🛍️ קטלוג מוצרים")
st.write("צפייה במוצרים זמינה לכל המשתמשים.")

# st.divider()

# try:
#     with st.spinner("טוען מוצרים..."):
#         products = get_all_products()
        
#     if not products:
#         st.info("לא נמצאו מוצרים במערכת.")
#     else:
#         # פריסה של 3 מוצרים בשורה לקריאות טובה
#         cols = st.columns(3)
        
#         for index, item in enumerate(products):
#             source = item.get("_source", {})
#             name = source.get("name", "ללא שם")
#             price = source.get("price", 0.0)
#             category = source.get("category", "כללי")
#             stock = source.get("stock_count", 0)
#             image_url = source.get("image_url")

#             # שימוש בעמודה הנכונה לפי האינדקס
#             with cols[index % 3]:
#                 st.subheader(name)
                
#                 # הצגת התמונה אם קיימת ואינה null
#                 if image_url:
#                     st.image(image_url, use_container_width=True)
#                 else:
#                     st.info("אין תמונה")
                    
#                 st.markdown(f"**מחיר:** ₪{price}")
#                 st.markdown(f"**קטגוריה:** {category}")
#                 st.markdown(f"**מלאי:** {stock} יחידות")
#                 st.write("---")

# except Exception as e:
#     st.error(f"שגיאה בשליפת הנתונים מהשרת. האם השרת למטה?")