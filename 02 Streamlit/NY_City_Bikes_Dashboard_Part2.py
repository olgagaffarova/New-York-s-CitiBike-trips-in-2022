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
from plotly.subplots import make_subplots
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
    **Goal:** Reduce bike shortages by up to **50%** in 2023 at the **top 20% busiest stations**, which together handle **80% of all CitiBike demand**, by optimizing redistribution.
    
    Before diving into operational recommendations, let's explore the CitiBike system through 2022 data—understanding how people use it, when they ride, and what influences demand. These insights will inform our strategic questions about fleet management, expansion, and redistribution.


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

    ### --- SEASONALITY & WEATHER PAGE --- ###


st.title("🌦️ Seasonality and Weather Impact on CitiBike Demand")

st.markdown("""
This visualization compares **daily CitiBike rides** with **average temperature** throughout 2022.  
It helps identify how weather influences ridership trends — colder months show lower demand,  
while warmer temperatures correspond to higher bike usage.
""")

# Create dual-axis line chart
fig = make_subplots(specs=[[{"secondary_y": True}]])

# --- Bike rides (primary y-axis) ---
fig.add_trace(
    go.Scatter(
        x=df_daily_weather['date'],
        y=df_daily_weather['bike_rides_daily'],
        name='Bike Rides',
        mode='lines',
        line=dict(color='#0ea5e9', width=2)
    ),
    secondary_y=False
)

# --- Avg temperature (secondary y-axis) ---
fig.add_trace(
    go.Scatter(
        x=df_daily_weather['date'],
        y=df_daily_weather['avgTemp'],
        name='Avg Temperature (°C)',
        mode='lines',
        line=dict(color='#a855f7', width=2, dash='dot')
    ),
    secondary_y=True
)

# --- Layout ---
fig.update_layout(
    title='Daily

    
    ### --- DAILY RIDES VS PRECIPITATION --- ###

st.markdown("### ☔ Daily Bike Rides and Precipitation (2022)")
st.markdown("""
This chart compares **daily CitiBike rides** with **rainfall levels** across 2022.  
Notice how heavy rain days correspond to a visible **drop in bike usage**,  
highlighting the strong dependence of CitiBike demand on weather conditions.
""")


# Create dual-axis chart
fig = make_subplots(specs=[[{"secondary_y": True}]])

# --- Bike rides (primary y-axis) ---
fig.add_trace(
    go.Scatter(
        x=df_daily_weather['date'],
        y=df_daily_weather['bike_rides_daily'],
        name='Bike Rides',
        mode='lines',
        line=dict(color='#0ea5e9', width=2)
    ),
    secondary_y=False
)

# --- Precipitation (secondary y-axis) ---
fig.add_trace(
    go.Scatter(
        x=df_daily_weather['date'],
        y=df_daily_weather['daily_rain_mm'],
        name='Daily Precipitation (mm)',
        mode='lines',
        line=dict(color='#a855f7', width=2, dash='dot')
    ),
    secondary_y=True
)

# --- Layout ---
fig.update_layout(
    title='Daily Bike Rides and Daily Precipitation (mm) — 2022',
    template='plotly_white',
    hovermode='x unified',
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    height=600,
    margin=dict(l=40, r=40, t=80, b=40)
)

fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="Number of Bike Rides", secondary_y=False)
fig.update_yaxes(title_text="Daily Precipitation (mm)", secondary_y=True)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)

 
    
    
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
# PAGE 4: Identifying Problem Stations for Bike Shortage Reduction
# ────────────────────
  st.markdown("""
This part of the analysis focuses on finding **the top problem docks** — stations that consistently *run out of bikes* during the day.

We use two criteria:

1. **Top 20% busiest stations** (634 high-demand stations)  
2. **Net_flow imbalance (starts − ends)**  
   - Positive net_flow → more trips **start** than end → bikes leave → **shortage risk**
   - Negative net_flow → more trips **end** than start → bikes accumulate → **overflow**

By calculating the **average daily net_flow** per station, we can detect which stations:
- consistently *lose bikes* (shortage → need redistribution **to** them)
- consistently *gain bikes* (overflow → bikes can be redistributed **from** them)
 
  This allows CitiBike to:
- ensure bike availability where riders need them the most  
- reduce operational costs by prioritizing only imbalance hotspots  
- improve customer satisfaction during peak commuter hours    
   """)
    
    # Split into two groups
donors = donors_receivers[donors_receivers['mean_net_flow'] > 0]
receivers = donors_receivers[donors_receivers['mean_net_flow'] < 0]


fig = go.Figure()

fig.add_trace(go.Bar(
    y=donors['station_name'],
    x=donors['mean_net_flow'],
    name='Donor Stations (shortage risk)',
    orientation='h',
    marker_color='royalblue'
))

fig.add_trace(go.Bar(
    y=receivers['station_name'],
    x=receivers['mean_net_flow'],
    name='Receiver Stations (overflow risk)',
    orientation='h',
    marker_color='tomato'
))

fig.update_layout(
    title="CitiBike Station Imbalance (Donors vs Receivers)",
    xaxis_title="Mean Net Flow (Rentals − Returns)",
    yaxis_title="Station",
    height=800,
    barmode='overlay',
    xaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='black'),
    legend=dict(yanchor="bottom", y=0.01, xanchor="right", x=0.95)
)

st.plotly_chart(fig, use_container_width=True)
    
# ───────────────────────────────────────────────
# PAGE 5: RECOMMENDATIONS
# ────────────────────
