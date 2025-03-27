import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# Title and description
st.title("Fashion Trend Quadrant Explorer")
st.markdown("""
Explore keyword performance based on **Year-over-Year (YoY)** and **Three-Month** search trends.  
Use the slider to filter by average monthly search volume.
""")

# Load cleaned fashion trend data from Google Drive or local test
csv_url = "https://drive.google.com/uc?export=download&id=1fsa-86gDxqG9WKHDmYVOo4ESlyXgkn9o"
df = pd.read_csv(csv_url)

# Clean and convert values
def clean_percent(col):
    return pd.to_numeric(
        col.replace("∞", np.nan).str.replace('%', ''), 
        errors='coerce'
    )

df["YoY change"] = clean_percent(df["YoY change"])
df["Three month change"] = clean_percent(df["Three month change"])
df["Avg. monthly searches"] = pd.to_numeric(df["Avg. monthly searches"], errors='coerce')
df = df.dropna()

# Classify quadrant trend
def classify(row):
    x = row["YoY change"]
    y = row["Three month change"]
    if x > 0 and y > 0:
        return "Winners 💚"
    elif x < 0 and y < 0:
        return "Fading 🔻"
    elif x < 0 and y > 0:
        return "Seasonal Spikes 🔵"
    else:
        return "Long-term Growth 🟠"

df["Trend Type"] = df.apply(classify, axis=1)

# Add slider for filtering by search volume
min_vol = int(df["Avg. monthly searches"].min())
max_vol = int(df["Avg. monthly searches"].max())
vol_range = st.slider("Filter by Avg. Monthly Searches", min_vol, max_vol, (min_vol, max_vol), step=10)

# Filter data
filtered = df[
    (df["Avg. monthly searches"] >= vol_range[0]) & 
    (df["Avg. monthly searches"] <= vol_range[1])
]

# Plot quadrant chart
fig = px.scatter(
    filtered,
    x="YoY change",
    y="Three month change",
    size="Avg. monthly searches",
    color="Trend Type",
    text="Keyword",
    title="Search Volume Quadrant Chart",
    labels={
        "YoY change": "YoY % Change",
        "Three month change": "3-Month % Change"
    },
    height=600
)
fig.update_traces(textposition='top center', marker=dict(opacity=0.7, line=dict(width=1, color='DarkSlateGrey')))
fig.add_hline(y=0, line_dash="dash", line_color="gray")
fig.add_vline(x=0, line_dash="dash", line_color="gray")

st.plotly_chart(fig, use_container_width=True)
