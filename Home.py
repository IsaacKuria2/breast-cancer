import streamlit as st
from streamlit_option_menu import option_menu
from utils.sidebar_comments import render_comment_sidebar

# MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Breast Cancer Early Detection",
    page_icon="💗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# OPTIONAL: hide Streamlit default UI (safe to keep)
st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
[data-testid="collapsedControl"] {
    display: none;
}
[data-testid="stHeader"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# SIDEBAR NAVIGATION
# ----------------------------
with st.sidebar:
    page = option_menu(
        menu_title="Navigation",
        options=["Home", "EDA", "Performance", "Prediction", "Admin"],
        icons=["house", "bar-chart", "graph-up", "activity", "gear"],
        default_index=0,
    )

    render_comment_sidebar()   # keeps comments in sidebar (clean placement)

# ----------------------------
# HOME PAGE
# ----------------------------
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
    Early and accurate detection is critical — when caught early, the 5-year survival rate is **over 99%**.
    When detected late, that drops dramatically.

    This dashboard applies **machine learning** to classify tumors as **Malignant** or **Benign**
    based on measurable features of cell nuclei from a biopsy image.

    > *The goal: show how ML can serve as a powerful second opinion in medical diagnosis.*
    """)

    st.markdown("---")

    st.subheader("📊 Dataset at a Glance")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Patients", "569")
    col2.metric("Malignant Cases", "212", "37.3%")
    col3.metric("Benign Cases", "357", "62.7%")
    col4.metric("Features Analysed", "30")

    st.markdown("---")

    st.subheader("🗺️ What You Can Explore")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 🔍 EDA
        - Distribution of tumor types
        - Feature relationships
        - Correlation analysis
        """)

    with col2:
        st.markdown("""
        ### 📊 Model Performance
        - Logistic Regression
        - KNN
        - SVM
        - Accuracy & ROC curves
        """)

    with col3:
        st.markdown("""
        ### 🧪 Live Prediction
        - 30 feature sliders
        - Model selection
        - Real-time prediction
        """)

    st.markdown("---")

    st.subheader("🧭 How to Navigate")
    st.info("Use the sidebar to switch between pages.")

    st.markdown("---")

    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.9rem;'>
        Built with ❤️ by <a href='https://www.linkedin.com/in/kuriaspace' target='_blank'>Isaac Kuria</a><br>
        Dataset: Wisconsin Breast Cancer Dataset (Kaggle)
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# EDA PAGE
# ----------------------------
elif page == "EDA":
    st.title("📊 Exploratory Data Analysis")
    st.write("EDA content goes here")

# ----------------------------
# PERFORMANCE PAGE
# ----------------------------
elif page == "Performance":
    st.title("📈 Model Performance")
    st.write("Model comparison results go here")

# ----------------------------
# PREDICTION PAGE
# ----------------------------
elif page == "Prediction":
    st.title("🧪 Live Prediction")
    st.write("Prediction UI goes here")

# ----------------------------
# ADMIN PAGE
# ----------------------------
elif page == "Admin":
    st.title("⚙️ Admin Panel")
    st.write("Admin tools go here")