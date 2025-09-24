# app.py
import pandas as pd
import re
from collections import Counter
import streamlit as st
import matplotlib.pyplot as plt

# -------------------------
# STEP 1: Load data
# Replace this with your parsed PDF → CSV/Excel if needed
# For now, using a sample dataset based on your PDF table

data = [
    ["Tableau, SQL", "High shipping & ops costs without visibility", "Cost reduction dashboards for shipping & ops", "Find root causes of cost overruns", "Multi-dashboard analysis", "$120K/year savings"],
    ["Python, Excel", "Low marketing ROI with unclear A/B test results", "A/B testing for marketing success", "Measure if changes improve conversion", "Statistical significance testing", "ROI up 15%"],
    ["Python, Tableau", "High employee turnover", "HR attrition analysis", "Predict risk of leaving", "Turnover dashboards", "Predicted 80% high-risk"],
    ["Python, SAS", "Rising churn rates", "Customer churn modeling", "Identify churn drivers", "Logistic regression", "Reduced churn 10%"],
    ["SAS Forecast Studio", "Frequent ATM outages", "ATM replenishment forecasting", "Forecast demand spikes", "Time series modeling", "Outages down 95%"],
    ["Python, SQL", "Manual data prep", "ETL automation", "Centralized analytics", "Automated ingestion", "Reduced prep 90%"],
]

df = pd.DataFrame(data, columns=["Tools", "Problem", "Process", "Aim", "Solution", "Impact"])


# -------------------------
# STEP 2: Frequency analysis function
def explode_and_count(series):
    words = []
    for entry in series.dropna():
        for w in re.split(r"[,\s/&]+", str(entry)):
            if w and len(w) > 2:  # skip very short words
                words.append(w.lower())
    return Counter(words)


tool_counts = explode_and_count(df["Tools"])
problem_counts = explode_and_count(df["Problem"])
process_counts = explode_and_count(df["Process"])


# -------------------------
# STEP 3: Convert to DataFrames
tool_freq = pd.DataFrame(tool_counts.most_common(), columns=["Tool/Keyword", "Count"])
problem_freq = pd.DataFrame(problem_counts.most_common(), columns=["Problem Keyword", "Count"])
process_freq = pd.DataFrame(process_counts.most_common(), columns=["Process Keyword", "Count"])


# -------------------------
# STEP 4: Streamlit UI
st.title("📊 High Frequency Project Data Analysis")
st.write("This app extracts high-frequency **tools, problems, and processes** from project records.")

# Tabs for organization
tab1, tab2, tab3 = st.tabs(["🔧 Tools", "⚠️ Problems", "⚙️ Processes"])

with tab1:
    st.subheader("Top Tools / Keywords")
    st.dataframe(tool_freq)
    fig, ax = plt.subplots()
    ax.bar(tool_freq["Tool/Keyword"][:10], tool_freq["Count"][:10])
    ax.set_title("Top 10 Tools")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

with tab2:
    st.subheader("Top Problem Keywords")
    st.dataframe(problem_freq)
    fig, ax = plt.subplots()
    ax.bar(problem_freq["Problem Keyword"][:10], problem_freq["Count"][:10])
    ax.set_title("Top 10 Problems")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

with tab3:
    st.subheader("Top Process Keywords")
    st.dataframe(process_freq)
    fig, ax = plt.subplots()
    ax.bar(process_freq["Process Keyword"][:10], process_freq["Count"][:10])
    ax.set_title("Top 10 Processes")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
