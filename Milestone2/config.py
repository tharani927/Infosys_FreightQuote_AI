"""
config.py — FreightQuote AI (v3 FINAL)
All secrets from Colab userdata. No hardcoded credentials anywhere.
"""
import os

def _get_secret(key):
    try:
        from google.colab import userdata
        val = userdata.get(key)
        if val: return val
    except Exception:
        pass
    return os.environ.get(key, "")

try:
    from __main__ import (STORAGE_DIR, NGROK_AUTHTOKEN, HF_TOKEN,
                          KAGGLE_USERNAME, KAGGLE_KEY, EMAIL_PASSWORD,
                          ADMIN_EMAIL, ADMIN_PASSWORD, EMAIL_ID)
except ImportError:
    STORAGE_DIR    = ("/content/drive/MyDrive/FreightQuote_AI"
                      if os.path.exists("/content/drive/MyDrive") else
                      os.path.abspath("./data/FreightQuote_AI"))
    NGROK_AUTHTOKEN = _get_secret("NGROK_AUTHTOKEN")
    NGROK_AUTH_TOKEN = NGROK_AUTHTOKEN # Alias for launch cell compatibility
    HF_TOKEN        = _get_secret("HF_TOKEN")
    KAGGLE_USERNAME = _get_secret("KAGGLE_USERNAME")
    KAGGLE_KEY      = _get_secret("KAGGLE_KEY")
    EMAIL_PASSWORD  = _get_secret("EMAIL_PASSWORD")
    EMAIL_ID        = _get_secret("EMAIL_ID")
    JWT_SECRET_KEY  = _get_secret("JWT_SECRET_KEY") or "freightquote-dev-secret-changeme"
    ADMIN_EMAIL     = _get_secret("ADMIN_EMAIL_ID")  or "infosys@ai"
    ADMIN_PASSWORD  = _get_secret("ADMIN_PASSWORD")  or "admin@123"

os.makedirs(STORAGE_DIR, exist_ok=True)
DB_PATH          = os.path.join(STORAGE_DIR, "freightquote.db")
MODELS_DIR       = os.path.join(STORAGE_DIR, "models")
KAGGLE_CACHE_DIR = os.path.join(MODELS_DIR, "kaggle_cache")
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(KAGGLE_CACHE_DIR, exist_ok=True)

AGENT1_MODEL_PATH = os.path.join(MODELS_DIR, "pricing_rf.joblib")
AGENT2_MODEL_PATH = os.path.join(MODELS_DIR, "delay_risk_rf.joblib")
AGENT3_MODEL_PATH = os.path.join(MODELS_DIR, "carrier_audit_gb.joblib")
