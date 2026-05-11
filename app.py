import streamlit as st
from model import predict
from coefficients import REGULAR_SEASON

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
    
