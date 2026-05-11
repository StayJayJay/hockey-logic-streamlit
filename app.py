import streamlit as st
from model import predict
from coefficients import REGULAR_SEASON

import pandas as pd
from datetime import datetime

if "matches" not in st.session_state:
    st.session_state.matches = []

st.set_page_config(page_title="Hockey Logic", layout="centered")

st.title("🏒 Hockey Logic – Match Predictor")

st.markdown("Zadej základní statistiky zápasu. Rozdíly se počítají automaticky.")

with st.form("match_form"):
    st.subheader("Zápas")

    home_team = st.checkbox("Domácí tým", value=True)

    col1, col2 = st.columns(2)

    with col1:
        shots_home = st.number_input("Střely na bránu – Home", min_value=0, step=1)
        pp_home = st.number_input("Přesilovky – Home", min_value=0, step=1)
        pp_goals_home = st.number_input("Využité PP – Home", min_value=0, step=1)
        goalie_home = st.number_input("Goalie rating – Home", value=0.50, step=0.01)

    with col2:
        shots_away = st.number_input("Střely na bránu – Away", min_value=0, step=1)
        pp_away = st.number_input("Přesilovky – Away", min_value=0, step=1)
        pp_goals_away = st.number_input("Využité PP – Away", min_value=0, step=1)
        goalie_away = st.number_input("Goalie rating – Away", value=0.50, step=0.01)

    submit = st.form_submit_button("Spočítat predikci")

if submit:
    shots_diff = shots_home - shots_away
    xg_diff = shots_diff * REGULAR_SEASON["scale_shots"]

    home_pp_eff = pp_goals_home / pp_home if pp_home > 0 else 0
    away_pp_eff = pp_goals_away / pp_away if pp_away > 0 else 0

    pp_diff = (home_pp_eff - away_pp_eff) * (pp_home + pp_away)
    pp_diff *= REGULAR_SEASON["scale_pp"]

    goalie_diff = goalie_home - goalie_away

    match = {
        "home": 1 if home_team else 0,
        "xg_diff": xg_diff,
        "pp_diff": pp_diff,
        "goalie_diff": goalie_diff,
    }

    log_odds, p_win = predict(match, REGULAR_SEASON)

    st.divider()
    st.subheader("📊 Výsledek")
    st.metric("Pravděpodobnost výhry", f"{p_win*100:.1f} %")
    st.write(f"**Log-Odds:** {log_odds:.3f}")

    if st.button("💾 Uložit zápas do historie"):
    st.session_state.matches.append({
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Mode": mode,
        "Home": home_team,
        "Shots Home": shots_home,
        "Shots Away": shots_away,
        "PP Home": pp_home,
        "PP Away": pp_away,
        "PP Goals Home": pp_goals_home,
        "PP Goals Away": pp_goals_away,
        "Goalie Diff": goalie_diff,
        "xG Diff": xg_diff,
        "PP Diff": pp_diff,
        "P(win)": round(p_win, 3),
        "Result": ""   # vyplníš později
    })
    st.success("Zápas uložen ✅")

st.divider()
st.subheader("📂 Historie zápasů")

if st.session_state.matches:
    df_history = pd.DataFrame(st.session_state.matches)
    st.data_editor(
        df_history,
        num_rows="dynamic",
        use_container_width=True,
        key="history_editor"
    )
    st.session_state.matches = df_history.to_dict("records")
else:
    st.info("Zatím nejsou uložené žádné zápasy.")

from io import BytesIO

if st.session_state.matches:
    buffer = BytesIO()
    export_df = pd.DataFrame(st.session_state.matches)
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        export_df.to_excel(writer, index=False, sheet_name="Matches")

    st.download_button(
        label="⬇️ Stáhnout Excel",
        data=buffer,
        file_name="hockey_logic_history.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )