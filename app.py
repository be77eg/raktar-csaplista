import datetime
import json
import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Csaplista & Hordókövető", page_icon="🍺", layout="wide"
)

DATA_FILE = "csaplista_data.json"


# Adatok betöltése vagy alapértelmezett állapot létrehozása
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Kezdő adatok a meglévő CSV struktúrája alapján
        return {
            "csapok": [
                {
                    "id": 1,
                    "jelenlegi": "I do what I want",
                    "datum": "2026-05-08",
                    "kovetkezo": ["Fake Your Pils"],
                },
                {
                    "id": 2,
                    "jelenlegi": "The Age of Heat Dome",
                    "datum": "2026-02-13",
                    "kovetkezo": [
                        "The Age of Heat Dome",
                        "The Age of Heat Dome",
                    ],
                },
                {
                    "id": 3,
                    "jelenlegi": "Let's Jump",
                    "datum": "2026-05-01",
                    "kovetkezo": ["Let's Jump", "Let's Jump"],
                },
                {
                    "id": 4,
                    "jelenlegi": "Trailer #50 Fifty Shades of Haze",
                    "datum": "2026-01-23",
                    "kovetkezo": [
                        "Trailer #50 Fifty Shades of Haze",
                        "Trailer #50 Fifty Shades of Haze",
                    ],
                },
                {
                    "id": 5,
                    "jelenlegi": "Heart and Sour",
                    "datum": "2026-05-01",
                    "kovetkezo": [
                        "Heart and Sour",
                        "Heart and Sour",
                        "Heart and Sour",
                    ],
                },
                {
                    "id": 6,
                    "jelenlegi": "F**k You Please",
                    "datum": "2026-02-15",
                    "kovetkezo": ["F**k You Please"],
                },
                {
                    "id": 7,
                    "jelenlegi": "Grain Cosmos",
                    "datum": "2026-01-23",
                    "kovetkezo": ["Grain Cosmos", "Grain Cosmos"],
                },
                {
                    "id": 8,
                    "jelenlegi": "Trailer #49 Let's Go B(ea)ches",
                    "datum": "2026-02-13",
                    "kovetkezo": [],
                },
                {
                    "id": 9,
                    "jelenlegi": "Rosa",
                    "datum": "2026-01-02",
                    "kovetkezo": ["Rosa"],
                },
                {
                    "id": 10,
                    "jelenlegi": "Dark Vanilla Sky",
                    "datum": "2026-01-02",
                    "kovetkezo": [],
                },
                {
                    "id": 11,
                    "jelenlegi": "Trailer #48 Universe of Senses",
                    "datum": "2026-05-02",
                    "kovetkezo": [],
                },
                {
                    "id": 12,
                    "jelenlegi": "Stróman",
                    "datum": "2026-02-15",
                    "kovetkezo": [],
                },
            ],
            "kuka": [
                "I do what I want",
                "Stróman",
                "Exhausted Existence",
                "I do what I want",
                "Dark Vanilla Sky",
            ],
            "csapmosas": "2026-02-27",
            "co2_csere": "2026-07-26",
        }


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


data = load_data()

# Fejléc és Karbantartás
st.title("🍺 Csaplista & Hordókövető")

col_k1, col_k2 = st.columns(2)
with col_k1:
    st.info(f"🧼 **Utolsó csapmosás:** {data['csapmosas']}")
with col_k2:
    st.warning(f"💨 **Utolsó CO2 csere:** {data['co2_csere']}")

# Fő navigáció
tab_csapok, tab_csere, tab_kuka, tab_admin = st.tabs(
    [
        "🚰 Aktuális Csaplista",
        "🔄 Hordócsere (Pultos)",
        "🗑️ Üres Hordók (Kuka)",
        "⚙️ Menedzsment",
    ]
)

