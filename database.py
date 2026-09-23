import os
import json
import datetime

DATA_DIR = "data"
BACKUP_DIR = os.path.join(DATA_DIR, "backups")
DATA_FILE = os.path.join(DATA_DIR, "csaplista_data.json")

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
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)

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
    ensure_directories()
    
    # 1. Próbáljuk betölteni a fő adatfájlból
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    if isinstance(data, dict) and "csapok" in data:
                        return data, None
        except Exception:
            pass

    # 2. Ha hiba van vagy nincs fő fájl, keressük a legfrissebb backupot
    if os.path.exists(BACKUP_DIR):
        backup_files = [os.path.join(BACKUP_DIR, f) for f in os.listdir(BACKUP_DIR) if f.endswith(".json")]
        if backup_files:
            latest_backup = max(backup_files, key=os.path.getmtime)
            try:
                with open(latest_backup, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    msg = f"Sikerült visszaállítani az adatokat innen: {os.path.basename(latest_backup)}"
                    return data, msg
            except Exception:
                pass

    # 3. Ha semmi nincs, inicializáljuk az alapértelmezett adatokkal
    initial_data = get_default_data()
    save_data(initial_data)
    return initial_data, "Új adatbázis lett inicializálva az alapértelmezett adatokkal."

def save_data(data):
    ensure_directories()
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        return False, str(e)

    # Biztonsági mentés időbélyeggel
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file_path = os.path.join(BACKUP_DIR, f"csaplista_backup_{timestamp}.json")
    try:
        with open(backup_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        # Csak az utolsó 20 mentés megőrzése
        all_backups = sorted([os.path.join(BACKUP_DIR, f) for f in os.listdir(BACKUP_DIR) if f.endswith(".json")], key=os.path.getmtime)
        if len(all_backups) > 20:
            for old_file in all_backups[:-20]:
                os.remove(old_file)
    except Exception:
        pass

    return True, None
