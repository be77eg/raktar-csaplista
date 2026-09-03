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
        "raktar": [
            "Fake Your Pils",
            "Grain Cosmos",
            "Dark Vanilla Sky",
            "Let's Jump",
        ],
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
if "pending_swap" not in st.session_state:
    st.session_state.pending_swap = None

st.title("🍺 Csaplista & Hordókövető")

# Karbantartás infó
col_k1, col_k2 = st.columns(2)
with col_k1:
    st.info(f"🧼 **Utolsó csapmosás:** {data.get('csapmosas', '—')}")
with col_k2:
    st.warning(f"💨 **Utolsó CO2 csere:** {data.get('co2_csere', '—')}")

# Visszavonás lehetőség az utolsó műveletre
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

# 1. FIX CSAPLISTA
with tab_csapok:
    st.subheader("Aktív Csapok Állapota")

    # Fejléc
    h_col1, h_col2, h_col3, h_col4, h_col5 = st.columns([1, 3, 2, 4, 2])
    with h_col1:
        st.markdown("**Csap**")
    with h_col2:
        st.markdown("**Jelenlegi sör**")
    with h_col3:
        st.markdown("**Csere dátuma**")
    with h_col4:
        st.markdown("**Következő hordók**")
    with h_col5:
        st.markdown("**Művelet**")

    st.markdown(
        "<hr style='margin: 4px 0 12px 0; border-color: #444;'>",
        unsafe_allow_html=True,
    )

    # Csapok kirajzolása sorról sorra
    for idx, c in enumerate(data["csapok"]):
        bg_color = (
            "rgba(255, 255, 255, 0.04)"
            if idx % 2 == 0
            else "rgba(255, 255, 255, 0.00)"
        )

        with st.container():
            st.markdown(
                f"<div style='background-color: {bg_color}; padding: 6px 8px; border-radius: 4px;'>",
                unsafe_allow_html=True,
            )
            col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 4, 2])

            with col1:
                st.markdown(f"### **#{c['id']}**")

            with col2:
                jelenlegi_nev = (
                    f"**{c['jelenlegi']}**" if c["jelenlegi"] else "❌ *ÜRES*"
                )
                st.markdown(jelenlegi_nev)

            with col3:
                st.markdown(f"📅 {c['datum']}")

            with col4:
                if c["kovetkezo"]:
                    st.markdown(" ➜ ".join(c["kovetkezo"]))
                else:
                    st.caption("Nincs következő hordó")

            with col5:
                # Ha épp erre a csapra nyomtak cserét, kérjen megerősítést
                if st.session_state.pending_swap == c["id"]:
                    st.warning("Biztos?")
                    b_ok, b_no = st.columns(2)
                    with b_ok:
                        if st.button("✅", key=f"confirm_{c['id']}"):
                            # Mentés történetbe
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

                            # Csere logika
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
                            st.session_state.pending_swap = None
                            st.rerun()

                    with b_no:
                        if st.button("❌", key=f"cancel_{c['id']}"):
                            st.session_state.pending_swap = None
                            st.rerun()
                else:
                    if st.button("🔄 Csere", key=f"btn_swap_{c['id']}"):
                        st.session_state.pending_swap = c["id"]
                        st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown(
                "<hr style='margin: 4px 0; border-color: #222;'>",
                unsafe_allow_html=True,
            )

# 2. KUKA / ÜRES HORDÓK
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

# 3. MENEDZSMENT & RAKTÁR
with tab_admin:
    st.subheader("📦 Raktár (Szabad Hordók)")
    st.caption("Itt találhatóak azok a hordók, amelyek még nincsenek csapra/várakozási sorba állítva.")

    col_r1, col_r2 = st.columns([2, 1])

    with col_r1:
        if data.get("raktar"):
            raktar_df = (
                pd.DataFrame(data["raktar"], columns=["Sör neve"])
                .value_counts()
                .reset_index(name="Készlet (db)")
            )
            st.dataframe(raktar_df, use_container_width=True, hide_index=True)
        else:
            st.info("A raktár jelenleg üres.")

    with col_r2:
        st.markdown("**Új hordó érkezett a raktárba:**")
        uj_raktar_sor = st.text_input("Sör neve:", key="input_raktar")
        if st.button("➕ Raktárba tesz"):
            if uj_raktar_sor.strip():
                data["raktar"].append(uj_raktar_sor.strip())
                save_data(data)
                st.success("Hordó hozzáadva a raktárhoz!")
                st.rerun()

    st.markdown("---")
    st.subheader("➕ Várakozó Hordó Beállítása Csapra")

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        target_csap = st.selectbox(
            "Melyik csaphoz adjuk hozzá?",
            [f"#{c['id']} — {c['jelenlegi']}" for c in data["csapok"]],
        )
        c_id = int(target_csap.split(" ")[0].replace("#", ""))

    with col_m2:
        # Választhat raktárból vagy írhat újat
        raktar_opciok = list(set(data.get("raktar", [])))
        valasztas = st.selectbox(
            "Válassz hordót a Raktárból vagy adj meg újat:",
            ["-- Raktárból választok --"]
            + raktar_opciok
            + ["➕ Új sör kézi megadása"],
        )

        if valasztas == "➕ Új sör kézi megadása":
            hozzaadando_sor = st.text_input("Új sör neve:")
            levon_raktarbol = False
        elif valasztas != "-- Raktárból választok --":
            hozzaadando_sor = valasztas
            levon_raktarbol = True
        else:
            hozzaadando_sor = ""
            levon_raktarbol = False

    if st.button("Hordó hozzáadása a csap sorához", type="primary"):
        if hozzaadando_sor.strip():
            target_c = next(c for c in data["csapok"] if c["id"] == c_id)
            target_c["kovetkezo"].append(hozzaadando_sor.strip())

            # Ha raktárból választottuk, kivesszük belőle az egyiket
            if levon_raktarbol and hozzaadando_sor in data["raktar"]:
                data["raktar"].remove(hozzaadando_sor)

            save_data(data)
            st.success(f"Hozzáadva a #{c_id} csaphoz!")
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
