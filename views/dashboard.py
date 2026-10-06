import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from utils.ui import load_css
from utils.sidebar import show_sidebar

from database import (
    get_total_prediction,
    get_last_prediction,
    get_prediction_chart
)


def show():

    load_css()
    show_sidebar()

    user = st.session_state.user

    total_prediksi = get_total_prediction(user["id"])
    last_prediction = get_last_prediction(user["id"])
    chart_data = get_prediction_chart(user["id"])

    if last_prediction:
        bmi = round(last_prediction["bmi"], 2)
        hasil = last_prediction["hasil"]
    else:
        bmi = "-"
        hasil = "-"

    st.markdown(
        "<span class='badge-pill'>📊 Ringkasan Kesehatan</span>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h1 class='title'>
        🏠 Dashboard
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <p class='subtitle'>
        Selamat Datang, <b>{user["nama"]}</b> 👋
        </p>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # ==========================================
    # METRIC
    # ==========================================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🧮 Total Prediksi",
            total_prediksi
        )

    with col2:
        st.metric(
            "⚖️ BMI Terakhir",
            bmi
        )

    with col3:
        st.metric(
            "🩺 Hasil Terakhir",
            hasil
        )

    st.divider()

    # ==========================================
    # GRAFIK RISIKO
    # ==========================================

    st.subheader("📈 Tren Risiko Diabetes")

    if len(chart_data) > 0:

        df = pd.DataFrame([dict(row) for row in chart_data])

        df["Tanggal"] = pd.to_datetime(df["created_at"])
        df["Risiko"] = (df["probabilitas"] * 100).round(2)
        df["Tanggal Label"] = df["Tanggal"].dt.strftime("%d-%m-%Y %H:%M")

        fig = go.Figure()

        # =========================
        # Garis Tren (Sederhana)
        # =========================

        fig.add_trace(
            go.Scatter(
                x=df["Tanggal"],
                y=df["Risiko"],
                mode="lines+markers",
                line=dict(
                    color="#2563EB",
                    width=4
                ),
                marker=dict(
                    size=10,
                    color="#2563EB"
                ),
                customdata=df[["Tanggal Label", "hasil"]],
                hovertemplate=
                "<b>%{customdata[0]}</b><br>" +
                "Risiko Diabetes : <b>%{y:.2f}%</b><br>" +
                "Hasil Prediksi : %{customdata[1]}" +
                "<extra></extra>",
                showlegend=False
            )
        )

        # =========================
        # Garis Ambang
        # =========================

        fig.add_hline(
            y=50,
            line_dash="dash",
            line_color="orange",
            annotation_text="Ambang Risiko 50%",
            annotation_position="top left"
        )

        fig.update_layout(
            template="plotly_white",
            height=500,
            showlegend=False,
            hovermode="closest",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color="#161b2c"),
            xaxis_title="Tanggal Pemeriksaan",
            yaxis_title="Risiko Diabetes (%)",
            yaxis=dict(
                range=[0, 100]
            )
        )

        with st.container(border=True):
            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ==========================================
        # RINGKASAN
        # ==========================================

        st.subheader("🗓️ Ringkasan Pemeriksaan")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "📅 Pemeriksaan Pertama",
                df.iloc[0]["Tanggal Label"]
            )

        with col2:
            st.metric(
                "🕓 Pemeriksaan Terakhir",
                df.iloc[-1]["Tanggal Label"]
            )

        st.divider()

        # ==========================================
        # PERUBAHAN RISIKO
        # ==========================================

        if len(df) >= 2:

            terakhir = df.iloc[-1]["Risiko"]
            sebelumnya = df.iloc[-2]["Risiko"]

            selisih = round(
                terakhir - sebelumnya,
                2
            )

            if selisih > 0:
                st.error(
                    f" Risiko meningkat **{selisih}%** dibanding pemeriksaan sebelumnya."
                )
            elif selisih < 0:
                st.success(
                    f" Risiko menurun **{abs(selisih)}%** dibanding pemeriksaan sebelumnya."
                )
            else:
                st.info(
                    " Risiko tetap dibanding pemeriksaan sebelumnya."
                )

            st.divider()

        # ==========================================
        # INTERPRETASI
        # ==========================================

        st.subheader("💡 Interpretasi Risiko")

        risiko = df.iloc[-1]["Risiko"]

        if risiko < 30:
            st.success(
                "Risiko diabetes saat ini tergolong **rendah**. Pertahankan pola hidup sehat, "
                "olahraga rutin, dan konsumsi makanan bergizi seimbang."
            )
        elif risiko < 60:
            st.warning(
                "Risiko diabetes saat ini tergolong **sedang**. Disarankan menjaga pola makan, "
                "meningkatkan aktivitas fisik, dan melakukan pemeriksaan kesehatan secara berkala."
            )
        else:
            st.error(
                "Risiko diabetes saat ini tergolong **tinggi**. Disarankan berkonsultasi dengan "
                "tenaga kesehatan untuk pemeriksaan lebih lanjut."
            )

        st.divider()

        st.info(
            """
            💡 Grafik di atas menunjukkan perkembangan risiko diabetes berdasarkan setiap
            hasil prediksi yang telah dilakukan. Semakin rutin melakukan pemeriksaan,
            semakin mudah memantau perubahan risiko dari waktu ke waktu.
            """
        )

    else:
        st.info(
            "Belum ada data prediksi untuk ditampilkan."
        )