# 1. AKTUÁLIS CSAPLISTA
with tab_csapok:
    st.subheader("Aktív csapok állapota")
    csap_lista = []
    for c in data["csapok"]:
        csap_lista.append(
            {
                "Csap": f"#{c['id']}",
                "Jelenlegi sör": c["jelenlegi"] if c["jelenlegi"] else "— ÜRES —",
                "Utolsó csere": c["datum"],
                "Következő 1.": (
                    c["kovetkezo"][0] if len(c["kovetkezo"]) > 0 else "—"
                ),
                "Következő 2.": (
                    c["kovetkezo"][1] if len(c["kovetkezo"]) > 1 else "—"
                ),
                "Következő 3.": (
                    c["kovetkezo"][2] if len(c["kovetkezo"]) > 2 else "—"
                ),
            }
        )
    st.dataframe(pd.DataFrame(csap_lista), use_container_width=True, hide_index=True)

# 2. HORDÓCSERE MŰVELET
with tab_csere:
    st.subheader("Hordó cseréje a csapon")
    st.write(
        "Válaszd ki a csapot! A gomb megnyomásával a jelenlegi sör a **Kukába** kerül, és a soron következő sör lép a helyére."
    )

    csap_options = [f"#{c['id']} - {c['jelenlegi']}" for c in data["csapok"]]
    valasztott = st.selectbox("Melyik csapon volt csere?", csap_options)
    csap_id = int(valasztott.split(" ")[0].replace("#", ""))

    if st.button("🚀 Hordócsere Rögzítése", type="primary"):
        target_csap = next(c for c in data["csapok"] if c["id"] == csap_id)

        # Régi sör kukába
        if target_csap["jelenlegi"]:
            data["kuka"].append(target_csap["jelenlegi"])

        # Következő sör előreléptetése
        if len(target_csap["kovetkezo"]) > 0:
            target_csap["jelenlegi"] = target_csap["kovetkezo"].pop(0)
        else:
            target_csap["jelenlegi"] = ""

        target_csap["datum"] = datetime.datetime.now().strftime("%Y-%m-%d")

        save_data(data)
        st.success(
            f"Csap #{csap_id} frissítve! Új sör: {target_csap['jelenlegi'] if target_csap['jelenlegi'] else 'Nincs következő sör'}"
        )
        st.rerun()

# 3. KUKA / ÜRES HORDÓK
with tab_kuka:
    st.subheader("Futárra váró üres hordók")
    if data["kuka"]:
        kuka_df = (
            pd.DataFrame(data["kuka"], columns=["Sör neve"])
            .value_counts()
            .reset_index(name="Darabszám")
        )
        st.dataframe(kuka_df, use_container_width=True, hide_index=True)

        if st.button("🚚 Futár elvitte az üres hordókat (Kuka ürítése)"):
            data["kuka"] = []
            save_data(data)
            st.success("Kuka kiürítve!")
            st.rerun()
    else:
        st.info("Jelenleg nincs üres hordó a kukában.")

# 4. MENEDZSMENT / BEÁLLÍTÁSOK
with tab_admin:
    st.subheader("Új várakozó hordó hozzáadása egy csaphoz")
    target_csap_admin = st.selectbox(
        "Csap kiválasztása",
        [f"#{c['id']}" for c in data["csapok"]],
        key="admin_csap",
    )
    admin_csap_id = int(target_csap_admin.replace("#", ""))
    uj_sor = st.text_input("Sör neve")

    if st.button("Hordó hozzáadása a várakozási sorhoz"):
        if uj_sor:
            target_c = next(c for c in data["csapok"] if c["id"] == admin_csap_id)
            target_c["kovetkezo"].append(uj_sor)
            save_data(data)
            st.success(f"Hozzáadva a #{admin_csap_id} csaphoz: {uj_sor}")
            st.rerun()

    st.markdown("---")
    st.subheader("Karbantartási dátumok frissítése")
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        if st.button("🧼 Csapmosás elvégezve ma"):
            data["csapmosas"] = datetime.datetime.now().strftime("%Y-%m-%d")
            save_data(data)
            st.rerun()
    with col_a2:
        if st.button("💨 CO2 csere elvégezve ma"):
            data["co2_csere"] = datetime.datetime.now().strftime("%Y-%m-%d")
            save_data(data)
            st.rerun()
