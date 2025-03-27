import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Title and description
st.title("Fashion Trend Quadrant Explorer")
st.markdown("""
Explore keyword performance based on **Year-over-Year (YoY)** and **Three-Month** search trends.  
Use the slider to filter by average monthly search volume. Quadrants highlight trend types.
""")

# Load data from Google Drive
csv_url = "https://drive.google.com/uc?export=download&id=1fsa-86gDxqG9WKHDmYVOo4ESlyXgkn9o"
df = pd.read_csv(csv_url)

# Clean and convert percentage strings and search volumes
def clean_percent(col):
    return pd.to_numeric(col.replace("∞", np.nan).str.replace('%', ''), errors='coerce')

df["YoY change"] = clean_percent(df["YoY change"])
df["Three month change"] = clean_percent(df["Three month change"])
df["Avg. monthly searches"] = pd.to_numeric(df["Avg. monthly searches"], errors='coerce')
df = df.dropna()

# Classify into quadrant trend types
def classify(row):
    x, y = row["YoY change"], row["Three month change"]
    if x > 0 and y > 0:
        return "Winners 💚"
    elif x < 0 and y < 0:
        return "Fading 🔻"
    elif x < 0 and y > 0:
        return "Seasonal Spikes 🔵"
    else:
        return "Long-term Growth 🟠"

df["Trend Type"] = df.apply(classify, axis=1)

# Slider for filtering by search volume
min_vol = int(df["Avg. monthly searches"].min())
max_vol = int(df["Avg. monthly searches"].max())
vol_range = st.slider("Filter by Avg. Monthly Searches", min_vol, max_vol, (min_vol, max_vol), step=10)

# Filtered dataset
filtered = df[
    (df["Avg. monthly searches"] >= vol_range[0]) &
    (df["Avg. monthly searches"] <= vol_range[1])
]

# Set axis limits (symmetric) for square quadrant
x_range = [-150, 150]
y_range = [-150, 150]

# Plot
fig = px.scatter(
    filtered,
    x="YoY change",
    y="Three month change",
    size="Avg. monthly searches",
    color="Trend Type",
    text="Keyword",
    title="Search Volume Quadrant Chart",
    labels={"YoY change": "YoY % Change", "Three month change": "3-Month % Change"},
    height=700
)

fig.update_traces(
    textposition='top center',
    marker=dict(opacity=0.6, sizemode='area', line=dict(width=1, color='DarkSlateGrey'))
)

# Lock aspect ratio and prevent zooming/auto-scaling
fig.update_layout(
    xaxis=dict(range=x_range),
    yaxis=dict(range=y_range, scaleanchor="x", scaleratio=1),
    margin=dict(l=40, r=40, t=60, b=40),
)

# Add quadrant lines
fig.add_hline(y=0, line_dash="dash", line_color="gray")
fig.add_vline(x=0, line_dash="dash", line_color="gray")

# Add quadrant annotations
quadrants = [
    {"x": 75, "y": 120, "text": "Winners 💚"},
    {"x": -75, "y": 120, "text": "Seasonal Spikes 🔵"},
    {"x": -75, "y": -120, "text": "Fading 🔻"},
    {"x": 75, "y": -120, "text": "Long-Term Growth 🟠"},
]

for q in quadrants:
    fig.add_annotation(
        x=q["x"], y=q["y"],
        text=q["text"],
        showarrow=False,
        font=dict(size=12, color="black"),
        align="center",
        opacity=0.7
    )

# Show chart
st.plotly_chart(fig, use_container_width=True)
