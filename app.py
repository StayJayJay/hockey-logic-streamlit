import streamlit as st

st.set_page_config(
    page_title="Hockey Logic",
    layout="centered"
)

# ======================
# SIDEBAR NAVIGACE
# ======================
st.sidebar.title("🏒 Hockey Logic")
st.sidebar.markdown("### Navigace")

st.sidebar.markdown(
    """
- 📊 **Predikce zápasu**  
- 📂 **Historie & Excel**
"""
)

st.sidebar.info(
    "Stránky přepínáš kliknutím na jejich název výše ⬆️"
)

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
