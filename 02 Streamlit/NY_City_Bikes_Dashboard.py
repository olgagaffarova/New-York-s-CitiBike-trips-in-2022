################################################ DIVVY BIKES DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
import plotly.io as pio
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
warnings.filterwarnings('ignore')

# Configure Seaborn with advanced color palettes
sns.set_theme(style="darkgrid")
plt.style.use('dark_background')

# Professional, subtle color palettes
subtle_colors = ['#6366f1', '#8b5cf6', '#a855f7', '#c084fc', '#d8b4fe', 
                '#e879f9', '#f0abfc', '#f9a8d4', '#fbb6ce', '#fecaca',
                '#fed7aa', '#fde68a', '#fef3c7', '#ecfdf5', '#a7f3d0',
                '#6ee7b7', '#34d399', '#10b981', '#059669', '#047857']

# Professional color palettes
advanced_palettes = {
    'professional': subtle_colors,
    'blues': ['#eff6ff', '#dbeafe', '#bfdbfe', '#93c5fd', '#60a5fa', '#3b82f6', '#2563eb', '#1d4ed8'],
    'cool': ['#f0f9ff', '#e0f2fe', '#bae6fd', '#7dd3fc', '#38bdf8', '#0ea5e9', '#0284c7', '#0369a1'],
    'warm': ['#fef7ed', '#fed7aa', '#fdba74', '#fb923c', '#f97316', '#ea580c', '#dc2626', '#b91c1c'],
    'nature': ['#f7fee7', '#ecfccb', '#d9f99d', '#bef264', '#a3e635', '#84cc16', '#65a30d', '#4d7c0f'],
    'purple': ['#faf5ff', '#f3e8ff', '#e9d5ff', '#d8b4fe', '#c084fc', '#a855f7', '#9333ea', '#7c3aed']
}

# Set professional palette
sns.set_palette(subtle_colors)


########################### Initial settings for the dashboard ##################################################################

st.set_page_config(page_title="CitiBike 2022 - Introduction", layout="wide")

# ──────────────────────────────────────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────────────────────────────────────

st.title("NYC CitiBike 2022")
st.markdown("Goal of the analysis:To reduce bike shortages by up to 50% in 2023 at the top 20% busiest start stations (which together handle 80% of CitiBike demand) by optimizing bike relocation from nearby overloaded stations.")
st.markdown("## Introduction: Understanding the CitiBike System")


########################## Import data ###########################################################################################

top15 = pd.read_csv('02 Streamlit/top15_dashboard.csv', index_col = 0)
df_group = pd.read_csv('02 Streamlit/df_group_dashboard.csv', index_col = 0)
df_daily_weather = pd.read_csv('02 Streamlit/df_daily_weather_dashboard.csv', index_col = 0)
donors_receivers = pd.read_csv('02 Streamlit/donors_receivers.csv', index_col = 0)


# ######################################### DEFINE THE CHARTS #####################################################################

### 1) Bar chart — Top 15 Most Popular Start Stations in New York ###

# Create the Plotly figure
fig = go.Figure(
    go.Bar(
        x=top15['start_station_name'],          # station names on X-axis
        y=top15['trips_per_station'],           # trip counts on Y-axis
        marker=dict(
            color=top15['trips_per_station'],   # color by trip count
            colorscale='Blues',
            showscale=True,
            colorbar=dict(title='Trip Count')
        ),
        text=top15['trips_per_station'],        # show numbers on bars
        textposition='outside'
    )
)

# Update chart layout
fig.update_layout(
    title='Top 15 Most Popular Start Stations in New York',
    xaxis_title='Station Name',
    yaxis_title='Number of Trips',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='black', size=11),
    x

### 2) Add the map -- top 14% routes covering 80% of trips ###

st.header("Interactive Map — Aggregated Trip Flows")

# Load Kepler map HTML
path_to_html = "02 Streamlit/nyc_bike_map.html"
with open(path_to_html, "r", encoding="utf-8") as f:
    html_data = f.read()

# Display the map
st.components.v1.html(html_data, height=900, scrolling=True)

# Add explanatory text under the map
st.markdown(
    """
    #### 📌 How to interpret this map

    - Only **14.5% of all CitiBike routes** account for **80% of total trip volume** (Pareto ratio).
    - On average, these high-demand routes carry **~163 trips per year each**.
    - The single busiest start–end pair reached **12,041 trips** in 2022.

    These high-traffic routes represent the strongest opportunities for **bike rebalancing and operational optimization**.
    """
)

### 3) CitiBike Station Imbalance (Rentals − Returns) ###

# Horizontal bar chart of net flow
fig = px.bar(
    donors_receivers,
    x="mean_net_flow",
    y="station_name",
    orientation="h",
    color="mean_net_flow",
    color_continuous_scale=["red", "lightgray", "blue"],
    title="CitiBike Station Imbalance (Rentals − Returns)",
    labels={
        "mean_net_flow": "Net Bike Flow (Daily Average)",
        "station_name": "Station"
    }
)

fig.update_layout(
    yaxis={'categoryorder': 'total ascending'},
    height=700,
    margin=dict(l=220),
)

fig.update_yaxes(automargin=True)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
- 🔵 **Positive net flow (blue):** More bikes **leave** than arrive → **shortage risk**  
  → stations need **bike delivery**.
- 🔴 **Negative net flow (red):** More bikes **arrive** than leave → **overflow risk**  
  → stations need **bike removal**.

Midtown stations such as **Broadway**, **Madison Ave**, and **West End Ave** show consistent *shortages*,  
while **Old Slip & South St** and **Washington Square E** accumulate bikes during the day.  

**Action:** Relocate bikes from red to blue zones during **7–9 AM** and **5–7 PM**  
to reduce shortages and full-dock issues by up to **50 %**.
"""
)

### Why this matters

By relocating bikes *from red stations to blue stations* during peak windows  
(morning 7-9 AM, evening 5-7 PM), CitiBike can: 

- reduce shortages and full-dock issues by **up to 50%**  
- increase rider satisfaction  
- optimize redistribution truck mileage  
"""
)
