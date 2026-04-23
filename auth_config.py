import streamlit_authenticator as stauth

# ---------- USERS ----------
names = ["Khanak", "Yash", "Admin"]
usernames = ["Khanak", "Yash", "Admin"]
passwords = ["2201", "3012", "1234"]

# ---------- PROPER HASHING (UPDATED FOR VERSION 0.4.2) ----------
hashed_passwords = stauth.Hasher().hash_passwords(passwords)

# ---------- CREDENTIALS ----------
credentials = {
    "usernames": {
        "Khanak": {
            "name": "Khanak",
            "password": hashed_passwords[0]
        },
        "Yash": {
            "name": "Yash",
            "password": hashed_passwords[1]
        },
        "Admin": {
            "name": "Admin",
            "password": hashed_passwords[2]
        }
    }
}

# ---------- AUTH OBJECT ----------
authenticator = stauth.Authenticate(
    credentials,
    "nutrition_app",
    "secure_cookie_key",
    cookie_expiry_days=1
)
