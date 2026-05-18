import streamlit as st
from utils.nav import render_nav
from utils.sidebar_comments import render_comment_sidebar

st.set_page_config(
    page_title="Breast Cancer Early Detection",
    page_icon="💗",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_nav()

# --- Hero Section ---
st.markdown("""
<div style='text-align: center; padding: 2rem 0'>
    <h1 style='font-size: 3rem;'> Early Detection Saves Lives</h1>
    <p style='font-size: 1.3rem; color: gray;'>
        Behind every data point is a real person. This is my small contribution to changing that story.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Personal Story ---
st.subheader("💬 Why I Built This")
st.markdown("""
Cancer doesn't knock before it enters. It doesn't warn you. It doesn't wait.

But data gives us a chance — a window to act before it's too late.

I built this dashboard because I believe technology should serve people, not just impress them.
Every number in this dataset represents a real human being — someone's mother, sister, friend.
My goal was simple: take raw medical data and turn it into something meaningful.
Something that could, even in a small way, contribute to earlier and more accurate detection.

This is not just a machine learning project. It's a reminder of **why data science matters**.
""")

st.markdown("---")

# --- The Reality ---
st.subheader("🌍 The Reality of Breast Cancer")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Diagnosed every 9 mins 🇬🇧", "1 woman", "in the UK alone")
col2.metric("Daily deaths in the UK", "31 people", "every single day")
col3.metric("Survival rate if caught early", "99%", "vs 26% if caught late")
col4.metric("Lives saved by screening", "1,300+", "every year in the UK")

st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.85rem; margin-top: 0.5rem'>
    Statistics sourced from <a href='https://www.cancerresearchuk.org' target='_blank'>Cancer Research UK</a>
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

# --- About Me ---
st.subheader("👨‍💻 About the Developer")
st.markdown("""
Hi, I'm **Isaac Kuria** — a Data Scientist passionate about using machine learning
to solve real-world problems, especially in healthcare and social impact.

This project demonstrates end-to-end data science skills — from raw data cleaning
and exploratory analysis, to model training, evaluation, and deploying a
production-ready web application.

**What I bring:**
- 🧹 Data wrangling & preprocessing
- 📊 Exploratory data analysis & visualisation
- 🤖 Machine learning model development & evaluation
- 🚀 End-to-end deployment with Streamlit
- 🧪 Translating complex models into accessible tools

📫 Open to Data Science & ML opportunities — let's connect!
""")

col1, col2 = st.columns(2)
with col1:
    st.link_button("💼 Connect on LinkedIn", "https://www.linkedin.com/in/kuriaspace")

st.markdown("---")

# --- Disclaimer ---
st.error("""
⚠️ DISCLAIMER: This tool is built purely for educational and portfolio purposes.
It is NOT a medical device and should NEVER be used to diagnose, treat, or make
any medical decisions. If you have any health concerns, please consult a
qualified medical professional immediately. Early detection saves lives — please speak to your doctor.
""")

st.markdown("---")

# --- How to Navigate ---
st.subheader("🧭 How to Navigate")
st.info("👈 Use the **sidebar on the left** to switch between EDA, Model Performance, and Live Prediction.")

st.markdown("---")

# --- Footer ---
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9rem;'>
    Machine Learning & Data Science by <a href='https://www.linkedin.com/in/kuriaspace' target='_blank'>Isaac Kuria</a><br>
    Dataset: Wisconsin Breast Cancer Dataset
</div>
""", unsafe_allow_html=True)

render_comment_sidebar()