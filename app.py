import streamlit as st
from database import load_data, save_data, DATA_FILE, BACKUP_DIR

# --- ALKALMAZÁS INICIALIZÁLÁSA ---
st.set_page_config(page_title="Raktár & Csaplista", layout="wide")

if "data" not in st.session_state:
    data, msg = load_data()
    st.session_state.data = data
    if msg:
        if "Visszaállítva" in msg:
            st.success(msg)
        else:
            st.info(msg)

# --- FELHASZNÁLÓI FELÜLET (UI) ---
st.title("🍺 Raktár és Csaplista Kezelő")

# Navigációs sáv
menu = st.sidebar.selectbox("Menü", ["Csapok", "Raktár", "Kuka", "Beállítások / Adatok"])

data = st.session_state.data

if menu == "Csapok":
    st.header("Aktuális Csapok Állapota")
    
    for csap in data["csapok"]:
        col1, col2, col3 = st.columns([1, 3, 3])
        with col1:
            st.write(f"### #{csap['id']}")
        with col2:
            uj_jelenlegi = st.text_input(f"Jelenlegi sör (Csap #{csap['id']})", value=csap["jelenlegi"], key=f"jelenlegi_{csap['id']}")
            if uj_jelenlegi != csap["jelenlegi"]:
                csap["jelenlegi"] = uj_jelenlegi
                success, err = save_data(data)
                if not success:
                    st.error(f"Mentési hiba: {err}")
        with col3:
            uj_datum = st.text_input(f"Dátum (Csap #{csap['id']})", value=csap["datum"], key=f"datum_{csap['id']}")
            if uj_datum != csap["datum"]:
                csap["datum"] = uj_datum
                success, err = save_data(data)
                if not success:
                    st.error(f"Mentési hiba: {err}")
        st.divider()

elif menu == "Raktár":
    st.header("Raktár készlet")
    raktar_szoveg = st.text_area("Raktáron lévő tételek (soronként egy)", value="\n".join(data["raktar"]))
    if st.button("Raktár mentése"):
        data["raktar"] = [sor.strip() for sor in raktar_szoveg.split("\n") if sor.strip()]
        success, err = save_data(data)
        if success:
            st.success("Raktár sikeresen mentve!")
        else:
            st.error(f"Hiba: {err}")

elif menu == "Kuka":
    st.header("Kuka / Kidobott tételek")
    kuka_szoveg = st.text_area("Kukában lévő tételek (soronként egy)", value="\n".join(data["kuka"]))
    if st.button("Kuka mentése"):
        data["kuka"] = [sor.strip() for sor in kuka_szoveg.split("\n") if sor.strip()]
        success, err = save_data(data)
        if success:
            st.success("Kuka sikeresen mentve!")
        else:
            st.error(f"Hiba: {err}")

elif menu == "Beállítások / Adatok":
    st.header("Rendszer / Biztonsági mentések")
    st.write(f"Aktuális adatfájl helye: `{DATA_FILE}`")
    st.write(f"Biztonsági mentések mappája: `{BACKUP_DIR}`")
    
    if st.button("Adatok újratöltése a fizikai fájlból"):
        data, msg = load_data()
        st.session_state.data = data
        st.success("Adatok frissítve a fizikai tárolóból!")
        st.rerun()
