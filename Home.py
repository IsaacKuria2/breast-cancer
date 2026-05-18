import streamlit as st
from streamlit_option_menu import option_menu
from utils.sidebar_comments import render_comment_sidebar

# MUST BE FIRST
st.set_page_config(
    page_title="Breast Cancer Early Detection",
    page_icon="💗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- SIDEBAR MENU ----------------
with st.sidebar:
    page = option_menu(
        menu_title="Navigation",
        options=["Home", "EDA", "Performance", "Prediction", "Admin"],
        icons=["house", "bar-chart", "graph-up", "activity", "gear"],
        default_index=0
    )

    render_comment_sidebar()

# ---------------- HOME PAGE ----------------
if page == "Home":

    st.markdown("""
    <div style='text-align: center; padding: 2rem 0'>
        <h1 style='font-size: 3rem;'>🔬 Breast Cancer Classification</h1>
        <p style='font-size: 1.3rem; color: gray;'>
            Can machine learning help detect cancer earlier and more accurately?
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("💡 Why This Project Matters")
    st.markdown("""
    Breast cancer is the **most commonly diagnosed cancer** among women worldwide.
    Early detection saves lives.
    """)

    st.markdown("---")

    st.subheader("📊 Dataset at a Glance")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Patients", "569")
    col2.metric("Malignant Cases", "212", "37.3%")
    col3.metric("Benign Cases", "357", "62.7%")
    col4.metric("Features Analysed", "30")

    st.markdown("---")

    st.info("Use the sidebar to navigate between pages 👈")

# ---------------- EDA ----------------
elif page == "EDA":
    st.title("📊 Exploratory Data Analysis")
    st.write("EDA content goes here")

# ---------------- PERFORMANCE ----------------
elif page == "Performance":
    st.title("📈 Model Performance")
    st.write("Model comparison goes here")

# ---------------- PREDICTION ----------------
elif page == "Prediction":
    st.title("🧪 Live Prediction")
    st.write("Prediction UI goes here")

# ---------------- ADMIN ----------------
elif page == "Admin":
    st.title("⚙️ Admin Panel")
    st.write("Admin tools go here")