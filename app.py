import streamlit as st

st.set_page_config(
    page_title="Hockey Log.Dat",
    layout="centered"
)

# ======================
# SIDEBAR NAVIGACE
# ======================

st.title("Hockey Log.Dat")

if st.button("📊 Predikce zápasu"):
    st.switch_page("pages/1_📊_Predikce_zapasu.py")

if st.button("📂 Historie & Excel"):
    st.switch_page("pages/2_📂_Historie_a_Excel.py")
