import streamlit as st
import pandas as pd
from io import BytesIO

st.title("📂 Historie & Excel")

if "matches" not in st.session_state or not st.session_state.matches:
    st.info("Zatím žádná data.")
else:
    df = pd.DataFrame(st.session_state.matches)

    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True
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