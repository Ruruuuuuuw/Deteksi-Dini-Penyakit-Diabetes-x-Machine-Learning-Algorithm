import os
import shutil

import streamlit as st

from utils.ui import load_css
from utils.sidebar import show_sidebar

from database import (
    get_connection,
    get_total_prediction,
    update_user_name
)


def show():

    load_css()
    show_sidebar()

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

    st.markdown(
        "<span class='badge-pill'>👤 Akun Anda</span>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h1 class='title'>
        Profil Pengguna
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # ==========================================
    # FOTO PROFIL
    # ==========================================

    with st.container(border=True):

        st.markdown("<span class='marker-brand'></span>", unsafe_allow_html=True)

        st.markdown("##### 📷 Foto Profil")

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
                    width=180
                )

            else:

                st.info("📷 Belum ada foto profil.")

        else:

            st.info("📷 Belum ada foto profil.")

        uploaded = st.file_uploader(
            "Upload Foto Profil",
            type=["png", "jpg", "jpeg"]
        )

    if uploaded is not None:

        os.makedirs(
            "assets/profile",
            exist_ok=True
        )

        ext = uploaded.name.split(".")[-1]

        nama_file = f"{user['id']}.{ext}"

        save_path = os.path.join(
            "assets",
            "profile",
            nama_file
        )

        with open(save_path, "wb") as f:

            shutil.copyfileobj(
                uploaded,
                f
            )

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE users
            SET foto = ?
            WHERE id = ?
            """,
            (
                nama_file,
                user["id"]
            )
        )

        conn.commit()
        conn.close()

        st.success(
            "✅ Foto profil berhasil diperbarui."
        )

        st.rerun()

    st.write("")

    # ==========================================
    # INFORMASI USER
    # ==========================================

    total = get_total_prediction(user["id"])

    with st.container(border=True):

        st.markdown("<span class='marker-brand'></span>", unsafe_allow_html=True)

        st.markdown("##### ℹ️ Informasi Akun")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"👤 **Nama :** {data['nama']}")
            st.write(f"🆔 **Username :** {data['username']}")

        with col2:
            st.write(f"📅 **Bergabung :** {data['created_at']}")
            st.write(f"📊 **Total Prediksi :** {total}")

    st.write("")

    # ==========================================
    # EDIT NAMA
    # ==========================================

    with st.container(border=True):

        st.markdown("<span class='marker-brand'></span>", unsafe_allow_html=True)

        st.markdown("##### ✏️ Edit Nama")

        nama_baru = st.text_input(
            "Nama Baru",
            value=data["nama"]
        )

        if st.button(
            "💾  Simpan Nama",
            use_container_width=True
        ):

            if nama_baru.strip() == "":

                st.warning(
                    "Nama tidak boleh kosong."
                )

            else:

                update_user_name(
                    user["id"],
                    nama_baru
                )

                # Refresh session user
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

                st.session_state.user = dict(
                    cursor.fetchone()
                )

                conn.close()

                st.success(
                    "✅ Nama berhasil diperbarui."
                )

                st.rerun()

    st.write("")

    st.button(
        "🔑  Ganti Password (Coming Soon)",
        disabled=True,
        use_container_width=True
    )