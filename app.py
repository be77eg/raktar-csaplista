import datetime
import json
import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Csaplista & Hordókövető", page_icon="🍺", layout="wide"
)

DATA_FILE = "csaplista_data.json"

# Alapértelmezett színpaletta a sörökhöz
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
        "raktar": [
            "Fake Your Pils",
            "Grain Cosmos",
            "Dark Vanilla Sky",
            "Let's Jump",
        ],
        "szinek": DEFAULT_COLORS,
        "csapmosas": "2026-02-27",
        "co2_csere": "2026-07-26",
        "history": [],
    }


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


data = load_data()
if "raktar" not in data:
    data["raktar"] = []
if "szinek" not in data:
    data["szinek"] = DEFAULT_COLORS

# Színformázó segédfüggvény
def format_beer_badge(beer_name):
    if not beer_name or beer_name == "— ÜRES —":
        return "<span style='color: #888;'>— ÜRES —</span>"
    color = data["szinek"].get(beer_name, "#3498DB")
    return f"<span style='background-color: {color}; color: #ffffff; padding: 3px 8px; border-radius: 12px; font-weight: bold; display: inline-block;'>{beer_name}</span>"


st.title("🍺 Csaplista & Hordókövető")

# Karbantartási információk
col_k1, col_k2 = st.columns(2)
with col_k1:
    st.info(f"🧼 **Utolsó csapmosás:** {data.get('csapmosas', '—')}")
with col_k2:
    st.warning(f"💨 **Utolsó CO2 csere:** {data.get('co2_csere', '—')}")

# Visszavonás gomb
if data.get("history") and len(data["history"]) > 0:
    if st.button("↩️ Legutóbbi hordócsere visszavonása"):
        prev_state = data["history"].pop()
        data["csapok"] = prev_state["csapok"]
        data["kuka"] = prev_state["kuka"]
        if "raktar" in prev_state:
            data["raktar"] = prev_state["raktar"]
        save_data(data)
        st.success("Sikeresen visszavontad az utolsó cserét!")
        st.rerun()

tab_csapok, tab_kuka, tab_admin = st.tabs(
    ["🚰 Csapok (1-12)", "🗑️ Üres Hordók (Kuka)", "⚙️ Menedzsment & Raktár"]
)

