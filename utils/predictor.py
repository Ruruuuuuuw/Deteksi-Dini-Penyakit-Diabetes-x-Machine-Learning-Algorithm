import joblib
import pandas as pd

# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load("model/model_random_forest.pkl")

print("=" * 50)
print("MODEL BERHASIL DIMUAT")
print("CLASS MODEL :", model.classes_)
print("=" * 50)


# ==========================================
# PREDIKSI DIABETES
# ==========================================

def predict_diabetes(umur, jenis_kelamin, bmi, sistolik, diastolik):
    """
    Mapping Label Model

    0 = Non Diabetes
    1 = Diabetes
    """

    # ==========================================
    # DATA INPUT
    # HARUS SAMA DENGAN SAAT TRAINING
    # ==========================================

    data = pd.DataFrame([{

        "Umur": umur,

        "Jenis Kelamin": jenis_kelamin,

        "BMI": bmi,

        "Sistolik": sistolik,

        "Diastolik": diastolik

    }])

    # ==========================================
    # PREDIKSI
    # ==========================================

    hasil = int(model.predict(data)[0])

    probabilitas = model.predict_proba(data)[0]

    # ==========================================
    # DEBUG
    # ==========================================

    print("\n" + "=" * 50)
    print("INPUT")
    print(f"Umur            : {umur}")
    print(f"Jenis Kelamin   : {jenis_kelamin}")
    print(f"BMI             : {bmi}")
    print(f"Sistolik        : {sistolik}")
    print(f"Diastolik       : {diastolik}")
    print("-" * 50)
    print("HASIL PREDIKSI :", hasil)
    print("PROBABILITAS   :", probabilitas)
    print("CLASS MODEL    :", model.classes_)
    print("=" * 50 + "\n")

    return hasil, probabilitas