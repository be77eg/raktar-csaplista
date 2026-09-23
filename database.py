import os
import streamlit as st
from supabase import create_client, Client

# Visszaállítottuk a kompatibilitási változókat az app.py importjaihoz
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

def get_default_data():
    return {
        "csapok": [
            {"id": 1, "jelenlegi": "I do what I want", "datum": "2026-05-08", "kovetkezo": ["Fake Your Pils"]},
            {"id": 2, "jelenlegi": "The Age of Heat Dome", "datum": "2026-02-13", "kovetkezo": ["The Age of Heat Dome", "The Age of Heat Dome"]},
            {"id": 3, "jelenlegi": "Let's Jump", "datum": "2026-05-01", "kovetkezo": ["Let's Jump", "Let's Jump"]},
            {"id": 4, "jelenlegi": "Trailer #50 Fifty Shades of Haze", "datum": "2026-01-23", "kovetkezo": ["Trailer #50 Fifty Shades of Haze", "Trailer #50 Fifty Shades of Haze"]},
            {"id": 5, "jelenlegi": "Heart and Sour", "datum": "2026-05-01", "kovetkezo": ["Heart and Sour", "Heart and Sour", "Heart and Sour"]},
            {"id": 6, "jelenlegi": "F**k You Please", "datum": "2026-02-15", "kovetkezo": ["F**k You Please"]},
            {"id": 7, "jelenlegi": "Grain Cosmos", "datum": "2026-01-23", "kovetkezo": ["Grain Cosmos", "Grain Cosmos"]},
            {"id": 8, "jelenlegi": "Trailer #49 Let's Go B(ea)ches", "datum": "2026-02-13", "kovetkezo": []},
            {"id": 9, "jelenlegi": "Rosa", "datum": "2026-01-02", "kovetkezo": ["Rosa"]},
            {"id": 10, "jelenlegi": "Dark Vanilla Sky", "datum": "2026-01-02", "kovetkezo": []},
            {"id": 11, "jelenlegi": "Trailer #48 Universe of Senses", "datum": "2026-05-02", "kovetkezo": []},
            {"id": 12, "jelenlegi": "Stróman", "datum": "2026-02-15", "kovetkezo": []},
        ],
        "kuka": ["I do what I want", "Stróman", "Exhausted Existence", "I do what I want", "Dark Vanilla Sky"],
        "raktar": ["Fake Your Pils", "Grain Cosmos", "Dark Vanilla Sky", "Let's Jump"],
        "szinek": DEFAULT_COLORS,
        "csapmosas": "2026-02-27",
        "co2_csere": "2026-07-26",
        "history": [],
        "kuka_history": [],
    }

def load_data():
    try:
        supabase = init_supabase()
        response = supabase.table("app_data").select("payload").eq("id", 1).execute()
        
        if response.data and len(response.data) > 0:
            payload = response.data[0].get("payload")
            if payload and isinstance(payload, dict) and "csapok" in payload:
                return payload, None
                
        # Ha az adatbázis üres, feltöltjük az alapértelmezett adatokkal
        initial_data = get_default_data()
        success, err = save_data(initial_data)
        if not success:
            st.error(f"⚠️ Nem sikerült elmenteni a kezdő adatokat a Supabase-be: {err}")
        return initial_data, "Az adatbázis üres volt, inicializálva az alapértelmezett adatokkal."
    except Exception as e:
        st.error(f"⚠️ Hiba a Supabase elérésekor: {e}")
        return get_default_data(), f"Hiba történt az adatbázis elérésekor: {e}"

def save_data(data):
    try:
        supabase = init_supabase()
        supabase.table("app_data").upsert({"id": 1, "payload": data}).execute()
        return True, None
    except Exception as e:
        return False, str(e)
