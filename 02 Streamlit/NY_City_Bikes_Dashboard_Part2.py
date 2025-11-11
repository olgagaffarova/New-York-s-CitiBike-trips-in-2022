############################################################
# 🗽 NYC CITIBIKE 2022 DASHBOARD
# Author: Olga Gaffarova
# Goal: Reduce bike shortages by 50% at top 20% busiest stations
############################################################

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ───────────────────────────────────────────────
# CONFIGURATION
# ───────────────────────────────────────────────
sns.set_theme(style="darkgrid")
plt.style.use('dark_background')

st.set_page_config(page_title="CitiBike 2022", layout="wide")

# Sidebar Navigation
st.sidebar.title("Dashboard Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["About Citibike", "Member vs Casual Patterns", "Weather Impact", "Identifying Main Routes and Problem Stations", "Recommendations"]
)

# ───────────────────────────────────────────────
# LOAD DATA
# ───────────────────────────────────────────────
top15 = pd.read_csv('02 Streamlit/top15_dashboard.csv', index_col=0)
df_group = pd.read_csv('02 Streamlit/df_group_dashboard.csv', index_col=0)
df_daily_weather = pd.read_csv('02 Streamlit/df_daily_weather_dashboard.csv', index_col=0)
donors_receivers = pd.read_csv('02 Streamlit/donors_receivers.csv', index_col=0)
df_heat = pd.read_csv('02 Streamlit/df_heat.csv', index_col=0)
df_daily_precipitations = pd.read_csv('02 Streamlit/df_daily_precipitations.csv', index_col=0, parse_dates=True)
hours_member_casual = pd.read_csv('02 Streamlit/hours_member_casual.csv', index_col=0)


# ───────────────────────────────────────────────
# PAGE 1: INTRO + HOURLY & MONTHLY RIDERSHIP
# ───────────────────────────────────────────────
if page == "About Citibike":

    st.title("🚴 CitiBike 2022: Understanding New York’s Bike Network")

    # --- Intro text ---
    st.markdown("""
    ### **Project Objective:**  
As the lead analyst for New York City’s **CitiBike**, this project aims to conduct a **descriptive analysis** of 2022 usage data to help the business strategy team assess the **bike distribution model** and identify **expansion opportunities**. The goal is to uncover **actionable insights** that prevent bike shortages and ensure CitiBike’s continued leadership in **sustainable urban mobility**.  

Since launching in **2013**, CitiBike has grown into a network of **33,000 bikes** and **4,600 docking stations** across **Manhattan, Brooklyn, and Queens**. However, uneven demand, seasonal patterns, and capacity limits have created persistent **availability issues** at key stations.  

This dashboard explores how, when, and where riders use the system to support smarter decision-making around fleet management and station planning. It focuses on three key business questions:  

1. **Seasonal Scaling:** How much should the fleet be **scaled back between November and April** to match lower demand while reducing maintenance costs?  
2. **Network Expansion:** How can data guide the decision on **adding new stations** along high-demand **waterfront routes**?  
3. **Redistribution Strategy:** What operational strategies can ensure bikes remain **available at the busiest stations**, especially during peak morning and evening hours?  

    """)

    # --- Top 15 stations bar chart ---
    st.markdown("""
    ### 🏙️ Top 15 Most Popular Start Stations in New York")

The analysis begins by examining overall CitiBike activity across New York City to identify **where most trips start**.  
The chart below shows the **15 most popular start stations** in 2022 — areas with the **highest ridership volumes** throughout the year.  

These stations are mainly located in **central Manhattan**, close to business districts, parks, and major transportation hubs.  
Understanding these high-demand areas provides a clear picture of the **core network structure** and highlights where maintaining a steady bike supply is essential to meet daily commuter demand.  
   """)


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

    # --- Divider between charts ---
    st.markdown("---")

    # --- Hourly & Monthly Heatmap section ---
    st.markdown("### 🕒 Hourly and Monthly CitiBike Demand")

    st.markdown("""
    The heatmap visualizes how **CitiBike demand** varies by hour and month in **2022**.  
    Morning (**7–9 a.m.**) and evening (**5–7 p.m.**) peaks dominate across all seasons, with the highest activity between **June and August**.  
    These patterns highlight the **commuter-driven nature** of CitiBike use and the need for **efficient bike redistribution** during rush hours, especially in summer months.
    """)

    # Order months chronologically
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    df_heat["month"] = pd.Categorical(df_heat["month"], categories=month_order, ordered=True)

    # --- Plotly heatmap ---
    fig = px.density_heatmap(
        df_heat,
        x="hour",
        y="month",
        z="rides",
        color_continuous_scale="Blues",
        title="CitiBike Rides by Hour and Month (2022)"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        font=dict(size=14),
        coloraxis_colorbar=dict(title="Number of Rides"),
        margin=dict(l=80, r=60, t=60, b=60)
    )

    st.plotly_chart(fig, use_container_width=True)



