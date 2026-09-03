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

# Megerősítési állapotok inicializálása
if "confirm_wash" not in st.session_state:
    st.session_state["confirm_wash"] = False
if "confirm_co2" not in st.session_state:
    st.session_state["confirm_co2"] = False


def format_beer_badge(beer_name):
    if not beer_name or beer_name == "— ÜRES —":
        return "<span style='color: #888; font-size: 0.8rem;'>— ÜRES —</span>"

    # Tört hordó színének meghatározása az alapsör alapján
    base_name = beer_name.replace(" (tört)", "").strip()
    color = data["szinek"].get(base_name, "#3498DB")

    return f"<span style='background-color: {color}; color: #ffffff; padding: 3px 8px; border-radius: 8px; font-weight: bold; font-size: 0.8rem; display: inline-block; white-space: nowrap;'>{beer_name}</span>"


st.title("🍺 Csaplista & Hordókövető")

col_k1, col_k2 = st.columns(2)
with col_k1:
    st.info(f"🧼 **Utolsó csapmosás:** {data.get('csapmosas', '—')}")
with col_k2:
    st.warning(f"💨 **Utolsó CO2 csere:** {data.get('co2_csere', '—')}")

tab_csapok, tab_kuka, tab_admin = st.tabs(
    ["🚰 Csapok", "🗑️ Üres Hordók", "⚙️ Menedzsment & Raktár"]
)

