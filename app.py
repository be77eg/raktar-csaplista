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
        "kuka_history": [],
    }


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


data = load_data()
if "raktar" not in data:
    data["raktar"] = []
if "szinek" not in data:
    data["szinek"] = DEFAULT_COLORS
if "kuka_history" not in data:
    data["kuka_history"] = []

if "confirm_wash" not in st.session_state:
    st.session_state["confirm_wash"] = False
if "confirm_co2" not in st.session_state:
    st.session_state["confirm_co2"] = False
if "confirm_delete_beer" not in st.session_state:
    st.session_state["confirm_delete_beer"] = None
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "🚰 Csapok"


def format_beer_badge(beer_name):
    if not beer_name or beer_name == "— ÜRES —":
        return "<span style='color: #888; font-size: 0.8rem;'>— ÜRES —</span>"

    base_name = beer_name.replace(" (tört)", "").strip()
    color = data["szinek"].get(base_name, "#3498DB")

    return f"<span style='background-color: {color}; color: #ffffff; padding: 4px 10px; border-radius: 8px; font-weight: bold; font-size: 0.85rem; display: inline-block; white-space: nowrap;'>{beer_name}</span>"


def get_recommended_tap_option_index(beer_name, csapok):
    base_beer = beer_name.replace(" (tört)", "").strip()

    for idx, c in enumerate(csapok):
        if c["jelenlegi"] == base_beer:
            return idx + 1

    for idx, c in enumerate(csapok):
        if base_beer in c["kovetkezo"]:
            return idx + 1

    return 0


