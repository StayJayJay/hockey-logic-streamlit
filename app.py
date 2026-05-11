import os
import streamlit as st

st.write("Working dir:", os.getcwd())
st.write("Files:", os.listdir("."))

st.set_page_config(
    page_title="Hockey Log.Dat",
    layout="centered"
)

st.title("Hockey Log.Dat")

if st.button("Predikce zápasu"):
    st.switch_page("pages/predikce.py")

if st.button("Historie & Excel"):
    st.switch_page("pages/historie.py")