# ───────────────────────────────────────────────
# PAGE 2: MEMBER VS CASUAL PATTERNS
# ───────────────────────────────────────────────

elif page == "Members vs Casual Users Patterns":
    st.title("👥 Members vs Casual Users Ride Patterns")

    st.markdown("""
    This section compares the **hourly usage patterns** of CitiBike members and casual users,
    further broken down by the **type of bike** used (classic or electric).  
    Members show strong commuting peaks on weekdays, while casual users favor late morning
    and afternoon leisure rides.
    """)

    # --- Plotly Facet Bar Chart by Member Type and Bike Type ---
    fig = px.bar(
        hours_member_casual,
        x='hour',
        y='ride_id',
        color='rideable_type',         # adds bike type breakdown
        facet_col='member_casual',     # members vs casual
        labels={
            'hour': 'Hour of Day',
            'ride_id': 'Number of Rides',
            'rideable_type': 'Bike Type'
        },
        title='Hourly Ride Patterns by User Type and Bike Type',
        color_discrete_sequence=px.colors.qualitative.Set2  # soft, distinct colors
    )

    fig.update_layout(
        barmode='stack',              # stack bike types in each hour
        showlegend=True,
        height=550,
        margin=dict(t=80, l=40, r=40, b=40),
        title_font=dict(size=16),
        legend_title_text='Bike Type'
    )

    fig.update_xaxes(dtick=1)

    st.plotly_chart(fig, use_container_width=True)


# ───────────────────────────────────────────────
# PAGE 3: SEASONALITY & WEATHER
# ───────────────────────────────────────────────

elif page == "Weather Impact":
    st.title("Weather Impact on CitiBike Demand")
    st.markdown("""
    This section explores how **temperature** and **precipitation** affect CitiBike ridership.  
    Colder or rainy days tend to reduce daily rides, while warm and dry conditions encourage more cycling.
    """)

    # --- DAILY RIDES VS AVERAGE TEMPERATURE ---
    st.markdown("### Daily Bike Rides and Average Temperature (2022)")
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Left Y-axis — Bike Rides
    fig.add_trace(
        go.Scatter(
            x=df_group['date'],
            y=df_group['bike_rides_daily'],
            name='Bike Rides',
            mode='lines',
            line=dict(color='#0ea5e9', width=2)
        ),
        secondary_y=False
    )

    # Right Y-axis — Average Temperature
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

    fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        height=600,
        margin=dict(l=40, r=40, t=80, b=40)
    )

    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Number of Bike Rides", secondary_y=False)
    fig.update_yaxes(title_text="Average Temperature (°C)", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)
    
    # ================================================================
    # DAILY RIDES VS PRECIPITATION
    # ================================================================
    st.subheader("Daily Bike Rides and Precipitation (2022)")

    fig_precip = make_subplots(specs=[[{"secondary_y": True}]])

    # Left Y-axis — Bike Rides
    fig_precip.add_trace(
        go.Scatter(
            x=df_daily_precipitations.index,
            y=df_daily_precipitations['bike_rides_daily'],
            name='Bike Rides',
            mode='lines',
            line=dict(color='#0ea5e9', width=2)
        ),
        secondary_y=False
    )

    # Right Y-axis — Precipitation
    fig_precip.add_trace(
        go.Scatter(
            x=df_daily_precipitations.index,
            y=df_daily_precipitations['daily_rain_mm'],
            name='Total Precipitation (mm)',
            mode='lines',
            line=dict(color='#a855f7', width=2, dash='dot')
        ),
        secondary_y=True
    )

    fig_precip.update_layout(
        title='Daily Bike Rides and Total Precipitation — 2022',
        template='plotly_white',
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        height=600,
        margin=dict(l=40, r=40, t=80, b=40)
    )

    fig_precip.update_xaxes(title_text="Date")
    fig_precip.update_yaxes(title_text="Number of Bike Rides", secondary_y=False)
    fig_precip.update_yaxes(title_text="Total Precipitation (mm)", secondary_y=True)

    st.plotly_chart(fig_precip, use_container_width=True)






