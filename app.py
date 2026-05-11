import streamlit as st

st.set_page_config(
    page_title="Hockey Logic",
    layout="centered"
)

# ======================
# SIDEBAR NAVIGACE
# ======================

st.title("🏒 Hockey Logic")

if st.button("📊 Predikce zápasu"):
    st.switch_page("pages/1_📊_Predikce_zapasu.py")

if st.button("📂 Historie & Excel"):
    st.switch_page("pages/2_📂_Historie_a_Excel.py")

# ======================
# HLAVNÍ STRÁNKA
# ======================
st.title("🏒 Hockey Logic")

st.markdown("""
Tato aplikace slouží k:

✅ predikci hokejových zápasů  
✅ ukládání historie  
✅ zadávání výsledků po zápase  
✅ exportu do Excelu  

---

👈 **Přejdi na jednotlivé stránky pomocí menu vlevo**
""")

st.success("Aplikace je správně nastavena ✅")
