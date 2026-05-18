import streamlit as st
from utils.nav import render_nav 
from utils.sidebar_comments import render_comment_sidebar

st.set_page_config(
    page_title="Breast Cancer Early Detection",
    page_icon="💗",                    # Changed to emoji for reliability
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Hero Section ---
st.markdown("""
<div style='text-align: center; padding: 2rem 0'>
    <h1 style='font-size: 3rem;'>🔬 Breast Cancer Classification</h1>
    <p style='font-size: 1.3rem; color: gray;'>
        Can machine learning help detect cancer earlier and more accurately?
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Why This Matters ---
st.subheader("💡 Why This Project Matters")
st.markdown("""
Breast cancer is the **most commonly diagnosed cancer** among women worldwide.
Early and accurate detection is critical — when caught early, the 5-year survival rate is **over 99%**.
When detected late, that drops dramatically.

This dashboard applies **machine learning** to classify tumors as **Malignant** or **Benign**
based on measurable features of cell nuclei from a biopsy image — the same kind of data
a clinician would have access to.

> *The goal: show how ML can serve as a powerful second opinion in medical diagnosis.*
""")

st.markdown("---")

# --- Key Stats ---
st.subheader("📊 Dataset at a Glance")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Patients", "569")
col2.metric("Malignant Cases", "212", "37.3%")
col3.metric("Benign Cases", "357", "62.7%")
col4.metric("Features Analysed", "30")

st.markdown("---")

# --- What's Inside ---
st.subheader("🗺️ What You Can Explore")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🔍 EDA
    **Exploratory Data Analysis**
    - How are malignant vs benign tumors distributed?
    - Which features differ most between the two?
    - How correlated are the 30 features?

    👉 *Great starting point to understand the data.*
    """)

with col2:
    st.markdown("""
    ### 📊 Model Performance
    **Compare 3 ML Models**
    - Logistic Regression
    - K-Nearest Neighbors
    - Support Vector Machine

    See accuracy, confusion matrices, and ROC curves side by side.

    👉 *Find out which model performs best.*
    """)

with col3:
    st.markdown("""
    ### 🧪 Live Prediction
    **Try It Yourself**
    - Adjust 30 tumor feature sliders
    - Choose your model
    - Get an instant Malignant / Benign prediction with confidence score

    👉 *See the model in action in real time.*
    """)

st.markdown("---")

# --- How to Navigate ---
st.subheader("🧭 How to Navigate")
st.info("👈 Use the **sidebar on the left** to switch between EDA, Model Performance, and Live Prediction.")

st.markdown("---")

# --- Footer ---
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9rem;'>
    Built with ❤️ by <a href='https://www.linkedin.com/in/kuriaspace' target='_blank'>Isaac Kuria</a><br>
    Dataset: Wisconsin Breast Cancer Dataset (Kaggle)
</div>
""", unsafe_allow_html=True)
render_nav()
render_comment_sidebar()