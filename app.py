import datetime
import json
import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Csaplista & Hordókövető", page_icon="🍺", layout="wide"
)

DATA_FILE = "csaplista_data.json"


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
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
                "kovetkezo": ["The Age of Heat Dome", "The Age of Heat Dome"],
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
        "history": [],
    }


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_active_beers(data):
    beers = set()
    for c in data["csapok"]:
        if c["jelenlegi"]:
            beers.add(c["jelenlegi"])
        for k in c["kovetkezo"]:
            if k:
                beers.add(k)
    for kuka_item in data["kuka"]:
        if kuka_item:
            beers.add(kuka_item)
    return sorted(list(beers))


data = load_data()

st.title("Csaplista & Hordókövető")

col_k1, col_k2 = st.columns(2)
with col_k1:
    st.info(f"🧼 **Utolsó csapmosás:** {data.get('csapmosas', '—')}")
with col_k2:
    st.warning(f"💨 **Utolsó CO2 csere:** {data.get('co2_csere', '—')}")

# Visszavonás gomb
if data.get("history") and len(data["history"]) > 0:
    if st.button("↩️ Utolsó hordócsere visszavonása"):
        prev_state = data["history"].pop()
        data["csapok"] = prev_state["csapok"]
        data["kuka"] = prev_state["kuka"]
        save_data(data)
        st.success("Sikeres visszavonás!")
        st.rerun()

tab_csapok, tab_kuka, tab_admin = st.tabs(
    ["🚰 Aktuális Csaplista", "🗑️ Üres Hordók (Kuka)", "⚙️ Menedzsment"]
)

# 1. CSAPLISTA TÁBLÁZAT + GYORS CSERE
with tab_csapok:
    st.subheader("Aktív csapok állapota")

    table_data = []
    for c in data["csapok"]:
        table_data.append(
            {
                "Csap": f"#{c['id']}",
                "Jelenlegi sör": (
                    c["jelenlegi"] if c["jelenlegi"] else "— ÜRES —"
                ),
                "Utolsó csere": c["datum"],
                "Következő sörök": (
                    " ➜ ".join(c["kovetkezo"])
                    if c["kovetkezo"]
                    else "Nincs következő"
                ),
            }
        )

    df_display = pd.DataFrame(table_data)
    st.dataframe(df_display, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("⚡ Gyors Hordócsere")

    csap_options = [
        f"#{c['id']} — {c['jelenlegi'] if c['jelenlegi'] else 'ÜRES'}"
        for c in data["csapok"]
    ]
    valasztott = st.selectbox(
        "Válaszd ki a cserélendő csapot:", csap_options, key="quick_swap_select"
    )

    if st.button("🔄 Hordócsere végrehajtása", type="primary"):
        csap_id = int(valasztott.split(" ")[0].replace("#", ""))
        c = next(item for item in data["csapok"] if item["id"] == csap_id)

        if "history" not in data:
            data["history"] = []

        data["history"].append(
            {
                "csapok": json.loads(json.dumps(data["csapok"])),
                "kuka": list(data["kuka"]),
            }
        )
        if len(data["history"]) > 5:
            data["history"].pop(0)

        if c["jelenlegi"]:
            data["kuka"].append(c["jelenlegi"])

        if len(c["kovetkezo"]) > 0:
            c["jelenlegi"] = c["kovetkezo"].pop(0)
        else:
            c["jelenlegi"] = ""

        c["datum"] = datetime.datetime.now().strftime("%Y-%m-%d")

        save_data(data)
        st.success(f"Csap #{csap_id} sikeresen frissítve!")
        st.rerun()

# 2. KUKA / ÜRES HORDÓK
with tab_kuka:
    st.subheader("Futárra váró üres hordók")

    osszes_kuka = len(data["kuka"])
    st.metric(label="Összes üres hordó száma", value=f"{osszes_kuka} db")

    if data["kuka"]:
        st.markdown("### Bontás sörök szerint:")
        kuka_df = (
            pd.DataFrame(data["kuka"], columns=["Sör neve"])
            .value_counts()
            .reset_index(name="Darabszám (db)")
        )

        st.dataframe(kuka_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        if st.button(
            "🚚 Futár elvitte az üres hordókat (Kuka ürítése)", type="primary"
        ):
            data["kuka"] = []
            save_data(data)
            st.success("Kuka kiürítve!")
            st.rerun()
    else:
        st.info("Jelenleg nincs üres hordó a kukában.")

# 3. MENEDZSMENT / BEÁLLÍTÁSOK
with tab_admin:
    st.subheader("Új várakozó hordó hozzáadása egy csaphoz")

    c_select, b_select = st.columns(2)

    with c_select:
        target_csap_admin = st.selectbox(
            "Melyik csaphoz adjuk hozzá?",
            [f"#{c['id']}" for c in data["csapok"]],
            key="admin_csap",
        )
        admin_csap_id = int(target_csap_admin.replace("#", ""))

    with b_select:
        active_beers = get_active_beers(data)
        options = ["➕ Új sör hozzáadása"] + active_beers

        valasztott_sor = st.selectbox("Sör kiválasztása listából", options)

        if valasztott_sor == "➕ Új sör hozzáadása":
            uj_sor_nev = st.text_input("Új sör neve:")
        else:
            uj_sor_nev = valasztott_sor

    if st.button("Hordó hozzáadása a várakozási sorhoz", type="primary"):
        if uj_sor_nev.strip():
            target_c = next(
                c for c in data["csapok"] if c["id"] == admin_csap_id
            )
            target_c["kovetkezo"].append(uj_sor_nev.strip())
            save_data(data)
            st.success(
                f"Sikeresen hozzáadva a #{admin_csap_id} csaphoz: {uj_sor_nev.strip()}"
            )
            st.rerun()
        else:
            st.error("Kérlek add meg a sör nevét!")

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
