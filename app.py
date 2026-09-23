import os
import json
import datetime
import streamlit as st

# --- KONFIGURÁCIÓ ÉS FÁJLÚTVONALAK ---
DATA_DIR = "data"
BACKUP_DIR = os.path.join(DATA_DIR, "backups")
DATA_FILE = os.path.join(DATA_DIR, "csaplista_data.json")

# Alapértelmezett színpaletta (csak teljesen új, üres induláskor használatos)
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

def ensure_directories():
    """Létrehozza a szükséges mappákat, ha még nem léteznek."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)

def get_empty_database_structure():
    """Teljesen üres, tiszta szerkezet az első induláshoz."""
    return {
        "csapok": [{"id": i, "jelenlegi": "", "datum": "", "kovetkezo": []} for i in range(1, 13)],
        "kuka": [],
        "raktar": [],
        "szinek": DEFAULT_COLORS,
        "csapmosas": "",
        "co2_csere": "",
        "history": [],
        "kuka_history": [],
    }

def load_data():
    """
    Mindig a legutolsó érvényes fizikai állapotot tölti vissza.
    Ha a fő fájl sérült vagy hiányzik, a backup mappából keresi a legfrissebbet.
    """
    ensure_directories()
    
    # 1. Próbáljuk meg a fő adatfájlt betölteni
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    if isinstance(data, dict) and "csapok" in data:
                        return data
        except Exception as e:
            st.warning(f"A fő adatfájl olvasási hiba miatt sérültnek tűnik: {e}")

    # 2. Ha a fő fájl nem létezik vagy hibás, nézzük meg a mentéseket (Backup)
    if os.path.exists(BACKUP_DIR):
        backup_files = [os.path.join(BACKUP_DIR, f) for f in os.listdir(BACKUP_DIR) if f.endswith(".json")]
        if backup_files:
            # Rendezzük a fájlokat módosítási idő szerint csökkenőbe (a legfrissebb előre)
            latest_backup = max(backup_files, key=os.path.getmtime)
            try:
                with open(latest_backup, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    st.success(f"Sikerült visszaállítani az adatokat a legfrissebb biztonsági mentésből: {os.path.basename(latest_backup)}")
                    return data
            except Exception:
                pass

    # 3. Ha semmi sincs, akkor inicializáljuk az üres struktúrát
    initial_data = get_empty_database_structure()
    save_data(initial_data)
    return initial_data

def save_data(data):
    """
    Elmenti az adatokat a fő fájlba, és készít egy időbélyeges mentést is a backups mappába.
    Így semmilyen frissítés vagy hiba nem törölheti el véglegesen az adatokat.
    """
    ensure_directories()
    
    # Adatok mentése a fő fájlba
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Hiba történt az adatok mentése közben: {e}")
        return

    # Időbélyeges biztonsági mentés készítése minden mentés alkalmával
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file_path = os.path.join(BACKUP_DIR, f"csaplista_backup_{timestamp}.json")
    try:
        with open(backup_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        # Takarítsuk ki a túl régi mentéseket (csak az utolsó 20-at őrizzük meg)
        all_backups = sorted([os.path.join(BACKUP_DIR, f) for f in os.listdir(BACKUP_DIR) if f.endswith(".json")], key=os.path.getmtime)
        if len(all_backups) > 20:
            for old_file in all_backups[:-20]:
                os.remove(old_file)
    except Exception:
        pass

# --- ALKALMAZÁS INICIALIZÁLÁSA ---
if "data" not in st.session_state:
    st.session_state.data = load_data()
