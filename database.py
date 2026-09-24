import os
import streamlit as st
from supabase import create_client, Client

# Kompatibilitási változók az app.py importjaihoz
DATA_FILE = "data/csaplista.json"
BACKUP_DIR = "data/backups"

# --- SUPABASE KAPCSOLAT BEÁLLÍTÁSA ---
SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL", ""))
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY", ""))

def init_supabase() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.error("⚠️ Nincsenek beállítva a Supabase hozzáférési adatok a Secrets-ben!")
        st.stop()
    return create_client(SUPABASE_URL, SUPABASE_KEY)

DEFAULT_COLORS = {
    "I do what I want": "#FF5733",
    "The Age of Heat Dome": "#33FF57",
    "Let's Jump": "#3357FF",
    "Trailer #50 Fifty Shades of Haze": "#F39C12",
    "Heart and Sour": "#E74C3C",
    "F**k You Please": "#9B59B6",
    "Grain Cosmos": "#1ABC9C",
    "Trailer #49 Let's Go B(ea)ches": "#D35400",
    "Rosa": "#FF69B4",
    "Dark Vanilla Sky": "#34495E",
    "Trailer #48 Universe of Senses": "#16A085",
    "Stróman": "#27AE60",
    "Fake Your Pils": "#F1C40F",
}

def get_empty_data():
    """Tiszta 0-pont kezdőállapot mintaadatok nélkül."""
    return {
        "csapok": [
            {"id": i, "jelenlegi": "Üres csap", "datum": "", "kovetkezo": []}
            for i in range(1, 13)
        ],
        "kuka": [],
        "raktar": [],
        "szinek": DEFAULT_COLORS,
        "csapmosas": "",
        "co2_csere": "",
        "history": [],
        "kuka_history": [],
    }

def load_data():
    try:
        supabase = init_supabase()
        response = supabase.table("app_data").select("payload").eq("id", 1).execute()
        
        if response.data and len(response.data) > 0:
            payload = response.data[0].get("payload")
            # Ha van érvényes csaplista adat, azt adjuk vissza
            if payload and isinstance(payload, dict) and "csapok" in payload and len(payload["csapok"]) > 0:
                return payload, None
                
        # Ha az adatbázis üres vagy törölve volt, elmentjük a tiszta 0-pontot
        empty_data = get_empty_data()
        save_data(empty_data)
        return empty_data, "Új, tiszta adatbázis inicializálva (0-pont)."
    except Exception as e:
        st.error(f"⚠️ Hiba a Supabase elérésekor: {e}")
        return get_empty_data(), f"Hiba történt az adatbázis elérésekor: {e}"

def save_data(data):
    try:
        supabase = init_supabase()
        supabase.table("app_data").upsert({"id": 1, "payload": data}).execute()
        return True, None
    except Exception as e:
        st.error(f"⚠️ Mentési hiba: {e}")
        return False, str(e)
