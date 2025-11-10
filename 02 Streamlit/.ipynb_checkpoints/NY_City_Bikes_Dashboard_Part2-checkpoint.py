############################################################
# 🗽 NYC CITIBIKE 2022 DASHBOARD
# Author: Olga Gaffarova
# Goal: Reduce bike shortages by 50% at top 20% busiest stations
############################################################

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Configure Seaborn
sns.set_theme(style="darkgrid")
plt.style.use('dark_background')

# Set page layout
st.set_page_config(page_title="CitiBike 2022", layout="wide")

# Sidebar Navigation
st.sidebar.title("📊 Dashboard Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["Intro", "Seasonality & Weather", "Top 14% Routes (Pareto)", "Recommendations"]
)

# ───────────────────────────────────────────────
# Load data
# ───────────────────────────────────────────────
top15 = pd.read_csv('02 Streamlit/top15_dashboard.csv', index_col=0)
df_group = pd.read_csv('02 Streamlit/df_group_dashboard.csv', index_col=0)
df_daily_weather = pd.read_csv('02 Streamlit/df_daily_weather_dashboard.csv', index_col=0)
donors_receivers = pd.read_csv('02 Streamlit/donors_receivers.csv', index_col=0)

# ───────────────────────────────────────────────
# PAGE 1: INTRO
# ───────────────────────────────────────────────
if page == "Intro":
    st.title("🚴 CitiBike 2022: Understanding New York’s Bike Network")
    st.markdown("""
    **Goal:** Reduce bike shortages by up to **50%** in 2023 at the **top 20% busiest stations**,  
    which together handle **80% of all CitiBike demand**, by optimizing redistribution.
    
    Since **2013**, New York City’s *CitiBike* has grown into a network of **33,000 bikes**
    and **4,600 docking stations** across **Manhattan**, **Brooklyn**, and **Queens**.
    """)

    st.markdown("### Top 15 Most Popular Start Stations in New York")

    fig = go.Figure(
        go.Bar(
            x=top15['start_station_name'],
            y=top15['trips_per_station'],
            marker=dict(
                color=top15['trips_per_station'],
                colorscale='Blues',
                showscale=True,
                colorbar=dict(title='Trip Count')
            ),
            text=top15['trips_per_station'],
            textposition='outside'
        )
    )

    fig.update_layout(
        title='Top 15 Most Popular Start Stations in New York',
        xaxis_title='Station Name',
        yaxis_title='Number of Trips',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=11),
        xaxis=dict(tickangle=-45, categoryorder='total descending'),
        height=600,
        margin=dict(l=40, r=40, t=80, b=120)
    )

    st.plotly_chart(fig, use_container_width=True)

# ───────────────────────────────────────────────
# PAGE 2: SEASONALITY & WEATHER
# ───────────────────────────────────────────────
elif page == "Seasonality & Weather":
    st.title("🌦️ Seasonality and Weather Impact on CitiBike Demand")
    st.markdown("""
    *(Coming soon)*  
    This page will explore how **temperature**, **precipitation**, and **seasonal trends**
    affect the overall bike demand and distribution patterns across the city.
    """)

# ───────────────────────────────────────────────
# PAGE 3: PARETO MAP
# ───────────────────────────────────────────────
elif page == "Top 14% Routes (Pareto)":
    st.title("📍 Pareto Analysis: Top 14% Routes Covering 80% of Trips")

    st.markdown("""
    ### Applying the Pareto Principle
    To focus the analysis on the most impactful bike routes, I applied the **80/20 rule** —  
    identifying the smallest share of routes generating the majority of rides.
    
    In this case, the **top 14% of routes** account for **80% of total CitiBike trips** in 2022.
    This allows us to focus redistribution planning on the busiest corridors of the city.
    """)

    st.header("Aggregated Trip Flows in New York (Pareto Ratio)")
    st.markdown("""
    These high-traffic routes represent the strongest opportunities for
    **bike rebalancing and operational optimization**.
    """)

    # Load and display Kepler map
    path_to_html = "02 Streamlit/nyc_bike_map.html"
    with open(path_to_html, "r", encoding="utf-8") as f:
        html_data = f.read()
    st.components.v1.html(html_data, height=900, scrolling=True)

# ───────────────────────────────────────────────
# PAGE 4: RECOMMENDATIONS
# ────────────────────
