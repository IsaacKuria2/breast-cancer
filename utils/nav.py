import streamlit as st

def render_nav():
    st.sidebar.markdown("## 💗 Menu")
    st.sidebar.page_link("Home.py",                      label="🏠 Home")
    st.sidebar.page_link("pages/1_EDA.py",               label="🔍 EDA")
    st.sidebar.page_link("pages/2_Model_Performance.py", label="📊 Model Performance")
    st.sidebar.page_link("pages/3_Live_Prediction.py",   label="🧪 Live Prediction")
    st.sidebar.page_link("pages/4_Admin.py",             label="🔐 Admin")
    st.sidebar.markdown("---")