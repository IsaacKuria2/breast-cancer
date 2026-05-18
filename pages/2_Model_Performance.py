import streamlit as st
import pandas as pd
import pickle
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, roc_curve, auc
)
from utils.data_loader import load_data, get_features_and_target, split_and_scale
from utils.sidebar_comments import render_comment_sidebar

st.set_page_config(page_title="Model Performance", page_icon="💗", layout="wide")

st.title("📊 Model Performance Comparison")

# --- Load data & models ---
df = load_data()
X, y = get_features_and_target(df)
X_train, X_test, y_train, y_test, scaler = split_and_scale(X, y)

model_names = {
    "Logistic Regression": "models/logistic_regression.pkl",
    "KNN": "models/knn.pkl",
    "SVM": "models/svm.pkl",
}

models = {}
for name, path in model_names.items():
    with open(path, "rb") as f:
        models[name] = pickle.load(f)

# --- Accuracy Comparison ---
st.subheader("Accuracy Comparison")
results = []
for name, model in models.items():
    y_pred = model.predict(X_test)
    results.append({
        "Model": name,
        "Train Accuracy": round(model.score(X_train, y_train), 4),
        "Test Accuracy": round(accuracy_score(y_test, y_pred), 4),
    })

results_df = pd.DataFrame(results)
st.dataframe(results_df, use_container_width=True)

fig = px.bar(results_df.melt(id_vars="Model", var_name="Split", value_name="Accuracy"),
             x="Model", y="Accuracy", color="Split", barmode="group",
             color_discrete_sequence=["#3498db", "#2ecc71"], range_y=[0.9, 1.0])
st.plotly_chart(fig, use_container_width=True)

# --- Per-model deep dive ---
st.subheader("Per-Model Deep Dive")
selected = st.selectbox("Select a model", list(models.keys()))
model = models[selected]
y_pred = model.predict(X_test)

col1, col2 = st.columns(2)

# Confusion matrix
with col1:
    st.markdown("**Confusion Matrix**")
    cm = confusion_matrix(y_test, y_pred)
    fig_cm = px.imshow(cm, text_auto=True, color_continuous_scale="Blues",
                       labels=dict(x="Predicted", y="Actual"),
                       x=["Benign", "Malignant"], y=["Benign", "Malignant"])
    st.plotly_chart(fig_cm, use_container_width=True)

# Classification report
with col2:
    st.markdown("**Classification Report**")
    report = classification_report(y_test, y_pred, target_names=["Benign", "Malignant"], output_dict=True)
    report_df = pd.DataFrame(report).transpose().round(2)
    st.dataframe(report_df, use_container_width=True)

# ROC Curve
st.markdown("**ROC Curve**")
fig_roc = go.Figure()
for name, m in models.items():
    y_prob = m.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    fig_roc.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", name=f"{name} (AUC={roc_auc:.3f})"))

fig_roc.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines",
                              line=dict(dash="dash", color="gray"), name="Random"))
fig_roc.update_layout(xaxis_title="False Positive Rate", yaxis_title="True Positive Rate")
st.plotly_chart(fig_roc, use_container_width=True)

render_comment_sidebar()