# DYNAMIKUS STÍLUSOK (5. és 2. PONT ELEMEI)
st.markdown(
    f"""
    <style>
        /* Selectbox billentyűzet tiltás / gépelés megelőzése */
        div[data-baseweb="select"] input {{
            pointer-events: none !important;
        }}
        
        /* 5. PONT: Dinamikus Navigációs Gombok Színei */
        div.stButton > button[key="nav_tap"] {{
            background-color: {"#1E88E5" if st.session_state["active_tab"] == "🚰 Csapok" else "#222"} !important;
            color: white !important;
            border-color: #1E88E5 !important;
            font-size: 1.05rem !important;
            font-weight: bold !important;
        }}
        div.stButton > button[key="nav_trash"] {{
            background-color: {"#E53935" if st.session_state["active_tab"] == "🗑️ Üres Hordók" else "#222"} !important;
            color: white !important;
            border-color: #E53935 !important;
            font-size: 1.05rem !important;
            font-weight: bold !important;
        }}
        div.stButton > button[key="nav_mgm"] {{
            background-color: {"#43A047" if st.session_state["active_tab"] == "⚙️ Menedzsment & Raktár" else "#222"} !important;
            color: white !important;
            border-color: #43A047 !important;
            font-size: 1.05rem !important;
            font-weight: bold !important;
        }}

        /* 1. PONT: Csapmosás (Rózsaszín) és CO2 (Kék) gombok alapszínei */
        div.stButton > button[key="btn_wash_act"] {{
            background-color: #E91E63 !important;
            color: white !important;
            border-color: #E91E63 !important;
        }}
        div.stButton > button[key="btn_co2_act"] {{
            background-color: #2196F3 !important;
            color: white !important;
            border-color: #2196F3 !important;
        }}

        /* 7. PONT: Zöld mentés gombok a raktár hozzáadásnál */
        div.stButton > button[key="add_exist_btn"],
        div.stButton > button[key="add_tort_btn"],
        div.stButton > button[key="add_new_beer_btn"] {{
            background-color: #2E7D32 !important;
            color: white !important;
            border-color: #2E7D32 !important;
        }}
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🍺 Csaplista & Hordókövető")

col_k1, col_k2 = st.columns(2)
with col_k1:
    st.info(f"🧼 **Utolsó csapmosás:** {data.get('csapmosas', '—')}")
with col_k2:
    st.warning(f"💨 **Utolsó CO2 csere:** {data.get('co2_csere', '—')}")

# 5. PONT: NAVIGÁCIÓS GOMBOK KÖZÉPRE ZÁRVA ÉS SZÍNEZVE
st.markdown("<br>", unsafe_allow_html=True)
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([1, 2, 2, 2, 1])

with nav_col2:
    if st.button("🚰 Csapok", key="nav_tap", use_container_width=True):
        st.session_state["active_tab"] = "🚰 Csapok"
        st.rerun()

with nav_col3:
    if st.button(
        "🗑️ Üres Hordók", key="nav_trash", use_container_width=True
    ):
        st.session_state["active_tab"] = "🗑️ Üres Hordók"
        st.rerun()

with nav_col4:
    if st.button(
        "⚙️ Menedzsment & Raktár", key="nav_mgm", use_container_width=True
    ):
        st.session_state["active_tab"] = "⚙️ Menedzsment & Raktár"
        st.rerun()

st.markdown("<hr style='margin: 15px 0 25px 0;'>", unsafe_allow_html=True)

# 1. TAB: CSAPLISTA
if st.session_state["active_tab"] == "🚰 Csapok":
    if data.get("history") and len(data["history"]) > 0:
        if st.button("↩️ Legutóbbi hordócsere visszavonása", key="undo_btn_tap_tab"):
            prev_state = data["history"].pop()
            data["csapok"] = prev_state["csapok"]
            data["kuka"] = prev_state["kuka"]
            if "raktar" in prev_state:
                data["raktar"] = prev_state["raktar"]
            save_data(data)
            st.success("Sikeresen visszavontad az utolsó cserét!")
            st.rerun()

    st.subheader("Aktív Csapok Állapota")

    st.markdown(
        """
        <style>
            [data-testid="column"] { min-width: 0 !important; }
            .stButton button { width: 100%; min-width: 70px; }
        </style>
    """,
        unsafe_allow_html=True,
    )

    h1, h2, h3, h4, h5 = st.columns([1, 3, 4, 2, 2])
    h1.markdown("**Csap**")
    h2.markdown("**Jelenlegi sör**")
    h3.markdown("**Következő hordók**")
    h4.markdown("**Utolsó csere**")
    h5.markdown("**Művelet**")
    st.markdown(
        "<hr style='margin: 2px 0 10px 0; border-color: #555;'>",
        unsafe_allow_html=True,
    )

    for c in data["csapok"]:
        c1, c2, c3, c4, c5 = st.columns(
            [1, 3, 4, 2, 2], vertical_alignment="center"
        )

        with c1:
            st.markdown(f"**#{c['id']}**")

        with c2:
            st.markdown(
                format_beer_badge(c["jelenlegi"]), unsafe_allow_html=True
            )

        with c3:
            if c["kovetkezo"]:
                kov_badges = [format_beer_badge(k) for k in c["kovetkezo"]]
                arrow = (
                    " <span style='color:#888; font-weight:bold;'>➜</span> "
                )
                st.markdown(
                    arrow.join(kov_badges), unsafe_allow_html=True
                )
            else:
                st.markdown(
                    "<span style='color: #666; font-size: 0.8rem;'>Nincs</span>",
                    unsafe_allow_html=True,
                )

        with c4:
            st.markdown(
                f"<span style='color: #aaa; font-size: 0.8rem;'>{c['datum']}</span>",
                unsafe_allow_html=True,
            )

        with c5:
            is_empty_tap = not (c["jelenlegi"] or c["kovetkezo"])
            if st.button(
                "🔄 Csere", key=f"btn_swap_{c['id']}", disabled=is_empty_tap
            ):
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

                if c["jelenlegi"]:
                    data["kuka"].append(c["jelenlegi"])

                if len(c["kovetkezo"]) > 0:
                    c["jelenlegi"] = c["kovetkezo"].pop(0)
                else:
                    c["jelenlegi"] = ""

                c["datum"] = datetime.datetime.now().strftime("%Y-%m-%d")
                save_data(data)
                st.rerun()

        st.markdown(
            "<hr style='margin: 4px 0; border-color: #222;'>",
            unsafe_allow_html=True,
        )

# 2. TAB: ÜRES HORDÓK (KUKA)
elif st.session_state["active_tab"] == "🗑️ Üres Hordók":
    st.subheader("Futárra Váró Üres Hordók")

    col_k_undo, col_k_save = st.columns(2)

    with col_k_undo:
        if data.get("kuka_history") and len(data["kuka_history"]) > 0:
            if st.button(
                "↩️ Legutóbbi elszállítás visszavonása",
                key="undo_kuka_btn",
            ):
                data["kuka"] = data["kuka_history"].pop()
                save_data(data)
                st.success("Elszállítás visszavonva, a hordók visszakerültek!")
                st.rerun()

    with col_k_save:
        if data.get("kuka_history") and len(data["kuka_history"]) > 0:
            if st.button(
                "🔒 Állapot véglegesítése (Elszállítások lezárása)",
                type="primary",
                key="lock_kuka_btn",
            ):
                data["kuka_history"] = []
                save_data(data)
                st.success(
                    "Elszállítások rögzítve! A visszavonási lehetőség lezárva."
                )
                st.rerun()

    st.metric(label="Összes üres hordó", value=f"{len(data['kuka'])} db")

    if data["kuka"]:
        kuka_counts = Counter(data["kuka"])
        for beer_name, count in sorted(kuka_counts.items()):
            k_col0, k_col1, k_col2, k_col3 = st.columns(
                [2, 3, 2, 2], vertical_alignment="center"
            )

            with k_col0:
                if st.button(
                    "↩️ Raktárba (tört)", key=f"return_wh_btn_{beer_name}"
                ):
                    data["kuka"].remove(beer_name)
                    tort_name = (
                        beer_name
                        if "(tört)" in beer_name
                        else f"{beer_name} (tört)"
                    )
                    data["raktar"].append(tort_name)

                    base_name = beer_name.replace(" (tört)", "").strip()
                    if (
                        base_name in data["szinek"]
                        and tort_name not in data["szinek"]
                    ):
                        data["szinek"][tort_name] = data["szinek"][base_name]

                    save_data(data)
                    st.success(
                        f"'{tort_name}' visszaküldve a raktárba tört hordóként!"
                    )
                    st.rerun()

            with k_col1:
                st.markdown(
                    f"{format_beer_badge(beer_name)} &nbsp;&nbsp; **{count} db**",
                    unsafe_allow_html=True,
                )

            with k_col2:
                take_count = st.number_input(
                    "Elvitt db:",
                    min_value=1,
                    max_value=count,
                    value=count,
                    key=f"take_num_{beer_name}",
                    label_visibility="collapsed",
                )

            with k_col3:
                if st.button(
                    "🚚 Elszállítás", key=f"take_btn_{beer_name}"
                ):
                    data["kuka_history"].append(list(data["kuka"]))
                    for _ in range(take_count):
                        if beer_name in data["kuka"]:
                            data["kuka"].remove(beer_name)
                    save_data(data)
                    st.success(
                        f"{take_count} db '{beer_name}' elszállítva!"
                    )
                    st.rerun()

            st.markdown(
                "<hr style='margin: 4px 0; border-color: #333;'>",
                unsafe_allow_html=True,
            )

        st.markdown("---")
        if st.button(
            "🚚 Összes üres hordó elszállítása (Teljes ürítés)",
            type="primary",
            key="empty_trash_btn",
        ):
            data["kuka_history"].append(list(data["kuka"]))
            data["kuka"] = []
            save_data(data)
            st.success("Minden üres hordó elszállítva!")
            st.rerun()
    else:
        st.info("Nincs üres hordó a kukában.")

# 3. TAB: MENEDZSMENT & RAKTÁR
elif st.session_state["active_tab"] == "⚙️ Menedzsment & Raktár":
    st.subheader("🧼 Karbantartási Műveletek")

    # 1. PONT & 4. PONT: KARBANTARTÁSI GOMBOK ÉS MEGERŐSÍTÉSEK ARÁNYOS ELOSZTÁSA
    m1, m2 = st.columns(2)

    with m1:
        with st.container(border=True):
            if not st.session_state["confirm_wash"]:
                if st.button(
                    "🧼 Csap mosása",
                    key="btn_wash_act",
                    use_container_width=True,
                ):
                    st.session_state["confirm_wash"] = True
                    st.rerun()
            else:
                st.warning("❓ **Biztosan frissíted a csapmosást?**")
                wc1, wc2, wc3 = st.columns([2, 2, 3])
                with wc1:
                    if st.button(
                        "✅ Igen", key="save_wash_btn", use_container_width=True
                    ):
                        data["csapmosas"] = datetime.datetime.now().strftime(
                            "%Y-%m-%d"
                        )
                        save_data(data)
                        st.session_state["confirm_wash"] = False
                        st.success("Dátum frissítve!")
                        st.rerun()
                with wc2:
                    if st.button(
                        "❌ Mégse",
                        key="cancel_wash_btn",
                        use_container_width=True,
                    ):
                        st.session_state["confirm_wash"] = False
                        st.rerun()

    with m2:
        with st.container(border=True):
            if not st.session_state["confirm_co2"]:
                if st.button(
                    "💨 CO2 lecserélése",
                    key="btn_co2_act",
                    use_container_width=True,
                ):
                    st.session_state["confirm_co2"] = True
                    st.rerun()
            else:
                st.warning("❓ **Biztosan frissíted a CO2 cserét?**")
                cc1, cc2, cc3 = st.columns([2, 2, 3])
                with cc1:
                    if st.button(
                        "✅ Igen", key="save_co2_btn", use_container_width=True
                    ):
                        data["co2_csere"] = datetime.datetime.now().strftime(
                            "%Y-%m-%d"
                        )
                        save_data(data)
                        st.session_state["confirm_co2"] = False
                        st.success("Dátum frissítve!")
                        st.rerun()
                with cc2:
                    if st.button(
                        "❌ Mégse",
                        key="cancel_co2_btn",
                        use_container_width=True,
                    ):
                        st.session_state["confirm_co2"] = False
                        st.rerun()

    st.markdown("---")

    # 8. PONT: KÖZÉPRE ZÁRT TELJES HORDÓ KIMUTATÁS
    st.markdown(
        "<h3 style='text-align: center;'>📊 Teljes Hordó Készletnyilvántartás</h3>",
        unsafe_allow_html=True,
    )

    teli_csapokon = sum(1 for c in data["csapok"] if c["jelenlegi"])
    varakozo_csapokon = sum(len(c["kovetkezo"]) for c in data["csapok"])
    raktarban = len(data.get("raktar", []))
    osszes_teli = teli_csapokon + varakozo_csapokon + raktarban
    ures_kuka = len(data.get("kuka", []))

    st_col1, st_col2, st_col3, st_col4 = st.columns(4)
    st_col1.metric("ÖSSZES TELI HORDÓ", f"{osszes_teli} db")
    st_col2.metric("Csapon Lévő", f"{teli_csapokon} db")
    st_col3.metric("Csapra Várakozó", f"{varakozo_csapokon} db")
    st_col4.metric("Raktárban Lévő", f"{raktarban} db")

    st.markdown(
        f"<p style='text-align: center; color: #aaa; margin-top: 10px;'>➕ <b>Kiegészítés (Üres hordók a kukában):</b> {ures_kuka} db üres hordó vár elszállításra.</p>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.subheader("📦 Raktárkészlet Kezelése")

    # 6. PONT: ARÁNYOS TÉRKÖZÖLÉS A RAKTÁRBAN
    col_r1, col_r2 = st.columns([3.2, 2.3])

    with col_r1:
        st.markdown("**Raktárban lévő hordók kezelése és csaphoz rendelése:**")
        if data.get("raktar"):
            raktar_counts = Counter(data["raktar"])

            csap_options = ["— Válassz csapot —"] + [
                f"#{c['id']} ({c['jelenlegi'] if c['jelenlegi'] else 'ÜRES'})"
                for c in data["csapok"]
            ]

            for beer_name, count in sorted(raktar_counts.items()):
                # Arányosított oszlopok
                r_col1, r_col2, r_col3, r_col4 = st.columns(
                    [3, 2.5, 1.5, 1.5], vertical_alignment="center"
                )

                default_tap_index = get_recommended_tap_option_index(
                    beer_name, data["csapok"]
                )

                with r_col1:
                    st.markdown(
                        f"{format_beer_badge(beer_name)} &nbsp; **({count} db)**",
                        unsafe_allow_html=True,
                    )

                with r_col2:
                    # 2. PONT: NEM SZERKESZTHETŐ SELECTBOX
                    selected_tap_str = st.selectbox(
                        "Csap:",
                        csap_options,
                        index=default_tap_index,
                        key=f"wh_select_tap_{beer_name}",
                        label_visibility="collapsed",
                    )

                with r_col3:
                    if st.button(
                        "➕ Csapra",
                        key=f"wh_add_btn_{beer_name}",
                        use_container_width=True,
                    ):
                        if selected_tap_str == "— Válassz csapot —":
                            st.error(
                                "Kérlek válassz ki egy csapot a legördülő menüből!"
                            )
                        else:
                            target_c_id = int(
                                selected_tap_str.split(" ")[0].replace("#", "")
                            )
                            target_c = next(
                                c
                                for c in data["csapok"]
                                if c["id"] == target_c_id
                            )

                            target_c["kovetkezo"].append(beer_name)
                            data["raktar"].remove(beer_name)

                            save_data(data)
                            st.success(
                                f"'{beer_name}' hozzáadva a #{target_c_id} csaphoz!"
                            )
                            st.rerun()

                with r_col4:
                    # 4. PONT: JOBB ELOSZTÁSÚ MEGERŐSÍTŐ TÖRLES
                    if (
                        st.session_state["confirm_delete_beer"]
                        == beer_name
                    ):
                        del_c1, del_c2 = st.columns(2)
                        with del_c1:
                            if st.button("✅", key=f"confirm_del_{beer_name}"):
                                data["raktar"].remove(beer_name)
                                st.session_state["confirm_delete_beer"] = None
                                save_data(data)
                                st.warning(
                                    f"1 db '{beer_name}' törölve a raktárból!"
                                )
                                st.rerun()
                        with del_c2:
                            if st.button("❌", key=f"cancel_del_{beer_name}"):
                                st.session_state["confirm_delete_beer"] = None
                                st.rerun()
                    else:
                        if st.button(
                            "🗑️ Törlés",
                            key=f"wh_del_btn_{beer_name}",
                            use_container_width=True,
                        ):
                            st.session_state["confirm_delete_beer"] = (
                                beer_name
                            )
                            st.rerun()

                st.markdown(
                    "<hr style='margin: 4px 0; border-color: #333;'>",
                    unsafe_allow_html=True,
                )
        else:
            st.info("A raktár jelenleg üres.")

    # 7. PONT: KERETES HOZZÁADÁS SZEKCIÓ VIZUÁLISAN ELKÜLÖNÍTVE
    with col_r2:
        with st.container(border=True):
            st.markdown("### ➕ Hordó Hozzáadása Raktárhoz")

            add_type = st.segmented_control(
                "Típus kiválasztása:",
                [
                    "Meglévő sörök",
                    "➕ Tört hordó hozzáadása",
                    "Vadonatúj sör",
                ],
                default="Meglévő sörök",
                key="add_type_segmented",
            )

            if add_type == "Meglévő sörök":
                # 3. PONT: TÖRT HORDÓK KISZŰRÉSE A MEGLÉVŐ SÖRÖKBŐL
                minden_sor = sorted(list(set(data.get("raktar", []))))
                tisztitott_sorok = [
                    s for s in minden_sor if "(tört)" not in s
                ]

                if tisztitott_sorok:
                    valasztott_meglevo = st.selectbox(
                        "Válassz teljes hordós sört:",
                        tisztitott_sorok,
                        key="select_existing_beer",
                    )
                    db_szam = st.number_input(
                        "Darabszám:",
                        min_value=1,
                        value=1,
                        key="num_existing_beer",
                    )

                    if st.button(
                        "➕ Hozzáadás Raktárhoz",
                        key="add_exist_btn",
                        use_container_width=True,
                    ):
                        for _ in range(db_szam):
                            data["raktar"].append(valasztott_meglevo)
                        save_data(data)
                        st.success(
                            f"{db_szam} db '{valasztott_meglevo}' hozzáadva!"
                        )
                        st.rerun()
                else:
                    st.warning("Nincs teljes hordó a raktári listában!")

            elif add_type == "➕ Tört hordó hozzáadása":
                # 3. PONT: KÜLÖN OPTIÓ TÖRT HORDÓ RÖGZÍTÉSÉRE
                minden_alap_sor = sorted(
                    list(
                        set(
                            [
                                s.replace(" (tört)", "").strip()
                                for s in data.get("raktar", [])
                            ]
                        )
                    )
                )

                if minden_alap_sor:
                    valasztott_tort_alap = st.selectbox(
                        "Válassz sört a tört hordóhoz:",
                        minden_alap_sor,
                        key="select_tort_beer",
                    )
                    db_szam_tort = st.number_input(
                        "Darabszám (tört):",
                        min_value=1,
                        value=1,
                        key="num_tort_beer",
                    )

                    if st.button(
                        "➕ Tört Hordó Hozzáadása",
                        key="add_tort_btn",
                        use_container_width=True,
                    ):
                        tort_teljes_nev = f"{valasztott_tort_alap} (tört)"
                        for _ in range(db_szam_tort):
                            data["raktar"].append(tort_teljes_nev)

                        if valasztott_tort_alap in data["szinek"]:
                            data["szinek"][tort_teljes_nev] = data["szinek"][
                                valasztott_tort_alap
                            ]

                        save_data(data)
                        st.success(
                            f"{db_szam_tort} db '{tort_teljes_nev}' hozzáadva!"
                        )
                        st.rerun()
                else:
                    st.warning("Előbb vegyél fel legalább egy rendes sört!")

            else:
                uj_sor_nev = st.text_input(
                    "Új sör neve:", key="input_raktar_name"
                )
                valasztott_szin = st.color_picker(
                    "Sör színe a táblázatban:", "#3498DB", key="color_picker"
                )
                db_szam_uj = st.number_input(
                    "Darabszám:", min_value=1, value=1, key="num_new_beer"
                )

                if st.button(
                    "➕ Új Sör Mentése",
                    key="add_new_beer_btn",
                    use_container_width=True,
                ):
                    if uj_sor_nev.strip():
                        s_nev = uj_sor_nev.strip()
                        for _ in range(db_szam_uj):
                            data["raktar"].append(s_nev)
                        data["szinek"][s_nev] = valasztott_szin
                        save_data(data)
                        st.success(
                            f"{db_szam_uj} db '{s_nev}' hozzáadva a raktárhoz!"
                        )
                        st.rerun()

    st.markdown("---")
    st.subheader("↩️ Várakozó Hordó VISSZAHÍVÁSA a Raktárba")

    has_waiting = False
    for c in data["csapok"]:
        if c["kovetkezo"]:
            has_waiting = True
            v_col1, v_col2, v_col3 = st.columns(
                [2, 4, 2], vertical_alignment="center"
            )

            with v_col1:
                st.markdown(f"**#{c['id']} Csap várakozói:**")

            with v_col2:
                kov_badges = [format_beer_badge(k) for k in c["kovetkezo"]]
                arrow_html = (
                    " <span style='color: #888; font-weight: bold;'>➜</span> "
                )
                st.markdown(
                    arrow_html.join(kov_badges), unsafe_allow_html=True
                )

            with v_col3:
                utolso_hordo = c["kovetkezo"][-1]
                if st.button(
                    f"↩️ Visszahívás", key=f"recall_btn_{c['id']}"
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
