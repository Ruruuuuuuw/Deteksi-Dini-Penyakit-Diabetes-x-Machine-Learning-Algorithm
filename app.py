import streamlit as st

from database import create_tables, add_foto_column

from views.login import show as show_login
from views.register import show as show_register
from views.dashboard import show as show_dashboard
from views.prediction import show as show_prediction
from views.history import show as show_history
from views.profile import show as show_profile

# ==========================================
# KONFIGURASI
# ==========================================

st.set_page_config(
    page_title="Diabetes Risk Prediction",
    page_icon="🩺",
    layout="wide"
)

create_tables()
add_foto_column()

# ==========================================
# SESSION
# ==========================================

if "page" not in st.session_state:
    st.session_state.page = "login"

if "user" not in st.session_state:
    st.session_state.user = None

# ==========================================
# ROUTING
# ==========================================

if st.session_state.page == "login":

    show_login()

elif st.session_state.page == "register":

    show_register()

elif st.session_state.page == "dashboard":

    show_dashboard()

elif st.session_state.page == "prediction":

    show_prediction()

elif st.session_state.page == "history":

    show_history()

elif st.session_state.page == "profile":
    show_profile()