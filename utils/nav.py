import streamlit as st

PAGES = {
    "🏠 Home": "Home.py",
    "🔍 EDA": "pages/1_EDA.py",
    "📊 Model Performance": "pages/2_Model_Performance.py",
    "🧪 Live Prediction": "pages/3_Live_Prediction.py",
    "🔐 Admin": "pages/4_Admin.py",
}

def render_nav():
    st.sidebar.markdown("## Breast Cancer Early Detection")
    selection = st.sidebar.selectbox("", list(PAGES.keys()))
    st.sidebar.markdown("---")