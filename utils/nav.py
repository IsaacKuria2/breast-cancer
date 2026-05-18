import streamlit as st

PAGES = {
    "🏠 Home": "Home.py",
    "🔍 EDA": "1_EDA.py",
    "📊 Model Performance": "2_Model_Performance.py",
    "🧪 Live Prediction": "3_Live_Prediction.py",
    "🔐 Admin": "4_Admin.py",
}

def render_nav():
    st.sidebar.markdown("## 💗 Dashboard")
    for label, path in PAGES.items():
        if st.sidebar.button(label, use_container_width=True, key=f"nav_{label}"):
            st.session_state["_navigate_to"] = path
    st.sidebar.markdown("---")

def handle_navigation():
    if "_navigate_to" in st.session_state:
        path = st.session_state.pop("_navigate_to")
        st.switch_page(path)