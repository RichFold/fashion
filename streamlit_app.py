import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# Set Streamlit title and description
st.title("Fashion Trend Quadrant Explorer")
st.markdown("""
Explore keyword performance based on **Year-over-Year (YoY)** and **Three-Month** search trends.  
Use the slider to filter based on average monthly search volume.
""")

# Load data from your public Google Drive CSV
csv_url = "https://drive.google.com/uc?export=download&id=1fsa-86gDxqG9WKHDmYVOo4ESlyXgkn9o"
df = pd.read_csv(csv_url)

# Rename and clean columns
rename_mapping = {
    "Keyword": "Keyword",
    "YoY change": "YoY Change",
    "Three month change": "Three Month Change",
    "Avg. monthly searches": "Avg. Monthly Searches"
}
df.rename(columns=rename_mapping, inplace=True)

# Convert values to numeric and clean
df["YoY Change"] = pd.to_numeric(df["YoY Change"].replace("∞", np.nan), errors='coerce')
df["Three Month Change"] = pd.to_numeric(df["Three Month Change"].replace("∞", np.nan), errors='coerce')
df["Avg. Monthly Searches"] = pd.to_numeric(df["Avg. Monthly Searches"], errors='coerce')
df = df.dropna()

# Add quadrant category
def classify_quadrant(row):
    if row["YoY Change"] > 0 and row["Three Month Change"] > 0:
        return "Winners 💚"
    elif row["YoY Change"] < 0 and row["Three Month Change"] < 0:
        return "Fading 🔻"
    elif row["YoY Change"] < 0 and row["Three Month Change"] > 0:
        return "Seasonal Spikes 🔵"
    else:
        return "Long-term Growth 🟠"

df["Trend Type"] = df.apply(classify_quadrant, axis=1)

# Volume slider
min_vol = int(df["Avg. Monthly Searches"].min())
max_vol = int(df["Avg. Monthly Searches"].max())
volume_range = st.slider("Filter by Avg. Monthly Searches", min_vol, max_vol, (min_vol, max_vol), step=100)

# Filter data
filtered = df[
    (df["Avg. Monthly Searches"] >= volume_range[0]) &
    (df["Avg. Monthly Searches"] <= volume_range[1])
]

# Plot interactive bubble chart
fig = px.scatter(
    filtered,
    x="YoY Change",
    y="Three Month Change",
    size="Avg. Monthly Searches",
    color="Trend Type",
    text="Keyword",
    title="Fashion Trend Quadrant Chart",
    labels={
        "YoY Change": "Year-over-Year Change (%)",
        "Three Month Change": "3-Month Change (%)"
    },
    height=600
)
fig.update_traces(textposition='top center', marker=dict(opacity=0.7, line=dict(width=1, color='DarkSlateGrey')))
fig.add_hline(y=0, line_dash="dash", line_color="gray")
fig.add_vline(x=0, line_dash="dash", line_color="gray")

st.plotly_chart(fig, use_container_width=True)