# 1. TAB: CSAPLISTA
with tab_csapok:
    st.subheader("Aktív Csapok Állapota")

    # Táblázat adatok összeállítása
    table_rows = []
    for c in data["csapok"]:
        jelenlegi_html = format_beer_badge(c["jelenlegi"])

        if c["kovetkezo"]:
            kov_list = [format_beer_badge(k) for k in c["kovetkezo"]]
            kovetkezo_html = " ➜ ".join(kov_list)
        else:
            kovetkezo_html = (
                "<span style='color: #777;'>Nincs következő</span>"
            )

        table_rows.append(
            {
                "Csap": f"<b>#{c['id']}</b>",
                "Jelenlegi sör": jelenlegi_html,
                "Következő hordók": kovetkezo_html,
                "Utolsó csere": c["datum"],
            }
        )

    df = pd.DataFrame(table_rows)

    # Egyedi HTML Táblázat generálása (Középre rendezett, nincs szétesve, tiszta sormegjelenítés)
    table_html = """
    <div style="overflow-x: auto; border: 1px solid #333; border-radius: 8px;">
        <table style="width: 100%; border-collapse: collapse; text-align: center; font-family: sans-serif;">
            <thead>
                <tr style="background-color: #262730; color: #ffffff; border-bottom: 2px solid #444;">
                    <th style="padding: 12px; text-align: center;">Csap</th>
                    <th style="padding: 12px; text-align: center;">Jelenlegi sör</th>
                    <th style="padding: 12px; text-align: center;">Következő hordók</th>
                    <th style="padding: 12px; text-align: center;">Utolsó csere</th>
                </tr>
            </thead>
            <tbody>
    """

    for idx, row in df.iterrows():
        bg = "#1e1e1e" if idx % 2 == 0 else "#262626"
        table_html += f"""
        <tr style="background-color: {bg}; border-bottom: 1px solid #333;">
            <td style="padding: 10px; text-align: center; font-size: 1.1em;">{row['Csap']}</td>
            <td style="padding: 10px; text-align: center;">{row['Jelenlegi sör']}</td>
            <td style="padding: 10px; text-align: center;">{row['Következő hordók']}</td>
            <td style="padding: 10px; text-align: center; color: #bbb; font-size: 0.9em;">{row['Utolsó csere']}</td>
        </tr>
        """

    table_html += "</tbody></table></div>"

    st.markdown(table_html, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("⚡ Gyors Hordócsere")

    csap_opciok = [
        f"#{c['id']} — {c['jelenlegi'] if c['jelenlegi'] else 'ÜRES'}"
        for c in data["csapok"]
    ]
    valasztott_csap_str = st.selectbox(
        "Válaszd ki a cserélendő csapot:", csap_opciok, key="swap_select_box"
    )

    if st.button("🔄 Hordócsere Végrehajtása", type="primary"):
        c_id = int(valasztott_csap_str.split(" ")[0].replace("#", ""))
        c = next(item for item in data["csapok"] if item["id"] == c_id)

        # Állapot mentése a visszavonhatóságért
        if "history" not in data:
            data["history"] = []
        data["history"].append(
            {
                "csapok": json.loads(json.dumps(data["csapok"])),
                "kuka": list(data["kuka"]),
                "raktar": list(data.get("raktar", [])),
            }
        )
        if len(data["history"]) > 5:
            data["history"].pop(0)

        # Csere végrehajtása
        if c["jelenlegi"]:
            data["kuka"].append(c["jelenlegi"])

        if len(c["kovetkezo"]) > 0:
            c["jelenlegi"] = c["kovetkezo"].pop(0)
        else:
            c["jelenlegi"] = ""

        c["datum"] = datetime.datetime.now().strftime("%Y-%m-%d")

        save_data(data)
        st.success(f"#{c_id} csap sikeresen kicserélve!")
        st.rerun()

# 2. TAB: KUKA
with tab_kuka:
    st.subheader("Futárra Váró Üres Hordók")
    st.metric(label="Összes üres hordó", value=f"{len(data['kuka'])} db")

    if data["kuka"]:
        kuka_df = (
            pd.DataFrame(data["kuka"], columns=["Sör neve"])
            .value_counts()
            .reset_index(name="Darabszám (db)")
        )
        st.dataframe(kuka_df, use_container_width=True, hide_index=True)

        if st.button("🚚 Kuka Ürítése (Elvitte a futár)", type="primary"):
            data["kuka"] = []
            save_data(data)
            st.success("Kuka kiürítve!")
            st.rerun()
    else:
        st.info("Nincs üres hordó a kukában.")

# 3. TAB: MENEDZSMENT & RAKTÁR
with tab_admin:
    st.subheader("📦 Raktárkészlet és Sörök Színei")

    col_r1, col_r2 = st.columns([2, 1])

    with col_r1:
        if data.get("raktar"):
            raktar_df = (
                pd.DataFrame(data["raktar"], columns=["Sör neve"])
                .value_counts()
                .reset_index(name="Készlet (db)")
            )

            # Szín oszlop hozzáadása
            raktar_df["Színkód"] = raktar_df["Sör neve"].apply(
                lambda x: data["szinek"].get(x, "#3498DB")
            )
            st.dataframe(raktar_df, use_container_width=True, hide_index=True)
        else:
            st.info("A raktár jelenleg üres.")

    with col_r2:
        st.markdown("**Új sör / hordó érkezése:**")
        uj_sor_nev = st.text_input("Sör neve:", key="input_raktar_name")
        valasztott_szin = st.color_picker(
            "Sör színe a táblázatban:", "#3498DB", key="color_picker"
        )

        if st.button("➕ Hozzáadás Raktárhoz"):
            if uj_sor_nev.strip():
                s_nev = uj_sor_nev.strip()
                data["raktar"].append(s_nev)
                data["szinek"][s_nev] = valasztott_szin
                save_data(data)
                st.success(f"'{s_nev}' hozzáadva a raktárhoz!")
                st.rerun()

    st.markdown("---")
    st.subheader("➡️ Várakozó hordó hozzáadása egy csaphoz")

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        target_csap = st.selectbox(
            "Melyik csaphoz adjuk hozzá?",
            [f"#{c['id']} — {c['jelenlegi']}" for c in data["csapok"]],
            key="add_to_tap_select",
        )
        c_id = int(target_csap.split(" ")[0].replace("#", ""))

    with col_m2:
        raktar_opciok = sorted(list(set(data.get("raktar", []))))
        valasztott_raktar_sor = st.selectbox(
            "Válassz hordót a Raktárból:",
            ["-- Válassz --"] + raktar_opciok,
            key="select_from_wh",
        )

    if st.button("Hordó áthelyezése a csap várakozó sorába", type="primary"):
        if valasztott_raktar_sor != "-- Válassz --":
            target_c = next(c for c in data["csapok"] if c["id"] == c_id)
            target_c["kovetkezo"].append(valasztott_raktar_sor)

            # Levonás a raktárból
            if valasztott_raktar_sor in data["raktar"]:
                data["raktar"].remove(valasztott_raktar_sor)

            save_data(data)
            st.success(f"Hordó hozzáadva a #{c_id} csaphoz!")
            st.rerun()

    st.markdown("---")
    st.subheader("↩️ Hordó VISSZAHÍVÁSA a csaplistáról a Raktárba")
    st.caption(
        "Módosult a sorrend? Itt visszaveheted a várakozó hordót a raktárba."
    )

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        vissza_csap = st.selectbox(
            "Melyik csapról hívjuk vissza a hordót?",
            [
                f"#{c['id']} — ({len(c['kovetkezo'])} db várakozik)"
                for c in data["csapok"]
                if len(c["kovetkezo"]) > 0
            ],
            key="recall_tap_select",
        )

    if vissza_csap:
        v_id = int(vissza_csap.split(" ")[0].replace("#", ""))
        target_v_c = next(c for c in data["csapok"] if c["id"] == v_id)
        utolso_hordo = target_v_c["kovetkezo"][-1]

        with col_v2:
            st.write(f"Visszahívandó hordó: **{utolso_hordo}**")
            if st.button("↩️ Visszahívás Raktárba"):
                recalled = target_v_c["kovetkezo"].pop()
                data["raktar"].append(recalled)
                save_data(data)
                st.success(
                    f"'{recalled}' visszakerült a raktárba a #{v_id} csapról!"
                )
                st.rerun()

    st.markdown("---")
    st.subheader("🧼 Karbantartás Regisztrálása")
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
