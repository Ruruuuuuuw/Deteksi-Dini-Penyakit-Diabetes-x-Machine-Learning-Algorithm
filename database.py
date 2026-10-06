import sqlite3

DB_PATH = "database/diabetes.db"


# ==========================================
# KONEKSI DATABASE
# ==========================================

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# MEMBUAT TABEL
# ==========================================

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # ======================
    # USERS
    # ======================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nama TEXT NOT NULL,

        username TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ======================
    # HISTORY
    # ======================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prediction_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        umur INTEGER,

        jenis_kelamin INTEGER,

        tinggi REAL,

        berat REAL,

        bmi REAL,

        sistolik INTEGER,

        diastolik INTEGER,

        hasil TEXT,

        probabilitas REAL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)

    )
    """)

    conn.commit()
    conn.close()


# ==========================================
# TAMBAH KOLOM FOTO
# ==========================================

def add_foto_column():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(users)")

    columns = [column[1] for column in cursor.fetchall()]

    if "foto" not in columns:

        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN foto TEXT DEFAULT 'default.png'
        """)

        conn.commit()

    conn.close()


# ==========================================
# SIMPAN HASIL PREDIKSI
# ==========================================

from datetime import datetime
from zoneinfo import ZoneInfo


def save_prediction(

    user_id,
    umur,
    jenis_kelamin,
    tinggi,
    berat,
    bmi,
    sistolik,
    diastolik,
    hasil,
    probabilitas

):

    conn = get_connection()
    cursor = conn.cursor()

    # Waktu Indonesia (WIB)
    created_at = datetime.now(
        ZoneInfo("Asia/Jakarta")
    ).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""

    INSERT INTO prediction_history(

        user_id,
        umur,
        jenis_kelamin,
        tinggi,
        berat,
        bmi,
        sistolik,
        diastolik,
        hasil,
        probabilitas,
        created_at

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        user_id,
        umur,
        jenis_kelamin,
        tinggi,
        berat,
        bmi,
        sistolik,
        diastolik,
        hasil,
        float(probabilitas),
        created_at

    ))

    conn.commit()
    conn.close()


# ==========================================
# RIWAYAT PREDIKSI USER
# ==========================================

def get_prediction_history(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM prediction_history

        WHERE user_id = ?

        ORDER BY created_at DESC

    """, (user_id,))

    history = cursor.fetchall()

    conn.close()

    return history


# ==========================================
# TOTAL PREDIKSI
# ==========================================

def get_total_prediction(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM prediction_history

        WHERE user_id = ?

    """, (user_id,))

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ==========================================
# DATA TERAKHIR
# ==========================================

def get_last_prediction(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM prediction_history

        WHERE user_id = ?

        ORDER BY created_at DESC

        LIMIT 1

    """, (user_id,))

    last = cursor.fetchone()

    conn.close()

    return last

    # ==========================================
# UPDATE NAMA USER
# ==========================================

def update_user_name(user_id, nama):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET nama = ?
        WHERE id = ?
        """,
        (
            nama,
            user_id
        )
    )

    conn.commit()
    conn.close()

# ==========================================
# STATISTIK PREDIKSI
# ==========================================

def get_prediction_summary(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT hasil,
               COUNT(*) as total
        FROM prediction_history
        WHERE user_id = ?
        GROUP BY hasil
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    summary = {
        "Diabetes": 0,
        "Non Diabetes": 0
    }

    for row in rows:

        summary[row["hasil"]] = row["total"]

    return summary

# ==========================================
# DATA GRAFIK RISIKO DIABETES
# ==========================================

def get_prediction_chart(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            created_at,
            probabilitas,
            hasil
        FROM prediction_history
        WHERE user_id = ?
        ORDER BY created_at ASC
        """,
        (user_id,)
    )

    data = cursor.fetchall()

    conn.close()

    return data