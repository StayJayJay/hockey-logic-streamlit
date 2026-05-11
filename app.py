import streamlit as st

st.set_page_config(
    page_title="Hockey Log.Dat",
    layout="centered"
)

st.title("Hockey Log.Dat")

if st.button("Predikce zápasu"):
    st.switch_page("pages/Predikce_zapasu.py")

if st.button("Historie & Excel"):
    st.switch_page("pages/Historie_a_Excel.py")
