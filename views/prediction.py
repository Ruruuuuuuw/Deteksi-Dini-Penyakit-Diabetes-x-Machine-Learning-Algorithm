import streamlit as st

from utils.ui import load_css
from utils.predictor import predict_diabetes
from database import save_prediction
from utils.sidebar import show_sidebar


# ==========================================
# HITUNG BMI
# ==========================================

def hitung_bmi(berat, tinggi):

    if tinggi == 0:
        return 0

    return round(
        berat / ((tinggi / 100) ** 2),
        2
    )


# ==========================================
# KATEGORI BMI
# ==========================================

def kategori_bmi(bmi):

    if bmi < 18.5:
        return "Berat Badan Kurang"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obesitas"


# ==========================================
# KATEGORI TEKANAN DARAH
# ==========================================

def kategori_tekanan_darah(sistolik, diastolik):

    if sistolik < 120 and diastolik < 80:
        return "Normal"

    elif 120 <= sistolik < 130 and diastolik < 80:
        return "Elevated"

    elif sistolik >= 140 or diastolik >= 90:
        return "Hipertensi Stage 2"

    elif sistolik >= 130 or diastolik >= 80:
        return "Hipertensi Stage 1"

    else:
        return "Normal"


# ==========================================
# REKOMENDASI
# ==========================================

def rekomendasi(hasil):

    if hasil == "Diabetes":

        return [

            "Kurangi konsumsi makanan dan minuman tinggi gula.",

            "Lakukan aktivitas fisik minimal 150 menit per minggu.",

            "Pertahankan berat badan ideal.",

            "Periksa kadar gula darah secara berkala.",

            "Konsultasikan dengan dokter untuk pemeriksaan lanjutan."

        ]

    return [

        "Pertahankan pola makan sehat dan seimbang.",

        "Tetap rutin berolahraga.",

        "Jaga berat badan tetap ideal.",

        "Lakukan pemeriksaan kesehatan secara berkala."

    ]


# ==========================================
# HALAMAN
# ==========================================

def show():

    load_css()

    show_sidebar()

    st.markdown(
        "<span class='badge-pill'>🩺 Cek Kesehatan Anda</span>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h1 class='title'>
        Prediksi Risiko Diabetes
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p class='subtitle'>
        Masukkan data kesehatan Anda untuk mendapatkan estimasi risiko diabetes
        </p>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    with st.container(border=True):

        st.markdown("##### 🧍 Data Diri")

        col_a, col_b = st.columns(2)

        with col_a:
            umur = st.number_input(
                "Umur",
                min_value=1,
                max_value=120,
                value=25
            )

        with col_b:
            jenis_kelamin = st.radio(
                "Jenis Kelamin",
                [
                    "Laki-laki",
                    "Perempuan"
                ]
            )

        st.markdown("##### ⚖️ Berat & Tinggi Badan")

        col_c, col_d = st.columns(2)

        with col_c:
            tinggi = st.number_input(
                "Tinggi Badan (cm)",
                min_value=50.0,
                max_value=250.0,
                value=170.0
            )

        with col_d:
            berat = st.number_input(
                "Berat Badan (kg)",
                min_value=10.0,
                max_value=250.0,
                value=70.0
            )

        bmi = hitung_bmi(
            berat,
            tinggi
        )

        st.info(f"📐 BMI Anda saat ini : **{bmi}**")

        st.markdown("##### ❤️ Tekanan Darah")

        col_e, col_f = st.columns(2)

        with col_e:
            sistolik = st.number_input(
                "Tekanan Darah Sistolik",
                min_value=50,
                max_value=250,
                value=120
            )

        with col_f:
            diastolik = st.number_input(
                "Tekanan Darah Diastolik",
                min_value=30,
                max_value=200,
                value=80
            )

        st.write("")

        col1, col2 = st.columns(2)

        with col1:

            prediksi = st.button(
                "🔍  Prediksi",
                key="prediction_button",
                use_container_width=True
            )

        with col2:

            dashboard = st.button(
                "🏠  Dashboard",
                key="prediction_dashboard",
                use_container_width=True
            )

    if dashboard:

        st.session_state.page = "dashboard"
        st.rerun()

    # ==========================================
    # PREDIKSI
    # ==========================================

    if prediksi:

        jk = 1 if jenis_kelamin == "Laki-laki" else 0

        hasil, probabilitas = predict_diabetes(

            umur,
            jk,
            bmi,
            sistolik,
            diastolik

        )

        peluang = float(probabilitas[1])
        risiko = probabilitas[1] * 100

        if risiko < 30:
            marker_class, pill_class, risk_emoji, risk_text = "marker-success", "success", "🟢", "Risiko Rendah"
        elif risiko < 60:
            marker_class, pill_class, risk_emoji, risk_text = "marker-warning", "warning", "🟡", "Risiko Sedang"
        else:
            marker_class, pill_class, risk_emoji, risk_text = "marker-danger", "danger", "🔴", "Risiko Tinggi"

        st.write("")
        st.markdown("---")

        with st.container(border=True):

            st.markdown(f"<span class='{marker_class}'></span>", unsafe_allow_html=True)

            if hasil == 1:
                hasil_label = "Diabetes"
                st.markdown("<span class='status-pill danger'>🔴 Hasil Prediksi : Diabetes</span>", unsafe_allow_html=True)
            else:
                hasil_label = "Non Diabetes"
                st.markdown("<span class='status-pill success'>🟢 Hasil Prediksi : Non Diabetes</span>", unsafe_allow_html=True)

            st.subheader("📊 Analisis Risiko Diabetes")

            st.metric(
                "Risiko Diabetes",
                f"{risiko:.2f}%"
            )

            st.progress(float(probabilitas[1]))

            st.markdown(
                f"<span class='status-pill {pill_class}'>{risk_emoji} {risk_text}</span>",
                unsafe_allow_html=True
            )

            st.divider()

            st.subheader("🧮 Probabilitas Model")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Diabetes",
                    f"{probabilitas[1]*100:.2f}%"
                )

            with col2:

                st.metric(
                    "Non Diabetes",
                    f"{probabilitas[0]*100:.2f}%"
                )

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "⚖️ BMI",
                    bmi
                )

                st.caption(
                    kategori_bmi(bmi)
                )

            with col2:

                st.metric(
                    "❤️ Tekanan Darah",
                    f"{sistolik}/{diastolik}"
                )

                st.caption(
                    kategori_tekanan_darah(
                        sistolik,
                        diastolik
                    )
                )

        st.write("")

        with st.container(border=True):

            st.markdown("<span class='marker-brand'></span>", unsafe_allow_html=True)

            st.subheader("💡 Rekomendasi")

            for saran in rekomendasi(hasil_label):

                st.write(f"• {saran}")

            st.warning(
                "⚠️ Hasil ini merupakan prediksi menggunakan model Machine Learning dan tidak menggantikan diagnosis dari tenaga medis."
            )

        # ==========================================
        # SIMPAN DATABASE
        # ==========================================

        save_prediction(

            user_id=st.session_state.user["id"],

            umur=umur,

            jenis_kelamin=jk,

            tinggi=tinggi,

            berat=berat,

            bmi=bmi,

            sistolik=sistolik,

            diastolik=diastolik,

            hasil=hasil_label,

            probabilitas=float(peluang)

        )

        st.success(
            "✅ Hasil prediksi berhasil disimpan."
        )