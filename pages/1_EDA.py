import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from utils.data_loader import load_data
from utils.nav import render_nav
from utils.sidebar_comments import render_comment_sidebar

st.set_page_config(page_title="EDA", page_icon="resources/favicon.png", layout="wide")
st.title("🔍 Exploratory Data Analysis")

df = load_data()
df["diagnosis_label"] = df["diagnosis"].map({1: "Malignant", 0: "Benign"})

# --- Dataset Overview ---
st.subheader("Dataset Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Samples", len(df))
col2.metric("Malignant", int(df["diagnosis"].sum()))
col3.metric("Benign", int((df["diagnosis"] == 0).sum()))

with st.expander("Preview raw data"):
    st.dataframe(df.drop(columns=["diagnosis_label"]).head(10))

with st.expander("Summary statistics"):
    st.dataframe(df.drop(columns=["diagnosis_label"]).describe().T)

# --- Diagnosis Distribution ---
st.subheader("Diagnosis Distribution")
fig = px.pie(df, names="diagnosis_label", color="diagnosis_label",
             color_discrete_map={"Malignant": "#e74c3c", "Benign": "#2ecc71"},
             hole=0.4)
st.plotly_chart(fig, use_container_width=True)

# --- Feature Distribution ---
st.subheader("Feature Distribution by Diagnosis")
feature = st.selectbox("Select a feature", df.columns.drop(["diagnosis", "diagnosis_label"]))
fig2 = px.histogram(df, x=feature, color="diagnosis_label", barmode="overlay",
                    color_discrete_map={"Malignant": "#e74c3c", "Benign": "#2ecc71"},
                    nbins=40)
st.plotly_chart(fig2, use_container_width=True)

# --- Boxplot ---
st.subheader("Boxplot by Diagnosis")
fig3 = px.box(df, x="diagnosis_label", y=feature, color="diagnosis_label",
              color_discrete_map={"Malignant": "#e74c3c", "Benign": "#2ecc71"})
st.plotly_chart(fig3, use_container_width=True)

# --- Correlation Heatmap ---
st.subheader("Correlation Heatmap")
fig4, ax = plt.subplots(figsize=(14, 10))
sns.heatmap(df.drop(columns=["diagnosis_label"]).corr(), cmap="coolwarm", ax=ax,
            annot=False, linewidths=0.5)
st.pyplot(fig4)
render_nav()
render_comment_sidebar()