import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from utils.data_loader import load_data, get_features_and_target
from utils.nav import render_nav
from utils.sidebar_comments import render_comment_sidebar

st.set_page_config(page_title="EDA", page_icon="🎗️", layout="wide")
render_nav()

st.title("🔍 Exploratory Data Analysis")
st.markdown("""
> *Every feature in this dataset was measured from a real biopsy image.
Behind every row is a patient waiting for an answer. Understanding this data
is the first step toward giving them a better one.*
""")

st.markdown("---")

df = load_data()
df["diagnosis_label"] = df["diagnosis"].map({1: "Malignant", 0: "Benign"})

# --- Dataset Overview ---
st.subheader("📋 Dataset Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Samples", len(df))
col2.metric("Malignant", int(df["diagnosis"].sum()))
col3.metric("Benign", int((df["diagnosis"] == 0).sum()))

with st.expander("Preview raw data"):
    st.dataframe(df.drop(columns=["diagnosis_label"]).head(10))

with st.expander("Summary statistics"):
    st.dataframe(df.drop(columns=["diagnosis_label"]).describe().T)

st.markdown("---")

# --- Diagnosis Distribution ---
st.subheader("🎗️ Diagnosis Distribution")
st.markdown("Over **37%** of patients in this dataset were diagnosed with malignant tumours — a sobering reminder of how common this disease is.")

fig = px.pie(df, names="diagnosis_label", color="diagnosis_label",
             color_discrete_map={"Malignant": "#e74c3c", "Benign": "#2ecc71"},
             hole=0.4)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- Comparison Table ---
st.subheader("📊 Malignant vs Benign — Mean Feature Comparison")
st.markdown("Malignant tumours consistently show **larger, more irregular** cell nuclei across almost every feature.")

mean_comparison = df.groupby("diagnosis_label").mean(numeric_only=True).T
mean_comparison["Difference (M-B)"] = mean_comparison["Malignant"] - mean_comparison["Benign"]
mean_comparison["Difference (M-B)"] = mean_comparison["Difference (M-B)"].round(4)
mean_comparison = mean_comparison.round(4)
st.dataframe(mean_comparison.style.background_gradient(subset=["Difference (M-B)"], cmap="RdYlGn_r"),
             use_container_width=True)

st.markdown("---")

# --- Top 10 Most Predictive Features ---
st.subheader("🏆 Top 10 Most Predictive Features")
st.markdown("""
Not all features are equal. These are the **10 features that matter most**
when distinguishing a malignant tumour from a benign one —
the signals a machine learning model listens to most closely.
""")

X, y = get_features_and_target(df.drop(columns=["diagnosis_label"]))
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)

importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": rf.feature_importances_
}).sort_values("Importance", ascending=False).head(10)

fig_imp = px.bar(importance_df, x="Importance", y="Feature", orientation="h",
                 color="Importance", color_continuous_scale="Reds",
                 title="Top 10 Most Predictive Features")
fig_imp.update_layout(yaxis=dict(autorange="reversed"))
st.plotly_chart(fig_imp, use_container_width=True)

st.markdown("---")

# --- Feature Distribution ---
st.subheader("📈 Feature Distribution by Diagnosis")
st.markdown("Select any feature below to see how its values differ between malignant and benign cases.")

feature = st.selectbox("Select a feature", df.columns.drop(["diagnosis", "diagnosis_label"]))

col1, col2 = st.columns(2)
with col1:
    fig2 = px.histogram(df, x=feature, color="diagnosis_label", barmode="overlay",
                        color_discrete_map={"Malignant": "#e74c3c", "Benign": "#2ecc71"},
                        nbins=40, title=f"Distribution of {feature}")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    fig3 = px.box(df, x="diagnosis_label", y=feature, color="diagnosis_label",
                  color_discrete_map={"Malignant": "#e74c3c", "Benign": "#2ecc71"},
                  title=f"Boxplot of {feature}")
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# --- Correlation Heatmap ---
st.subheader("🔗 Correlation Heatmap")
st.markdown("""
Many features are highly correlated — for example, radius, perimeter, and area
all measure the size of the nucleus in different ways.
Understanding these relationships helps us build better, less redundant models.
""")

fig4, ax = plt.subplots(figsize=(14, 10))
sns.heatmap(df.drop(columns=["diagnosis_label"]).corr(), cmap="coolwarm", ax=ax,
            annot=False, linewidths=0.5)
st.pyplot(fig4)

st.markdown("---")
st.info("👈 Head to **Model Performance** in the sidebar to see how well our models learned from this data.")

render_comment_sidebar()
# --- Footer ---
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9rem;'>
    Machine Learning & Data Science by <a href='https://www.linkedin.com/in/kuriaspace' target='_blank'>Isaac Kuria</a><br>
    Dataset: Wisconsin Breast Cancer Dataset
</div>
""", unsafe_allow_html=True)