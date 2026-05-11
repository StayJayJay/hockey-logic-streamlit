import streamlit as st

st.set_page_config(
    page_title="Hockey Logic",
    layout="centered"
)

st.title("🏒 Hockey Logic")

st.markdown("""
Tato aplikace slouží k:
- 📊 predikci hokejových zápasů
- 📂 správě historie zápasů
- 📥 exportu a editaci dat v Excelu
""")

st.divider()

st.subheader("Navigace")

st.page_link(
    "pages/1_📊_Predikce_zapasu.py",
    label="➡️ Predikce zápasu",
    icon="📊"
)

st.page_link(
    "pages/2_📂_Historie_a_Excel.py",
    label="➡️ Historie & Excel",
    icon="📂"
)

st.info("Stránky můžeš přepínat také v menu vlevo ⬅️")