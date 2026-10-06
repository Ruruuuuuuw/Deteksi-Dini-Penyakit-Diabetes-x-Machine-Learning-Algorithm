import bcrypt
from database import get_connection


# ===========================
# HASH PASSWORD
# ===========================

def hash_password(password):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )


# ===========================
# REGISTER USER
# ===========================

def register_user(nama, username, password):

    conn = get_connection()
    cursor = conn.cursor()

    hashed = hash_password(password)

    try:

        cursor.execute("""

        INSERT INTO users
        (nama, username, password)

        VALUES (?, ?, ?)

        """,

        (
            nama,
            username,
            hashed
        ))

        conn.commit()

        return True

    except:

        return False

    finally:

        conn.close()


# ===========================
# LOGIN
# ===========================

def login_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT *
    FROM users
    WHERE username=?

    """,(username,))

    user = cursor.fetchone()

    conn.close()

    if user:

        if bcrypt.checkpw(
            password.encode(),
            user["password"]
        ):

            return user

    return None