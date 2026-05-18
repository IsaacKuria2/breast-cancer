import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from utils.data_loader import load_data, get_features_and_target
from utils.nav import render_nav
from utils.sidebar_comments import render_comment_sidebar

st.set_page_config(page_title="Live Prediction", page_icon="🎗️", layout="wide")
render_nav()

st.title("🧪 Live Prediction")
st.markdown("""
> *This is where the data comes to life. Adjust the feature values below
and let the model make a prediction — the same way it would on a real biopsy sample.*
""")

st.markdown("---")

# --- Context ---
st.subheader("💡 How This Works")
col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Step 1 — Choose a Model**\nSelect which ML model you want to use from the sidebar.")
with col2:
    st.info("**Step 2 — Set Feature Values**\nAdjust the 30 sliders to match the cell nucleus measurements.")
with col3:
    st.info("**Step 3 — Get a Prediction**\nClick Predict and see the result with a confidence score.")

st.markdown("---")

# --- Load models & scaler ---
model_options = {
    "Logistic Regression": "models/logistic_regression.pkl",
    "KNN": "models/knn.pkl",
    "SVM": "models/svm.pkl",
}

with open("models/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

selected_model = st.sidebar.selectbox("🤖 Choose a model", list(model_options.keys()))
with open(model_options[selected_model], "rb") as f:
    model = pickle.load(f)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Selected:** `{selected_model}`")
st.sidebar.markdown("""
**Model Accuracies:**
- Logistic Regression: 96.49%
- KNN: 95.61%
- SVM: 96.49%
""")

# --- Load feature ranges ---
df = load_data()
X, _ = get_features_and_target(df)
feature_names = X.columns.tolist()

# --- Feature groups ---
mean_features = [f for f in feature_names if "_mean" in f]
se_features = [f for f in feature_names if "_se" in f]
worst_features = [f for f in feature_names if "_worst" in f]

st.subheader("🎛️ Input Features")
st.markdown("Features are grouped into **Mean**, **Standard Error**, and **Worst** measurements.")

user_input = {}

tab1, tab2, tab3 = st.tabs(["📊 Mean Values", "📉 Standard Error", "⚠️ Worst Values"])

with tab1:
    st.markdown("*Average measurements across all cells in the sample.*")
    cols = st.columns(3)
    for i, feature in enumerate(mean_features):
        col = cols[i % 3]
        min_val = float(X[feature].min())
        max_val = float(X[feature].max())
        mean_val = float(X[feature].mean())
        user_input[feature] = col.slider(feature, min_value=min_val,
                                          max_value=max_val, value=mean_val, format="%.4f")

with tab2:
    st.markdown("*How much the measurements vary across cells — higher SE suggests irregularity.*")
    cols = st.columns(3)
    for i, feature in enumerate(se_features):
        col = cols[i % 3]
        min_val = float(X[feature].min())
        max_val = float(X[feature].max())
        mean_val = float(X[feature].mean())
        user_input[feature] = col.slider(feature, min_value=min_val,
                                          max_value=max_val, value=mean_val, format="%.4f")

with tab3:
    st.markdown("*The largest/most abnormal values recorded — often the strongest predictors of malignancy.*")
    cols = st.columns(3)
    for i, feature in enumerate(worst_features):
        col = cols[i % 3]
        min_val = float(X[feature].min())
        max_val = float(X[feature].max())
        mean_val = float(X[feature].mean())
        user_input[feature] = col.slider(feature, min_value=min_val,
                                          max_value=max_val, value=mean_val, format="%.4f")

st.markdown("---")

# --- Predict ---
if st.button("🔍 Run Prediction", use_container_width=True):
    input_array = np.array([list(user_input.values())])
    input_scaled = scaler.transform(input_array)
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0]

    st.markdown("---")
    st.subheader("🎯 Prediction Result")

    col1, col2 = st.columns(2)

    with col1:
        if prediction == 1:
            st.error(f"""
            ### 🔴 Malignant
            **Confidence: {probability[1]*100:.1f}%**

            The model predicts this tumour is **malignant**.
            This means the cell nucleus features are consistent
            with cancerous tissue patterns in the training data.
            """)
        else:
            st.success(f"""
            ### 🟢 Benign
            **Confidence: {probability[0]*100:.1f}%**

            The model predicts this tumour is **benign**.
            This means the cell nucleus features are consistent
            with non-cancerous tissue patterns in the training data.
            """)

    with col2:
        # Gauge chart
        confidence = probability[1] * 100 if prediction == 1 else probability[0] * 100
        color = "#e74c3c" if prediction == 1 else "#2ecc71"

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=confidence,
            title={"text": "Confidence Score (%)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, 50], "color": "#f8f9fa"},
                    {"range": [50, 75], "color": "#ffeeba"},
                    {"range": [75, 100], "color": "#d4edda"},
                ],
            }
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Probability bar chart
    st.markdown("**Prediction Probabilities**")
    fig_prob = go.Figure(go.Bar(
        x=["Benign", "Malignant"],
        y=[round(probability[0] * 100, 2), round(probability[1] * 100, 2)],
        marker_color=["#2ecc71", "#e74c3c"],
        text=[f"{probability[0]*100:.1f}%", f"{probability[1]*100:.1f}%"],
        textposition="auto"
    ))
    fig_prob.update_layout(yaxis_title="Probability (%)", yaxis_range=[0, 100])
    st.plotly_chart(fig_prob, use_container_width=True)

    st.markdown("---")
    st.warning("""
    ⚠️ **Disclaimer:** This prediction is generated by a machine learning model
    trained on historical data for **educational purposes only**.
    It is NOT a medical diagnosis. Please consult a qualified healthcare
    professional for any medical concerns.
    """)

render_comment_sidebar()

# --- Footer ---
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9rem;'>
    Machine Learning & Data Science by <a href='https://www.linkedin.com/in/kuriaspace' target='_blank'>Isaac Kuria</a><br>
    Dataset: Wisconsin Breast Cancer Dataset
</div>
""", unsafe_allow_html=True)