import streamlit as st
import extra_streamlit_components as stx
import minio
cookie_manager = stx.CookieManager()


minio_client = Minio(env.MINIO_URL, 
               access_key=env.MINIO_ACCESS_KEY,
                secret_key=env.MINIO_SECRET_KEY, 
                secure=False
                )









# # def init_session_tocken():
# #     if "token" not in st.session_state:
# #         st.session_state.token = None
    

# def main():
    
#     st.title("pymart 🏰⚡☁️")

# if __name__ == "__main__":
#     main()
