import streamlit as st

from utils.ui import load_css
from utils.auth import login_user


def show():

    load_css()

    _, mid, _ = st.columns([1, 1.2, 1])

    with mid:

        st.markdown("<div class='auth-wrap'>", unsafe_allow_html=True)

        st.markdown(
            "<div class='auth-icon'>🩺</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <h1 class='title'>Diabetes Risk Prediction</h1>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <p class='subtitle'>
            Sistem Deteksi Dini Risiko Diabetes
            </p>
            """,
            unsafe_allow_html=True
        )

        with st.container(border=True):

            username = st.text_input(
                "Username",
                placeholder="Masukkan Username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Masukkan Password"
            )

            st.write("")

            col1, col2 = st.columns(2)

            with col1:

                if st.button("Login", use_container_width=True):

                    user = login_user(
                        username,
                        password
                    )

                    if user:

                        st.session_state.user = user

                        st.success("Login berhasil!")

                        st.session_state.page = "dashboard"

                        st.rerun()

                    else:

                        st.error("Username atau Password salah.")

            with col2:

                if st.button("Daftar", use_container_width=True):

                    st.session_state.page = "register"

                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)