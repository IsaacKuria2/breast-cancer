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
from utils.nav import render_nav
from utils.sidebar_comments import render_comment_sidebar

st.set_page_config(page_title="Model Performance", page_icon="🎗️", layout="wide")
render_nav()

st.title("📊 Model Performance Comparison")
st.markdown("""
> *In medicine, a wrong prediction isn't just a statistic, it's a missed diagnosis (Have you heard of 'Pam' sweets?).
This page shows how well our models perform, and more importantly,
how much we can trust them with something this important.*
""")

st.markdown("---")

# --- Why This Matters ---
st.subheader("💡 Why Model Performance Matters in Healthcare")
st.markdown("""
In most machine learning tasks, accuracy is the main goal.
But in healthcare, **the cost of being wrong is not equal on both sides.**

- A **False Negative** — telling a patient they are cancer-free when they are not could cost them their life.
- A **False Positive** — flagging a healthy patient as at risk causes unnecessary stress and further testing.

This is why we look beyond accuracy and examine **precision, recall, and AUC**
to understand the full picture of how trustworthy a model really is.
""")

st.markdown("---")

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
st.subheader("🏆 Accuracy Comparison")
st.markdown("How often does each model get the right answer overall?")

results = []
for name, model in models.items():
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, target_names=["Benign", "Malignant"], output_dict=True)
    results.append({
        "Model": name,
        "Train Accuracy": round(model.score(X_train, y_train), 4),
        "Test Accuracy": round(accuracy_score(y_test, y_pred), 4),
        "Recall (Malignant)": round(report["Malignant"]["recall"], 4),
        "Precision (Malignant)": round(report["Malignant"]["precision"], 4),
        "F1 Score (Malignant)": round(report["Malignant"]["f1-score"], 4),
    })

results_df = pd.DataFrame(results)
st.dataframe(results_df, use_container_width=True)

fig = px.bar(results_df.melt(id_vars="Model", var_name="Metric", value_name="Score"),
             x="Model", y="Score", color="Metric", barmode="group",
             color_discrete_sequence=["#3498db", "#2ecc71", "#e74c3c", "#f39c12", "#9b59b6"],
             range_y=[0.85, 1.0])
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- Plain English Metrics Explanation ---
st.subheader("📖 What Do These Metrics Mean?")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("""
    **Accuracy**
    Out of all predictions, how many were correct?
    *e.g. 96% means 96 out of 100 patients were correctly classified.*
    """)
with col2:
    st.warning("""
    **Recall (Sensitivity)**
    Of all actual malignant cases, how many did we catch?
    *High recall = fewer missed cancers. Critical in healthcare.*
    """)
with col3:
    st.success("""
    **Precision**
    Of all cases flagged as malignant, how many actually were?
    *High precision = fewer false alarms.*
    """)
with col4:
    st.error("""
    **F1 Score**
    The balance between precision and recall.
    *The best single number to judge a model in medical context.*
    """)

st.markdown("---")

# --- Precision vs Recall Medical Context ---
st.subheader("⚖️ Precision vs Recall — The Medical Trade-off")
st.markdown("""
In breast cancer detection, **recall is more important than precision.**

Here's why: if our model misses a malignant tumour (low recall),
that patient may not receive treatment in time.
If our model incorrectly flags a benign tumour (low precision),
the patient undergoes further testing stressful, but not fatal.

> *A model that catches every cancer case, even at the cost of some false alarms,
is more valuable in a clinical setting than one that is overly cautious.*

This is why we pay close attention to **Recall (Malignant)** above all other metrics.
""")

st.markdown("---")

# --- Per-model deep dive ---
st.subheader("🔬 Per-Model Deep Dive")
selected = st.selectbox("Select a model to inspect", list(models.keys()))
model = models[selected]
y_pred = model.predict(X_test)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Confusion Matrix**")
    st.markdown("*Rows = Actual diagnosis. Columns = Model prediction.*")
    cm = confusion_matrix(y_test, y_pred)
    fig_cm = px.imshow(cm, text_auto=True, color_continuous_scale="Blues",
                       labels=dict(x="Predicted", y="Actual"),
                       x=["Benign", "Malignant"], y=["Benign", "Malignant"])
    st.plotly_chart(fig_cm, use_container_width=True)

with col2:
    st.markdown("**Classification Report**")
    st.markdown("*Precision, Recall and F1 Score broken down by class.*")
    report = classification_report(y_test, y_pred, target_names=["Benign", "Malignant"], output_dict=True)
    report_df = pd.DataFrame(report).transpose().round(2)
    st.dataframe(report_df, use_container_width=True)

st.markdown("---")

# --- ROC Curve ---
st.subheader("📈 ROC Curve")
st.markdown("""
The ROC curve shows how well each model separates malignant from benign cases.
**AUC (Area Under Curve)** closer to 1.0 means the model is excellent at distinguishing between the two.
A value of 0.5 would mean the model is no better than a random guess.
""")

fig_roc = go.Figure()
for name, m in models.items():
    y_prob = m.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    fig_roc.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines",
                                  name=f"{name} (AUC={roc_auc:.3f})"))

fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines",
                              line=dict(dash="dash", color="gray"), name="Random Guess"))
fig_roc.update_layout(xaxis_title="False Positive Rate",
                       yaxis_title="True Positive Rate (Recall)")
st.plotly_chart(fig_roc, use_container_width=True)

st.markdown("---")

# --- Best Model Recommendation ---
st.subheader("🥇 Best Model Recommendation")

best_idx = results_df["Recall (Malignant)"].idxmax()
best_model = results_df.loc[best_idx, "Model"]
best_recall = results_df.loc[best_idx, "Recall (Malignant)"]
best_accuracy = results_df.loc[best_idx, "Test Accuracy"]

st.success(f"""
**Recommended Model: {best_model}**

Based on our evaluation, **{best_model}** achieves the highest recall for malignant cases
({best_recall * 100:.1f}%) with a test accuracy of {best_accuracy * 100:.1f}%.

In a clinical context, this means it is the best at catching actual cancer cases —
which is the most critical measure for a tool like this.
""")

st.markdown("""
> ⚠️ *Remember: this tool is for educational purposes only and should never replace
a qualified medical professional's diagnosis.*
""")

st.markdown("---")
st.info("👈 Head to **Live Prediction** in the sidebar to try the model yourself.")

render_comment_sidebar()