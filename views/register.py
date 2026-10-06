import streamlit as st

from utils.ui import load_css
from utils.auth import register_user


def show():

    load_css()

    _, mid, _ = st.columns([1, 1.2, 1])

    with mid:

        st.markdown("<div class='auth-wrap'>", unsafe_allow_html=True)

        st.markdown(
            "<div class='auth-icon'>📝</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <h1 class='title'>Register Akun</h1>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <p class='subtitle'>
            Silakan buat akun terlebih dahulu
            </p>
            """,
            unsafe_allow_html=True
        )

        with st.container(border=True):

            nama = st.text_input(
                "Nama Lengkap",
                placeholder="Masukkan nama lengkap"
            )

            username = st.text_input(
                "Username",
                placeholder="Masukkan username"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            confirm = st.text_input(
                "Konfirmasi Password",
                type="password"
            )

            st.write("")

            col1, col2 = st.columns(2)

            with col1:

                if st.button("Daftar", use_container_width=True):

                    if nama == "" or username == "" or password == "":

                        st.error("Semua data wajib diisi.")

                    elif password != confirm:

                        st.error("Konfirmasi password tidak sama.")

                    else:

                        success = register_user(
                            nama,
                            username,
                            password
                        )

                        if success:

                            st.success("Akun berhasil dibuat.")

                            st.session_state.page = "login"

                            st.rerun()

                        else:

                            st.error("Username sudah digunakan.")

            with col2:

                if st.button("Kembali", use_container_width=True):

                    st.session_state.page = "login"

                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)