import streamlit as st

from utils.ui import load_css
from database import get_prediction_history
from utils.sidebar import show_sidebar


def show():

    load_css()

    show_sidebar()

    st.markdown(
        "<span class='badge-pill'>📈 Perjalanan Kesehatan Anda</span>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h1 class='title'>
        Riwayat Prediksi
        </h1>
        """,
        unsafe_allow_html=True
    )

    user = st.session_state.user

    history = get_prediction_history(user["id"])

    if len(history) == 0:

        st.info("Belum ada riwayat prediksi.")

    else:

        st.markdown(
            f"<p class='subtitle'>Total <b>{len(history)}</b> pemeriksaan tercatat</p>",
            unsafe_allow_html=True
        )

        for item in history:

            if item["hasil"] == "Diabetes":
                status = "🔴 Diabetes"
                marker_class = "marker-danger"
                pill_class = "danger"
            else:
                status = "🟢 Non Diabetes"
                marker_class = "marker-success"
                pill_class = "success"

            with st.container(border=True):

                st.markdown(f"<span class='{marker_class}'></span>", unsafe_allow_html=True)

                st.markdown(
                    f"<span class='status-pill {pill_class}'>{status}</span>",
                    unsafe_allow_html=True
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"🗓️ **Tanggal :** {item['created_at']}")
                    st.write(f"⚖️ **BMI :** {item['bmi']}")

                with col2:
                    st.write(
                        f"❤️ **Tekanan Darah :** "
                        f"{item['sistolik']} / {item['diastolik']}"
                    )
                    st.write(
                        f"📊 **Probabilitas Diabetes :** "
                        f"{item['probabilitas']*100:.2f}%"
                    )

            st.write("")

    if st.button(
        "⬅  Dashboard",
        use_container_width=True
    ):

        st.session_state.page = "dashboard"

        st.rerun()