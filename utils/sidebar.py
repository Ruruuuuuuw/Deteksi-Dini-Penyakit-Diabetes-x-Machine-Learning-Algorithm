import os
import streamlit as st

from database import get_connection


def show_sidebar():

    user = st.session_state.user

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user["id"],)
    )

    data = cursor.fetchone()

    conn.close()

    with st.sidebar:

        st.markdown(
            """
            <h2 style='text-align:center;'>
            🩺 Diabetes Risk Prediction
            </h2>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        # ==========================================
        # FOTO PROFIL
        # ==========================================

        foto = data["foto"]

        if foto:

            foto_path = os.path.join(
                "assets",
                "profile",
                foto
            )

            if os.path.exists(foto_path):

                st.image(
                    foto_path,
                    width=150
                )

            else:

                st.image(
                    "assets/profile/default.png",
                    width=150
                )

        else:

            st.image(
                "assets/profile/default.png",
                width=150
            )

        st.markdown(
            f"""
            <h3 style='text-align:center;margin-bottom:0'>
            {data["nama"]}
            </h3>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <p style='text-align:center;color:gray'>
            @{data["username"]}
            </p>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        # ==========================================
        # MENU
        # ==========================================

        if st.button(
            "🏠  Dashboard",
            key="sidebar_dashboard",
            use_container_width=True
        ):

            st.session_state.page = "dashboard"
            st.rerun()

        if st.button(
            "🩺  Prediksi",
            key="sidebar_prediction",
            use_container_width=True
        ):

            st.session_state.page = "prediction"
            st.rerun()

        if st.button(
            "📈  Riwayat Prediksi",
            key="sidebar_history",
            use_container_width=True
        ):

            st.session_state.page = "history"
            st.rerun()

        if st.button(
            "👤  Profil",
            key="sidebar_profile",
            use_container_width=True
        ):

            st.session_state.page = "profile"
            st.rerun()

        st.divider()

        if st.button(
            "🚪  Logout",
            key="sidebar_logout",
            use_container_width=True
        ):

            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()

        st.divider()

        st.caption("Version 1.0")
        st.caption("© 2026 Diabetes Risk Prediction")