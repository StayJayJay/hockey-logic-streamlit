import streamlit as st
import pandas as pd
import math
from datetime import datetime
from io import BytesIO

# ===============================
# INIT SESSION STATE
# ===============================
if "page" not in st.session_state:
    st.session_state.page = "predikce"

if "matches" not in st.session_state:
    st.session_state.matches = []

if "last_match" not in st.session_state:
    st.session_state.last_match = None


# ===============================
# MODEL
# ===============================
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


# ===============================
# SIDEBAR NAVIGATION
# ===============================
st.sidebar.title("🏒 Hockey Dat.Cen")

if st.sidebar.button("Predikce zápasu"):
    st.session_state.page = "predikce"

if st.sidebar.button("Historie & Excel"):
    st.session_state.page = "historie"

st.sidebar.markdown("---")



# ===============================
# PAGE: PREDICTION
# ===============================
if st.session_state.page == "predikce":

    st.title("📊 Predikce zápasu")

    mode = st.radio(
        "Režim",
        ["Regular Season", "Play‑off"],
        horizontal=True
    )

    COEF = REGULAR_SEASON if mode == "Regular Season" else PLAYOFFS

    with st.form("match_form"):
        home_team = st.checkbox("Domácí tým", value=True)

        col1, col2 = st.columns(2)

        with col1:
            team_home = st.text_input("Team Home")
            shots_home = st.number_input("Střely Home", 0, step=1)
            pp_home = st.number_input("PP Home", 0, step=1)
            pp_goals_home = st.number_input("PP Góly Home", 0, step=1)
            goalie_home = st.number_input("Goalie Home", 0.0, 1.0, 0.50, step=0.01)

        with col2:
            team_away = st.text_input("Team Away")
            shots_away = st.number_input("Střely Away", 0, step=1)
            pp_away = st.number_input("PP Away", 0, step=1)
            pp_goals_away = st.number_input("PP Góly Away", 0, step=1)
            goalie_away = st.number_input("Goalie Away", 0.0, 1.0, 0.50, step=0.01)

        calculate = st.form_submit_button("📊 Spočítat predikci")

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

        st.metric("Pravděpodobnost výhry", f"{p_win*100:.1f} %")
        st.write(f"Log‑odds: `{log_odds:.3f}`")

        st.session_state.last_match = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Mode": mode,
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

    if st.session_state.last_match:
        if st.button("💾 Uložit zápas"):
            st.session_state.matches.append(st.session_state.last_match)
            st.session_state.last_match = None
            st.success("Zápas uložen ✅")


# ===============================
# PAGE: HISTORY + EXCEL
# ===============================
elif st.session_state.page == "historie":

    st.title("📂 Historie & Excel")

    if not st.session_state.matches:
        st.info("Zatím nejsou uložené žádné zápasy.")
    else:
        df = pd.DataFrame(st.session_state.matches)

        edited_df = st.data_editor(
            df,
            use_container_width=True,
            num_rows="dynamic"
        )

        st.session_state.matches = edited_df.to_dict("records")

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            edited_df.to_excel(writer, index=False, sheet_name="Matches")

        st.download_button(
            "⬇️ Stáhnout Excel",
            data=buffer,
            file_name="hockey_logic_history.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )