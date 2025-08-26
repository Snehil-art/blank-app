import streamlit as st
import requests
import sqlite3

# -------------------------
# CONFIG (your Airtable app credentials)
# -------------------------
CLIENT_ID = "55ac7ace-54db-47bf-bee5-4e478d47f1dd"
CLIENT_SECRET = "3ae16fa14d39b96e1f3551ec8fc497303ba3cd3f1a616da43f6ac49a1b9ebfe4"
REDIRECT_URI = "http://localhost:8501"  # change when you deploy
TOKEN_URL = "https://airtable.com/oauth2/v1/token"
SCOPES = "data.records:read data.records:write"

# -------------------------
# DB Setup
# -------------------------
def init_db():
    conn = sqlite3.connect("tokens.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_tokens (
            email TEXT PRIMARY KEY,
            access_token TEXT,
            refresh_token TEXT,
            base_id TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save_token(user_email, token_data):
    conn = sqlite3.connect("tokens.db")
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO user_tokens VALUES (?, ?, ?, ?)",
        (
            user_email,
            token_data["access_token"],
            token_data.get("refresh_token"),
            None
        )
    )
    conn.commit()
    conn.close()

# -------------------------
# UI
# -------------------------
st.set_page_config(page_title="Airtable OAuth Demo", page_icon="🔑")
st.title("🔑 Airtable OAuth Demo")

st.markdown("Click below to connect your Airtable account:")

auth_url = (
    f"https://airtable.com/oauth2/v1/authorize?"
    f"client_id={CLIENT_ID}&"
    f"redirect_uri={REDIRECT_URI}&"
    f"response_type=code&"
    f"scope={SCOPES}"
)

st.markdown(f"[🔗 Connect Airtable]({auth_url})")

# -------------------------
# Handle Callback
# -------------------------
params = st.query_params  # Streamlit's way to read URL query parameters
if "code" in params:
    code = params["code"]
    st.info(f"Got OAuth code: {code[:6]}...")

    # Exchange code for token
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }
    resp = requests.
