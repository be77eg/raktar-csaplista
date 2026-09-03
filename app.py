from collections import Counter
import datetime
import json
import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Csaplista & Hordókövető", page_icon="🍺", layout="wide"
)

DATA_FILE = "csaplista_data.json"

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


def format_beer_badge(beer_name):
    if not beer_name or beer_name == "— ÜRES —":
        return "<span style='color: #888;'>— ÜRES —</span>"
    color = data["szinek"].get(beer_name, "#3498DB")
    return f"<span style='background-color: {color}; color: #ffffff; padding: 4px 10px; border-radius: 12px; font-weight: bold; display: inline-block;'>{beer_name}</span>"


st.title("🍺 Csaplista & Hordókövető")

col_k1, col_k2 = st.columns(2)
with col_k1:
    st.info(f"🧼 **Utolsó csapmosás:** {data.get('csapmosas', '—')}")
with col_k2:
    st.warning(f"💨 **Utolsó CO2 csere:** {data.get('co2_csere', '—')}")

# Visszavonás lehetőség
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

# 1. TAB: CSAPLISTA (Függőlegesen és vízszintesen középre rendezve)
with tab_csapok:
    st.subheader("Aktív Csapok Állapota")

    # Fejléc elrendezés (középre zárt szövegekkel)
    h_col1, h_col2, h_col3, h_col4, h_col5 = st.columns([1, 3, 4, 2, 2])
    with h_col1:
        st.markdown(
            "<div style='text-align: center;'><b>Csap</b></div>",
            unsafe_allow_html=True,
        )
    with h_col2:
        st.markdown(
            "<div style='text-align: center;'><b>Jelenlegi sör</b></div>",
            unsafe_allow_html=True,
        )
    with h_col3:
        st.markdown(
            "<div style='text-align: center;'><b>Következő hordók</b></div>",
            unsafe_allow_html=True,
        )
    with h_col4:
        st.markdown(
            "<div style='text-align: center;'><b>Utolsó csere</b></div>",
            unsafe_allow_html=True,
        )
    with h_col5:
        st.markdown(
            "<div style='text-align: center;'><b>Művelet</b></div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        "<hr style='margin: 4px 0 12px 0; border-color: #444;'>",
        unsafe_allow_html=True,
    )

    for idx, c in enumerate(data["csapok"]):
        with st.container():
            # align-items: center gondoskodik a függőleges középre igazításról
            col1, col2, col3, col4, col5 = st.columns(
                [1, 3, 4, 2, 2], vertical_alignment="center"
            )

            with col1:
                st.markdown(
                    f"<div style='text-align: center; font-size: 1.2em; font-weight: bold;'>#{c['id']}</div>",
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    f"<div style='text-align: center;'>{format_beer_badge(c['jelenlegi'])}</div>",
                    unsafe_allow_html=True,
                )

            with col3:
                if c["kovetkezo"]:
                    kov_badges = [format_beer_badge(k) for k in c["kovetkezo"]]
                    st.markdown(
                        f"<div style='text-align: center;'>{' ➜ '.join(kov_badges)}</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        "<div style='text-align: center; color: #777;'>Nincs következő</div>",
                        unsafe_allow_html=True,
                    )

            with col4:
                st.markdown(
                    f"<div style='text-align: center; color: #aaa;'>{c['datum']}</div>",
                    unsafe_allow_html=True,
                )

            with col5:
                # Középre igazított csere gomb
                _, btn_center, _ = st.columns([1, 2, 1])
                with btn_center:
                    if st.button("🔄 Csere", key=f"row_swap_btn_{c['id']}"):
                        if "history" not in data:
                            data["history"] = []
                        data["history"].append(
                            {
                                "csapok": json.loads(
                                    json.dumps(data["csapok"])
                                ),
                                "kuka": list(data["kuka"]),
                                "raktar": list(data.get("raktar", [])),
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

                        c["datum"] = datetime.datetime.now().strftime(
                            "%Y-%m-%d"
                        )
                        save_data(data)
                        st.rerun()

            st.markdown(
                "<hr style='margin: 6px 0; border-color: #222;'>",
                unsafe_allow_html=True,
            )

# 2. TAB: KUKA (Színes címkékkel)
with tab_kuka:
    st.subheader("Futárra Váró Üres Hordók")
    st.metric(label="Összes üres hordó", value=f"{len(data['kuka'])} db")

    if data["kuka"]:
        kuka_counts = Counter(data["kuka"])
        for beer_name, count in kuka_counts.items():
            k_col1, k_col2 = st.columns([3, 1], vertical_alignment="center")
            with k_col1:
                st.markdown(
                    f"{format_beer_badge(beer_name)} &nbsp;&nbsp; **{count} db**",
                    unsafe_allow_html=True,
                )
            st.markdown(
                "<hr style='margin: 4px 0; border-color: #333;'>",
                unsafe_allow_html=True,
            )

        if st.button(
            "🚚 Kuka Ürítése (Elvitte a futár)",
            type="primary",
            key="empty_trash_btn",
        ):
            data["kuka"] = []
            save_data(data)
            st.success("Kuka kiürítve!")
            st.rerun()
    else:
        st.info("Nincs üres hordó a kukában.")

# 3. TAB: MENEDZSMENT & RAKTÁR
with tab_admin:
    st.subheader("📦 Raktárkészlet és Közvetlen Csapra Helyezés")

    col_r1, col_r2 = st.columns([3, 2])

    with col_r1:
        if data.get("raktar"):
            raktar_counts = Counter(data["raktar"])
            csap_options = [
                f"#{c['id']} ({c['jelenlegi'] if c['jelenlegi'] else 'ÜRES'})"
                for c in data["csapok"]
            ]

            st.markdown("**Válassz hordót és küldd közvetlenül a csapra:**")

            for beer_name, count in raktar_counts.items():
                r_col1, r_col2, r_col3 = st.columns(
                    [3, 3, 2], vertical_alignment="center"
                )

                with r_col1:
                    st.markdown(
                        f"{format_beer_badge(beer_name)} &nbsp; **({count} db)**",
                        unsafe_allow_html=True,
                    )

                with r_col2:
                    selected_tap_str = st.selectbox(
                        "Csap:",
                        csap_options,
                        key=f"wh_select_tap_{beer_name}",
                        label_visibility="collapsed",
                    )

                with r_col3:
                    if st.button("➕ Csapra", key=f"wh_add_btn_{beer_name}"):
                        target_c_id = int(
                            selected_tap_str.split(" ")[0].replace("#", "")
                        )
                        target_c = next(
                            c for c in data["csapok"] if c["id"] == target_c_id
                        )

                        target_c["kovetkezo"].append(beer_name)
                        data["raktar"].remove(beer_name)

                        save_data(data)
                        st.success(
                            f"'{beer_name}' hozzáadva a #{target_c_id} csaphoz!"
                        )
                        st.rerun()

                st.markdown(
                    "<hr style='margin: 4px 0; border-color: #333;'>",
                    unsafe_allow_html=True,
                )
        else:
            st.info("A raktár jelenleg üres.")

    with col_r2:
        st.markdown("**Új sör regisztrálása a raktárba:**")
        uj_sor_nev = st.text_input("Sör neve:", key="input_raktar_name")
        valasztott_szin = st.color_picker(
            "Sör színe a táblázatban:", "#3498DB", key="color_picker"
        )

        if st.button("➕ Új sör hozzáadása"):
            if uj_sor_nev.strip():
                s_nev = uj_sor_nev.strip()
                data["raktar"].append(s_nev)
                data["szinek"][s_nev] = valasztott_szin
                save_data(data)
                st.success(f"'{s_nev}' hozzáadva a raktárhoz!")
                st.rerun()

    st.markdown("---")
    st.subheader("↩️ Hordók VISSZAHÍVÁSA a csaplistáról a Raktárba")
    st.caption("A várakozó sörök jól elkülönítve, közvetlenül visszahívhatók:")

    has_waiting = False
    for c in data["csapok"]:
        if c["kovetkezo"]:
            has_waiting = True
            with st.container():
                v_col1, v_col2, v_col3 = st.columns(
                    [2, 4, 2], vertical_alignment="center"
                )

                with v_col1:
                    st.markdown(f"**#{c['id']} Csap várakozó sora:**")

                with v_col2:
                    kov_badges = [format_beer_badge(k) for k in c["kovetkezo"]]
                    st.markdown(
                        " ➜ ".join(kov_badges), unsafe_allow_html=True
                    )

                with v_col3:
                    utolso_hordo = c["kovetkezo"][-1]
                    if st.button(
                        f"↩️ Utolsó ({utolso_hordo}) visszahívása",
                        key=f"recall_btn_{c['id']}",
                    ):
                        recalled = c["kovetkezo"].pop()
                        data["raktar"].append(recalled)
                        save_data(data)
                        st.success(
                            f"'{recalled}' visszakerült a raktárba a #{c['id']} csapról!"
                        )
                        st.rerun()

                st.markdown(
                    "<hr style='margin: 4px 0; border-color: #222;'>",
                    unsafe_allow_html=True,
                )

    if not has_waiting:
        st.info("Jelenleg egyetlen csapon sincs várakozó hordó.")

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
