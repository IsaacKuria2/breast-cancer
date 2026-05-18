import streamlit as st
import pickle
import numpy as np
import pandas as pd
from utils.data_loader import load_data, get_features_and_target
from utils.sidebar_comments import render_comment_sidebar

st.set_page_config(page_title="Live Prediction", page_icon="resources/favicon.png", layout="wide")
st.title("🧪 Live Prediction")
st.markdown("Adjust the feature sliders and click **Predict** to classify a tumor.")

# --- Load models & scaler ---
model_options = {
    "Logistic Regression": "models/logistic_regression.pkl",
    "KNN": "models/knn.pkl",
    "SVM": "models/svm.pkl",
}

with open("models/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

selected_model = st.sidebar.selectbox("Choose a model", list(model_options.keys()))
with open(model_options[selected_model], "rb") as f:
    model = pickle.load(f)

# --- Load feature ranges from data ---
df = load_data()
X, _ = get_features_and_target(df)
feature_names = X.columns.tolist()

# --- Sliders ---
st.subheader("Input Features")
cols = st.columns(3)
user_input = {}

for i, feature in enumerate(feature_names):
    col = cols[i % 3]
    min_val = float(X[feature].min())
    max_val = float(X[feature].max())
    mean_val = float(X[feature].mean())
    user_input[feature] = col.slider(
        feature, min_value=min_val, max_value=max_val, value=mean_val,
        format="%.4f"
    )

# --- Predict ---
st.markdown("---")
if st.button("🔍 Predict", use_container_width=True):
    input_array = np.array([list(user_input.values())])
    input_scaled = scaler.transform(input_array)
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0]

    st.markdown("### Result")
    if prediction == 1:
        st.error(f"🔴 **Malignant** — {probability[1]*100:.1f}% confidence")
    else:
        st.success(f"🟢 **Benign** — {probability[0]*100:.1f}% confidence")

    st.markdown("**Prediction Probabilities**")
    prob_df = pd.DataFrame({
        "Class": ["Benign", "Malignant"],
        "Probability": [round(probability[0], 4), round(probability[1], 4)]
    })
    st.dataframe(prob_df, use_container_width=True)
    render_comment_sidebar()