# ───────────────────────────────────────────────
# PAGE 4: Identifying Main Routes and Problem Stations 
# ───────────────────────────────────────────────
elif page == "Identifying Main Routes and Problem Stations":
    st.title("Pareto Analysis: Top 14% Routes Covering 80% of Trips")
    st.markdown("""
    Applying the **Pareto Principle (80/20 rule)** helps focus on the most significant routes.  
    The **top 14% of all routes** in 2022 account for **80% of total CitiBike trips**.  
    These high-traffic routes reveal where rebalancing and optimization bring the most benefit.
    """)

    st.markdown("### Aggregated Trip Flows in New York (Pareto Ratio)")
    path_to_html = "02 Streamlit/nyc_bike_map.html"
    with open(path_to_html, "r", encoding="utf-8") as f:
        html_data = f.read()
    st.components.v1.html(html_data, height=900, scrolling=True)

    st.title("🚲 Identifying Problem Stations and Strategic Recommendations")
    st.markdown("""
    This section identifies **stations with persistent bike shortages or overflows**  
    using the **mean net flow** (rentals − returns) metric across 2022.
    
    - **Positive net flow → Donor stations** (bikes leave → shortage risk)  
    - **Negative net flow → Receiver stations** (bikes accumulate → overflow risk)
    """)

    # ───────────────────────────────────────────────
    # STATION IMBALANCE
    # ───────────────────────────────────────────────
    st.title("CitiBike Station Imbalance (Rentals − Returns)")

    fig = go.Figure()

    # Color stations by net flow: red = shortage, blue = overflow
    colors = [
        'tomato' if x > 0 else 'royalblue'
        for x in donors_receivers['mean_net_flow']
    ]

    fig.add_trace(go.Bar(
        y=donors_receivers['station_name'],
        x=donors_receivers['mean_net_flow'],
        orientation='h',
        marker_color=colors,
        text=donors_receivers['mean_net_flow'].round(1),
        textposition='outside',
    ))

    fig.update_layout(
        title="CitiBike Station Imbalance (Positive = Shortage Risk, Negative = Overflow)",
        xaxis_title="Mean Net Flow (Rentals − Returns)",
        yaxis_title="Station",
        height=800,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=11),
        xaxis=dict(
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='black'
        ),
        showlegend=False,
        margin=dict(l=220, r=40, t=80, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)


# ───────────────────────────────────────────────
# PAGE 5: RECOMMENDATIONS
# ───────────────────────────────────────────────
elif page == "Recommendations":
    st.title("💡 Strategic Recommendations")

    st.markdown("""
    ### 1️⃣ Scale Back Fleet During Off-Season (Nov–Apr)
    Reduce active bikes by **30–40%**, matching seasonal demand drops while lowering maintenance and storage costs.  
    This aligns supply with reduced winter ridership and helps free up resources for high-demand months.

    ### 2️⃣ Expand Docking Stations Along the Waterfront
    High trip density along riverside routes (Hudson & East River) indicates strong potential for **new docking points**.  
    Expanding capacity in these zones will ease congestion at inner-city stations and attract more leisure riders.

    ### 3️⃣ Implement Predictive Redistribution
    Rebalance bikes between **7–9 AM** and **5–7 PM** — from overflow to shortage areas — using existing fleet data.  
    Integrating weather and demand forecasts can make daily relocation more efficient and responsive.

    ### 4️⃣ Focus on Top Imbalance Clusters
    Prioritize the **~600 busiest stations** (covering 80% of all rides) for redistribution scheduling.  
    Targeting this core network can improve reliability and rider satisfaction with minimal resource expansion.
    """)

    st.markdown("---")
    st.subheader("🔍 Suggested Directions for Future Analysis")
    st.markdown("""
    **• Transport Service Disruptions**  
    Incorporate data on temporary construction, maintenance, or street closures — especially at night — to assess their impact on trip volume and route selection.

    **• Event and Seasonal Planning**  
    Cross-reference trip data with **city event calendars** (concerts, parades, sports games, festivals) to anticipate demand surges and pre-position bikes in nearby zones.

    **• Integration with Other Mobility Data**  
    Combine CitiBike data with public transport usage (MTA turnstile or bus ridership) to explore multimodal patterns and support city-wide mobility optimization.
    """)



