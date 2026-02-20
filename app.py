import streamlit as st
from services.auth import login, logout, require_auth
from utils.logger import setup_logger

logger = setup_logger()

st.set_page_config(page_title="Enterprise Dashboard", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    login()
else:
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Analytics", "Admin", "Logout"])

    if page == "Dashboard":
        from pages.dashboard import show_dashboard
        show_dashboard()

    elif page == "Analytics":
        from pages.analytics import show_analytics
        show_analytics()

    elif page == "Admin":
        require_auth(role="admin")
        from pages.admin import show_admin
        show_admin()

    elif page == "Logout":
        logout()
