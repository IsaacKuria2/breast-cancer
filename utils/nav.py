import streamlit as st

def render_nav():
    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.image("resources/favicon.png", width=150)
        st.markdown("<h3 style='text-align:center; color:#e75480;'>Breast Cancer Early Detection</h3>",
                    unsafe_allow_html=True)
        st.markdown("---")
        st.page_link("Home.py", label="🏠 Home")
        st.page_link("pages/1_EDA.py", label="🔍 EDA")
        st.page_link("pages/2_Model_Performance.py", label="📊 Model Performance")
        st.page_link("pages/3_Live_Prediction.py", label="🧪 Live Prediction")
        st.page_link("pages/4_Admin.py", label="🔐 Admin")
        st.markdown("---")