# 1. TAB: CSAPLISTA
with tab_csapok:
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
            
            div.stButton > button.btn-wash {
                background-color: #FF69B4 !important;
                color: white !important;
                border: none !important;
                font-weight: bold !important;
            }
            div.stButton > button.btn-co2 {
                background-color: #1E90FF !important;
                color: white !important;
                border: none !important;
                font-weight: bold !important;
            }
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
with tab_kuka:
    st.subheader("Futárra Váró Üres Hordók")

    # PONT 1 & 4: Elszállítás visszavonása gomb és Véglegesítés
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
        for beer_name, count in kuka_counts.items():
            # PONT 2: Visszaküldés raktárba gomb a bal oldalon
            k_col0, k_col1, k_col2, k_col3 = st.columns(
                [2, 3, 2, 2], vertical_alignment="center"
            )

            with k_col0:
                if st.button(
                    "↩️ Raktárba (tört)", key=f"return_wh_btn_{beer_name}"
                ):
                    data["kuka"].remove(beer_name)
                    # PONT 2: Tört jelölés hozzáadása
                    tort_name = (
                        beer_name
                        if "(tört)" in beer_name
                        else f"{beer_name} (tört)"
                    )
                    data["raktar"].append(tort_name)

                    # Szín beállítása ha új tétel lenne
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
                    # Előzmény elmentése a visszavonhatósághoz
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
with tab_admin:
    st.subheader("🧼 Karbantartási Műveletek")

    # PONT 3: CSAPMOSÁS ÉS CO2 CSERE EGY SORBAN
    m1, m2 = st.columns(2)

    with m1:
        if not st.session_state["confirm_wash"]:
            if st.button("🧼 csap mosása", key="btn_wash_act"):
                st.session_state["confirm_wash"] = True
                st.rerun()
        else:
            st.warning("❓ **Biztosan ma végezted el a csapmosást?**")
            wc1, wc2 = st.columns(2)
            with wc1:
                if st.button("✅ Igen, mentés", key="save_wash_btn"):
                    data["csapmosas"] = datetime.datetime.now().strftime(
                        "%Y-%m-%d"
                    )
                    save_data(data)
                    st.session_state["confirm_wash"] = False
                    st.success("Csapmosás dátuma frissítve!")
                    st.rerun()
            with wc2:
                if st.button("❌ Mégse", key="cancel_wash_btn"):
                    st.session_state["confirm_wash"] = False
                    st.rerun()

    with m2:
        if not st.session_state["confirm_co2"]:
            if st.button("💨 co lecserélése", key="btn_co2_act"):
                st.session_state["confirm_co2"] = True
                st.rerun()
        else:
            st.warning("❓ **Biztosan ma cserélted ki a CO2 palackot?**")
            cc1, cc2 = st.columns(2)
            with cc1:
                if st.button("✅ Igen, mentés", key="save_co2_btn"):
                    data["co2_csere"] = datetime.datetime.now().strftime(
                        "%Y-%m-%d"
                    )
                    save_data(data)
                    st.session_state["confirm_co2"] = False
                    st.success("CO2 csere dátuma frissítve!")
                    st.rerun()
            with cc2:
                if st.button("❌ Mégse", key="cancel_co2_btn"):
                    st.session_state["confirm_co2"] = False
                    st.rerun()

    st.markdown("---")

    # TELJES HORDÓ KIMUTATÁS
    st.subheader("📊 Teljes Hordó Készletnyilvántartás")

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

    st.caption(
        f"➕ **Kiegészítés (Üres hordók a kukában):** {ures_kuka} db üres hordó vár elszállításra."
    )

    st.markdown("---")
    st.subheader("📦 Raktárkészlet Kezelése")

    col_r1, col_r2 = st.columns([3, 2])

    with col_r1:
        st.markdown("**Raktárban lévő hordók kezelése és csaphoz rendelése:**")
        if data.get("raktar"):
            raktar_counts = Counter(data["raktar"])
            csap_options = [
                f"#{c['id']} ({c['jelenlegi'] if c['jelenlegi'] else 'ÜRES'})"
                for c in data["csapok"]
            ]

            for beer_name, count in raktar_counts.items():
                r_col1, r_col2, r_col3, r_col4 = st.columns(
                    [3, 3, 2, 2], vertical_alignment="center"
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

                with r_col4:
                    if st.button("🗑️ Törlés", key=f"wh_del_btn_{beer_name}"):
                        data["raktar"].remove(beer_name)
                        save_data(data)
                        st.warning(f"1 db '{beer_name}' törölve a raktárból!")
                        st.rerun()

                st.markdown(
                    "<hr style='margin: 4px 0; border-color: #333;'>",
                    unsafe_allow_html=True,
                )
        else:
            st.info("A raktár jelenleg üres.")

    # PONT 3: ÚJ / MEGLÉVŐ SÖR HOZZÁADÁS SZÉP GOMBOKKAL
    with col_r2:
        st.markdown("**Új hordó hozzáadása a raktárhoz:**")

        add_type = st.segmented_control(
            "Hozzáadás típusa:",
            ["Meglévő sörök közül", "Vadonatúj sör felvétele"],
            default="Meglévő sörök közül",
            key="add_type_segmented",
        )

        if add_type == "Meglévő sörök közül":
            # Tört szavak nélküli egyedi nevek kigyűjtése
            meglevo_sorok = sorted(
                list(
                    set(
                        k.replace(" (tört)", "")
                        for k in data["szinek"].keys()
                    )
                )
            )
            if meglevo_sorok:
                valasztott_meglevo = st.selectbox(
                    "Válassz sört:", meglevo_sorok, key="select_existing_beer"
                )
                db_szam = st.number_input(
                    "Darabszám:", min_value=1, value=1, key="num_existing_beer"
                )

                if st.button(
                    "➕ Hozzáadás a Raktárhoz",
                    type="primary",
                    key="add_exist_btn",
                ):
                    for _ in range(db_szam):
                        data["raktar"].append(valasztott_meglevo)
                    save_data(data)
                    st.success(
                        f"{db_szam} db '{valasztott_meglevo}' hozzáadva!"
                    )
                    st.rerun()
            else:
                st.info("Még nincs rögzített sör a rendszerben.")
        else:
            uj_sor_nev = st.text_input("Új sör neve:", key="input_raktar_name")
            valasztott_szin = st.color_picker(
                "Sör színe a táblázatban:", "#3498DB", key="color_picker"
            )
            db_szam_uj = st.number_input(
                "Darabszám:", min_value=1, value=1, key="num_new_beer"
            )

            if st.button(
                "➕ Új sör mentése és hozzáadása",
                type="primary",
                key="add_new_beer_btn",
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
