import streamlit as st
import pandas as pd
import math
from datetime import datetime
from io import BytesIO

# =========================
# MODEL
# =========================

def logistic(x):
    return 1 / (1 + math.exp(-x))


REGULAR_SEASON = {
    "intercept": -1.008,
    "home": 1.481,
    "xg_diff": 0.104,
    "pp_diff": 3.74,
    "goalie": 3.67,
    "scale_shots": 0.05,
    "scale_pp": 0.15,
}

PLAYOFFS = {
    "intercept": -1.008,
    "home": 1.6291,
    "xg_diff": 0.0624,
    "pp_diff": 2.992,
    "goalie": 4.404,
    "scale_shots": 0.05,
    "scale_pp": 0.15,
}


# =========================
# SESSION STATE INIT
# =========================

if "matches" not in st.session_state:
    st.session_state.matches = []

if "last_match" not in st.session_state:
    st.session_state.last_match = None


# =========================
# UI
# =========================

st.set_page_config(page_title="Hockey Logic", layout="centered")
st.title("🏒 Hockey Logic – Match Predictor")

mode = st.radio(
    "Režim",
    ["Regular Season", "Play‑off"],
    horizontal=True
)

COEF = REGULAR_SEASON if mode == "Regular Season" else PLAYOFFS

with st.form("match_form"):
    st.subheader("Zadání zápasu")

    home_team = st.checkbox("Domácí tým", value=True)

    col1, col2 = st.columns(2)

    with col1:
        shots_home = st.number_input("Střely na bránu – Home", 0, step=1)
        pp_home = st.number_input("Přesilovky – Home", 0, step=1)
        pp_goals_home = st.number_input("Využité PP – Home", 0, step=1)
        goalie_home = st.number_input("Goalie rating – Home", 0.0, 1.0, 0.50, step=0.01)

    with col2:
        shots_away = st.number_input("Střely na bránu – Away", 0, step=1)
        pp_away = st.number_input("Přesilovky – Away", 0, step=1)
        pp_goals_away = st.number_input("Využité PP – Away", 0, step=1)
        goalie_away = st.number_input("Goalie rating – Away", 0.0, 1.0, 0.50, step=0.01)

    calculate = st.form_submit_button("📊 Spočítat predikci")


# =========================
# PREDICTION
# =========================

if calculate:
    shots_diff = shots_home - shots_away
    xg_diff = shots_diff * COEF["scale_shots"]

    home_pp_eff = pp_goals_home / pp_home if pp_home > 0 else 0
    away_pp_eff = pp_goals_away / pp_away if pp_away > 0 else 0

    pp_diff = (home_pp_eff - away_pp_eff) * (pp_home + pp_away)
    pp_diff *= COEF["scale_pp"]

    goalie_diff = goalie_home - goalie_away

    log_odds = (
        COEF["intercept"]
        + COEF["home"] * (1 if home_team else 0)
        + COEF["xg_diff"] * xg_diff
        + COEF["pp_diff"] * pp_diff
        + COEF["goalie"] * goalie_diff
    )

    p_win = logistic(log_odds)

    st.session_state.last_match = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Mode": mode,
        "Home": home_team,
        "Shots Home": shots_home,
        "Shots Away": shots_away,
        "PP Home": pp_home,
        "PP Away": pp_away,
        "PP Goals Home": pp_goals_home,
        "PP Goals Away": pp_goals_away,
        "xG Diff": round(xg_diff, 3),
        "PP Diff": round(pp_diff, 3),
        "Goalie Diff": round(goalie_diff, 3),
        "P(win)": round(p_win, 3),
        "Result": ""
    }

    st.success("Predikce spočítána ✅")
    st.metric("Pravděpodobnost výhry", f"{p_win*100:.1f} %")
    st.write(f"Log-Odds: `{log_odds:.3f}`")


# =========================
# SAVE MATCH
# =========================

if st.session_state.last_match:
    if st.button("💾 Uložit zápas do historie", key="save_match"):
        st.session_state.matches.append(st.session_state.last_match)
        st.session_state.last_match = None
        st.success("Zápas uložen ✅")


# =========================
# HISTORY
# =========================

st.divider()
st.subheader("📂 Historie zápasů")

if st.session_state.matches:
    df = pd.DataFrame(st.session_state.matches)

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key="history_editor"
    )

    st.session_state.matches = edited_df.to_dict("records")

    # EXPORT TO EXCEL
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        edited_df.to_excel(writer, index=False, sheet_name="Matches")

    st.download_button(
        "⬇️ Stáhnout Excel",
        data=buffer,
        file_name="hockey_logic_history.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("Zatím nejsou uložené žádné zápasy.")