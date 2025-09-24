# app.py
import pandas as pd
import re
from collections import Counter
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# -------------------------
# STEP 1: Load data
# Replace with your actual CSV/Excel that has job descriptions
# Expected columns: ["Date", "Tools", "Problem", "Process"]
# Example: job_data.csv
# Date should be in format YYYY-MM-DD

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("job_data.csv")
    except FileNotFoundError:
        st.error("❌ Could not find job_data.csv. Please place it in the project folder.")
        return pd.DataFrame()
    
    # Ensure date column is datetime
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    return df

df = load_data()

if df.empty:
    st.stop()

# -------------------------
# STEP 2: Filter last month + limit to 1,000 rows
one_month_ago = datetime.now() - timedelta(days=30)
df_recent = df[df["Date"] >= one_month_ago].sort_values("Date", ascending=False).head(1000)

# -------------------------
# STEP 3: Frequency analysis
def explode_and_count(series, top_n=50):
    words = []
    for entry in series.dropna():
        for w in re.split(r"[,\s/&]+", str(entry)):
            if w and len(w) > 2:  # skip very short words
                words.append(w.lower())
    return pd.DataFrame(Counter(words).most_common(top_n), columns=["Keyword", "Count"])

tool_freq = explode_and_count(df_recent["Tools"])
problem_freq = explode_and_count(df_recent["Problem"])
process_freq = explode_and_count(df_recent["Process"])

# -------------------------
# STEP 4: Streamlit UI
st.title("📊 Job Description Keyword Analysis")
st.write(f"Analyzing the last **{len(df_recent)} job descriptions** from the past month.")

tab1, tab2, tab3 = st.tabs(["🔧 Tools", "⚠️ Problems", "⚙️ Processes"])

def render_tab(df_freq, title, xlabel):
    st.subheader(title)
    st.dataframe(df_freq)
    fig, ax = plt.subplots()
    ax.bar(df_freq["Keyword"], df_freq["Count"])
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

with tab1:
    render_tab(tool_freq, "Top Tools / Keywords", "Tools")

with tab2:
    render_tab(problem_freq, "Top Problem Keywords", "Problems")

with tab3:
    render_tab(process_freq, "Top Process Keywords", "Processes")
