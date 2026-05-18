import streamlit as st

def render_nav():
    with st.sidebar:
        st.markdown("## 💗 Menu")
        st.page_link("Home.py",                      label="🏠 Home")
        st.page_link("pages/1_EDA.py",               label="🔍 EDA")
        st.page_link("pages/2_Model_Performance.py", label="📊 Model Performance")
        st.page_link("pages/3_Live_Prediction.py",   label="🧪 Live Prediction")
        st.page_link("pages/4_Admin.py",             label="🔐 Admin")
        st.markdown("---")