############################################################
# 🗽 NYC CITIBIKE 2022 DASHBOARD
# Author: Olga Gaffarova
############################################################

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import numpy as np
import requests
import pickle
warnings.filterwarnings('ignore')

# ───────────────────────────────────────────────
# CONFIGURATION
# ───────────────────────────────────────────────
sns.set_theme(style="darkgrid")
plt.style.use('dark_background')

st.set_page_config(page_title="CitiBike 2022", layout="wide")


# ───────────────────────────────────────────────
# SIDEBAR NAVIGATION (UPDATED STRUCTURE)
# ───────────────────────────────────────────────
st.sidebar.title("Dashboard Navigation")
page = st.sidebar.radio(
    "Go to:",
    [
        "About Citibike",
        "Weather Impact and Fleet Optimization (Nov–Apr)",
        "Identifying Main Routes and Problem Stations",
        "Predictive Rebalancing Strategy",
        "Waterfront Expansion Opportunities",
        "Recommendations"
    ]
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
monthly_waterfront = pd.read_csv('02 Streamlit/monthly_waterfront.csv', index_col=0)
waterfront_trips = pd.read_csv('02 Streamlit/waterfront_trips.csv', index_col=0)
monthly_type = pd.read_csv('02 Streamlit/fleet_reduction.csv', index_col=0)
low_season = pd.read_csv('02 Streamlit/low_season_summary.csv', index_col=0)
low_season_type = pd.read_csv('02 Streamlit/low_season_type.csv', index_col=0)
popular_stations = pd.read_parquet('02 Streamlit/popular_stations.parquet')



month_order = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

# Define unified color palette
blue = "#0ea5e9"
orange = "#f97316"
bluescale = "Blues"

# ───────────────────────────────────────────────
# PAGE 1: ABOUT CITIBIKE
# ───────────────────────────────────────────────
if page == "About Citibike":

    st.title("🚴 CitiBike 2022: Understanding New York’s Bike Network")

    st.markdown("""
    ### **Project Objective**
    This analysis examines **CitiBike’s 2022 ridership** to improve **bike availability**, optimize **fleet management**, 
    and identify **expansion opportunities** across New York City.
    """)

    st.markdown("""
    #### Top 15 Most Popular Start Stations
    The following chart highlights the **15 busiest start stations**, mostly in **central Manhattan**, where daily commuter demand is highest.
    - Busiest stations are concentrated in **central Manhattan** commuter and tourist zones.
    - Top stations (e.g., *W 21 St & 6 Ave*) exceed **120k annual starts**.
    """)

    fig = go.Figure(
        go.Bar(
            x=top15['start_station_name'],
            y=top15['trips_per_station'],
            marker=dict(
                color=top15['trips_per_station'],
                colorscale=bluescale,
                showscale=True,
                colorbar=dict(title='Trip Count')
            ),
            text=top15['trips_per_station'],
            textposition='outside'
        )
    )

    fig.update_layout(
        title="Top 15 Most Popular Start Stations in New York",
        xaxis_title='Station Name',
        yaxis_title='Number of Trips',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=11),
        xaxis=dict(tickangle=-45, categoryorder='total descending'),
        height=600,
        margin=dict(l=40, r=40, t=80, b=120),
        title_x=0.5
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### Hourly and Monthly CitiBike Demand")
    st.markdown("""
    - Strong **seasonality**: highest demand from **June–September**, lowest in winter months.
    - Daily peaks appear almost every month around **8–10 AM** and **4–7 PM**.
    """)


    df_heat["hour"] = df_heat["hour"].astype(str)
    df_heat["month"] = pd.Categorical(
        df_heat["month"],
        categories=[
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ],
        ordered=True
    )

    fig = px.density_heatmap(
        df_heat,
        x="hour",
        y="month",
        z="rides",
        color_continuous_scale=bluescale
    )

    fig.update_layout(
        title="CitiBike Rides by Hour and Month (2022)",
        template="plotly_white",
        title_x=0.5,
        font=dict(size=14),
        coloraxis_colorbar=dict(title="Number of Rides"),
        margin=dict(l=80, r=60, t=60, b=60)
    )
    fig.update_xaxes(type='category', categoryorder='array', categoryarray=[str(h) for h in range(24)])
    st.plotly_chart(fig, use_container_width=True)


    st.markdown("""
    This section compares **hourly ride behavior** for **members vs casual users**, 
    with breakdown by **bike type (classic vs electric)**.
    """)

    fig = px.bar(
        hours_member_casual,
        x='hour',
        y='ride_id',
        color='rideable_type',
        facet_col='member_casual',
        labels={'hour': 'Hour of Day', 'ride_id': 'Number of Rides', 'rideable_type': 'Bike Type'},
        color_discrete_sequence=[blue, orange]
    )

    fig.update_layout(
		title="Member vs Casual User Patterns",
        barmode='stack',
        showlegend=True,
        height=550,
        margin=dict(t=80, l=40, r=40, b=40),
        title_font=dict(size=16),
        legend_title_text='Bike Type'
    )
    fig.update_xaxes(dtick=1)
    st.plotly_chart(fig, use_container_width=True)

# ───────────────────────────────────────────────
# PAGE 2: WEATHER IMPACT + FLEET OPTIMIZATION
# ───────────────────────────────────────────────

elif page == "Weather Impact and Fleet Optimization (Nov–Apr)":

    # ------------------------------------------------------------
    # PAGE TITLE + INTRO
    # ------------------------------------------------------------
    st.title("🌦️ Weather Impact and Fleet Optimization (Nov–Apr)")

    st.markdown("""
    Understanding how **weather patterns** influence CitiBike ridership is essential for
    determining how many bikes should remain active during the **low season (November–April)**.

    This page answers three key questions:

    **1. How do temperature shifts influence ridership?**  
    → Strong positive correlation.

    **2. How does rainfall affect daily usage?**  
    → Immediate ridership drop during rain days.

    **3. Given these patterns, how much should we scale back the fleet in winter?**  
    → Recommended **30–40% reduction** based on demand.

    Below you’ll find the analysis broken into four sections:  
    **(A) Temperature impact**, **(B) Rainfall impact**,  
    **(C) Seasonal demand modeling**, and  
    **(D) Fleet reduction recommendations**.
    """)

    # COLOR PALETTE
    blue = "#1f77b4"
    orange = "#ff7f0e"
    light_blue = "#84c2ff"
    light_orange = "#ffb87a"



    # ============================================================
    # A. DAILY BIKE RIDES VS TEMPERATURE
    # ============================================================

    st.markdown("## A. Temperature Impact on Daily Ridership")

    st.markdown("""
    Temperature is the **strongest seasonal predictor** of bike demand.  
    As temperatures rise through spring and summer, ridership increases sharply.
    Once temperatures fall below **10°C**, ridership consistently declines.

    👉 This helps define **when low season begins and ends**.
    """)

    fig_temp = make_subplots(specs=[[{"secondary_y": True}]])

    fig_temp.add_trace(go.Scatter(
        x=df_group['date'],
        y=df_group['bike_rides_daily'],
        name="Bike Rides",
        mode='lines',
        line=dict(color=blue, width=2)
    ), secondary_y=False)

    fig_temp.add_trace(go.Scatter(
        x=df_daily_weather['date'],
        y=df_daily_weather['avgTemp'],
        name="Avg Temperature (°C)",
        mode='lines',
        line=dict(color=orange, width=2, dash='dot')
    ), secondary_y=True)

    fig_temp.update_layout(
        template='plotly_white',
        hovermode='x unified',
        title="Daily Bike Rides vs Temperature (2022)",
        height=550,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig_temp.update_xaxes(title="Date")
    fig_temp.update_yaxes(title="Number of Bike Rides", secondary_y=False)
    fig_temp.update_yaxes(title="Average Temperature (°C)", secondary_y=True)

    st.plotly_chart(fig_temp, use_container_width=True)



    # ============================================================
    # B. DAILY BIKE RIDES VS PRECIPITATION
    # ============================================================

    st.markdown("## B. Rainfall Impact on Daily Ridership")

    st.markdown("""
    Rainfall acts as a **short-term disruptor**:  
    even a few millimeters of rain can cause a noticeable drop in ridership.

    Unlike temperature, which shapes **seasonal trends**,  
    rainfall creates **daily fluctuations** that operators must respond to.
    """)

    fig_rain = make_subplots(specs=[[{"secondary_y": True}]])

    fig_rain.add_trace(go.Scatter(
        x=df_daily_precipitations.index,
        y=df_daily_precipitations['bike_rides_daily'],
        name="Bike Rides",
        mode='lines',
        line=dict(color=blue, width=2)
    ), secondary_y=False)

    fig_rain.add_trace(go.Scatter(
        x=df_daily_precipitations.index,
        y=df_daily_precipitations['daily_rain_mm'],
        name="Total Precipitation (mm)",
        mode='lines',
        line=dict(color=orange, width=2, dash='dot')
    ), secondary_y=True)

    fig_rain.update_layout(
        title="Daily Bike Rides and Precipitation (2022)",
        template="plotly_white",
        hovermode="x unified",
        height=550,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig_rain.update_xaxes(title="Date")
    fig_rain.update_yaxes(title="Number of Bike Rides", secondary_y=False)
    fig_rain.update_yaxes(title="Total Precipitation (mm)", secondary_y=True)

    st.plotly_chart(fig_rain, use_container_width=True)



    # ============================================================
    # C. SEASONAL FLEET SCALING — MODELING DEMAND
    # ============================================================

    st.markdown("## C. Seasonal Demand Patterns (Identifying Low Season)")

    st.markdown("""
    Using temperature and ridership patterns, we estimate demand relative to peak season
    for each bike type.

    - **Classic bikes** decline most sharply in winter.  
    - **Electric bikes** retain stronger winter usage.  
    - **Low season months** clearly fall between **November–April**.

    These curves allow us to convert demand patterns into **monthly reduction targets**.
    """)

    fig1 = go.Figure()

    for bt in monthly_type['rideable_type'].unique():
        df_bt = monthly_type[monthly_type['rideable_type'] == bt]
        fig1.add_trace(go.Scatter(
            x=df_bt['month'],
            y=df_bt['demand_vs_peak_%'],
            mode='lines+markers',
            name=bt.replace("_", " ").title(),
            line=dict(width=3, color=blue if "classic" in bt else orange)
        ))

    fig1.update_layout(
        title="Monthly Demand Patterns by Bike Type",
        template="plotly_white",
        xaxis_title="Month",
        yaxis_title="Demand vs Peak (%)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=450,
    )

    st.plotly_chart(fig1, use_container_width=True)



    # ============================================================
    # D. FLEET REDUCTION RECOMMENDATIONS
    # ============================================================

    st.markdown("## D. Recommended Fleet Reduction (Nov–Apr)")

    st.markdown("""
    Based on monthly demand and the strength of each bike type during winter,
    we calculate **optimal fleet reduction percentages**.

    The heatmap below shows reduction recommendations **per month, per bike type**.
    """)

    # HEATMAP
    pivot_data = monthly_type.pivot(index='rideable_type', columns='month', values='fleet_reduction_%')
    pivot_data.index = pivot_data.index.str.replace('_', ' ').str.title()

    fig2 = go.Figure(
        data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='RdYlGn_r',
            colorbar=dict(title="Fleet Reduction %"),
            showscale=True
        )
    )

    fig2.update_layout(
        title="Fleet Reduction Recommendations (%) — Heatmap View",
        template="plotly_white",
        height=450,
    )

    st.plotly_chart(fig2, use_container_width=True)



    # ============================================================
    # Average reduction bar chart
    # ============================================================

    st.markdown("""
    The next chart summarizes **average reduction during low season (Nov–Apr)**:

    - Classic bikes → require **~58% reduction**  
    - Electric bikes → require **~44% reduction**

    This supports keeping more e-bikes active in winter. Winter ridership drops to about 60–70% below peak for classic bikes and 40–50% below peak for electric bikes. 
    When combined and weighted by actual winter usage, the overall demand reduction equals ~32%.
    Сonsidering daily variability and service reliability, this translates into a safe operational range of 30–40% fleet reduction.
    """)

    low_avg = low_season_type.groupby('rideable_type')['fleet_reduction_%'].mean().sort_values()
    bt_labels = low_avg.index.str.replace("_", " ").str.title()

    fig3 = go.Figure(go.Bar(
        x=low_avg.values,
        y=bt_labels,
        orientation='h',
        marker_color=[light_blue if "Classic" in lab else light_orange for lab in bt_labels]
    ))

    for i, v in enumerate(low_avg.values):
        fig3.add_annotation(x=v + 1, y=i, text=f"{v:.1f}%", showarrow=False, font=dict(size=12))

    fig3.update_layout(
        title="Low-Season Average Reduction (Nov–Apr)",
        xaxis_title="Fleet Reduction (%)",
        template="plotly_white",
        height=400
    )

    st.plotly_chart(fig3, use_container_width=True)



    # ============================================================
    # Ride volume by type (stacked area chart)
    # ============================================================

    st.markdown("""
    This final chart visualizes monthly **ride volumes** by bike type.

    It illustrates why electric bikes should remain more available in winter:
    they continue to serve a large share of riders even in low temperatures.
    """)

    month_order = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']
    
    # Prepare data (sum by month/type and enforce month order)
    pivot_rides = (
        monthly_type
        .groupby(['month','rideable_type'], as_index=False)['total_rides']
        .sum()
    )
    pivot_rides['month'] = pd.Categorical(pivot_rides['month'], categories=month_order, ordered=True)
    pivot_rides = pivot_rides.sort_values('month')
    
    # Wide format for easy plotting
    wide = pivot_rides.pivot(index='month', columns='rideable_type', values='total_rides').fillna(0)
    
    # Color map
    bike_colors = {'electric_bike': '#FFB482', 'classic_bike': '#8FB9FF', 'docked_bike': '#BFE8D9'}
    
    fig_area = go.Figure()
    
    for col in wide.columns:
        fig_area.add_trace(
            go.Scatter(
                x=wide.index.astype(str),
                y=wide[col],
                mode='lines',
                line=dict(width=2),
                stackgroup='one',                 # <- stacked totals on y-axis
                name=col.replace('_',' ').title(),
                hovertemplate='%{x}<br>%{y:,.0f} rides<extra></extra>',
                fill='tonexty',
                fillcolor=bike_colors.get(col, '#888'),
            )
        )
    
    fig_area.update_layout(
		title="Ride Volume Distribution by Type",
        template='plotly_white',
        height=420,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=40, r=20, t=30, b=40),
    )
    # Consistent units: axis + hover show raw counts (with thousands separators)
    fig_area.update_yaxes(title_text='Total Rides', tickformat=',')   # 1,234,567
    fig_area.update_xaxes(title_text='Month', categoryorder='array', categoryarray=month_order)
    
    st.plotly_chart(fig_area, use_container_width=True)
    	



    # ============================================================
    # SUMMARY INSIGHTS
    # ============================================================

    st.markdown("""
    ---
    ## 🔍 Key Takeaways

    - Ridership **drops sharply** with falling temperatures and heavy rainfall.  
    - Electric bikes retain **higher winter usage**, so they should remain more available.  
    - **Low season = November → April**, confirmed by both temperature and demand curves.  
    - Optimal fleet reduction: **30–40%** of bikes during this low season.  
    - Savings can be redirected to **spring maintenance**, dock repairs, and battery readiness.

    **Final Recommendation:**  
    Scale back active bikes by **30–40% between November–April** to match demand while maintaining service reliability.
    """)



# ───────────────────────────────────────────────
# PAGE 4: IDENTIFYING MAIN ROUTES AND PROBLEM STATIONS
# ───────────────────────────────────────────────
elif page == "Identifying Main Routes and Problem Stations":
    st.title("🗺️ Main Routes and Problem Stations")

    st.markdown("""
    The **top 14% of all routes** account for **80% of trips**.  
    This analysis identifies those key corridors and stations with persistent imbalances.
    """)

    path_to_html = "02 Streamlit/nyc_bike_map.html"
    with open(path_to_html, "r", encoding="utf-8") as f:
        html_data = f.read()
    st.components.v1.html(html_data, height=900, scrolling=True)

    st.markdown("### CitiBike Station Imbalance (Rentals − Returns)")
    colors = ['tomato' if x > 0 else blue for x in donors_receivers['mean_net_flow']]
    fig = go.Figure(go.Bar(y=donors_receivers['station_name'], x=donors_receivers['mean_net_flow'],
                           orientation='h', marker_color=colors,
                           text=donors_receivers['mean_net_flow'].round(1), textposition='outside'))
    fig.update_layout(title="Station Imbalance (Positive = Shortage, Negative = Overflow)",
                      xaxis_title="Mean Net Flow", yaxis_title="Station",
                      height=800, plot_bgcolor='white', paper_bgcolor='white',
                      font=dict(color='black', size=11), margin=dict(l=220, r=40, t=80, b=40))
    st.plotly_chart(fig, use_container_width=True)


# ───────────────────────────────────────────────
# PAGE 5: PREDICTIVE REBALANCING STRATEGY
# ───────────────────────────────────────────────

elif page == "Predictive Rebalancing Strategy":
	st.title("🔁 Predictive Rebalancing Strategy")
	st.markdown("""
	Introduces **dynamic redistribution** and **predictive scheduling** for **morning (7–9 AM)** 
	and **evening (5–7 PM)** peaks to prevent shortages and overflow.  
	The model below visualizes **daily net bike flow** at the busiest stations 
	to anticipate where bikes should be **added or removed** throughout the day.
	""")
	

	# ------------------------------------------------
	# Sidebar filters
	# ------------------------------------------------
	st.sidebar.markdown("### 🔍 Filter View")
	
	# Month filter
	selected_month = st.sidebar.selectbox(
	    "Select Month:", 
	    sorted(popular_stations["month"].unique()),
	    format_func=lambda x: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
	                           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][int(x)-1]
	)
	
	# Day filter (assuming 'day' is day of month or day of week)
	selected_day = st.sidebar.selectbox(
	    "Select Day:", 
	    sorted(popular_stations["day"].unique())
	)
	
	# Hour slider
	selected_hour = st.sidebar.slider(
	    "Select Hour (0–23):", 
	    min_value=int(popular_stations["hour"].min()), 
	    max_value=int(popular_stations["hour"].max()), 
	    value=8
	)
	
	# ------------------------------------------------
	# Filter dataset based on user selection
	# ------------------------------------------------
	filtered_df = popular_stations[
	    (popular_stations["month"] == selected_month) &
	    (popular_stations["day"] == selected_day) &
	    (popular_stations["hour"] == selected_hour)
	].copy()
	
	# ------------------------------------------------
	# Check if data exists for selection
	# ------------------------------------------------
	if filtered_df.empty:
	    st.warning("⚠️ No data available for this month, day, and hour combination. Please try different filters.")
	else:
	    # ------------------------------------------------
	    # Calculate inflow/outflow summary
	    # ------------------------------------------------
	    st.markdown("### 🚲 Net Bike Flow — Station-Level View")
	
	    # Negative net_flow = more bikes leaving (needs bikes added)
	    # Positive net_flow = more bikes arriving (needs bikes removed)
	    filtered_df["net_flow_status"] = filtered_df["net_flow"].apply(
	        lambda x: "Receiver (Needs Bikes)" if x < 0 else "Donor (Has Surplus)"
	    )
	
	    donor_sum = filtered_df[filtered_df["net_flow"] > 0]["net_flow"].sum()
	    receiver_sum = filtered_df[filtered_df["net_flow"] < 0]["net_flow"].sum()
	
	    col1, col2 = st.columns(2)
	    col1.metric("🚚 Total Bikes to Remove", f"{int(donor_sum)}")
	    col2.metric("📦 Total Bikes to Add", f"{int(abs(receiver_sum))}")
	
	    # ------------------------------------------------
	    # Sort and take top 20 stations by absolute net flow
	    # ------------------------------------------------
	    top_stations = filtered_df.sort_values(
	        "net_flow", 
	        ascending=True
	    ).head(20)
	
	    # ------------------------------------------------
	    # Plotly visualization
	    # ------------------------------------------------
	    fig = px.bar(
	        top_stations,
	        x="net_flow",
	        y="station",
	        orientation='h',
	        color="net_flow_status",
	        color_discrete_map={
	            "Donor (Has Surplus)": "#22c55e",
	            "Receiver (Needs Bikes)": "#ef4444"
	        },
	        title=f"Top 20 Stations — Net Bike Flow (Month: {selected_month}, Day: {selected_day}, Hour: {selected_hour}:00)",
	        hover_data={
	            "rides_started": True,
	            "rides_ended": True,
	            "total_activity": True,
	            "net_flow_status": False
	        },
	        labels={
	            "net_flow": "Net Bike Flow",
	            "station": "Station Name",
	            "rides_started": "Rides Started",
	            "rides_ended": "Rides Ended",
	            "total_activity": "Total Activity"
	        }
	    )
	
	    fig.update_layout(
	        xaxis_title="Net Bike Flow (Started - Ended)",
	        yaxis_title="Station Name",
	        title_x=0.05,
	        title_font=dict(size=18),
	        height=600,
	        plot_bgcolor="rgba(0,0,0,0)",
	        paper_bgcolor="rgba(0,0,0,0)",
	        legend_title_text="Station Status",
	        showlegend=True,
	        xaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='gray')
	    )
	
	    st.plotly_chart(fig, use_container_width=True)
	
	    # ------------------------------------------------
	    # Detailed Table View
	    # ------------------------------------------------
	    st.markdown("### 📊 Detailed Station Data")
	    
	    # Prepare display dataframe
	    display_df = top_stations[['station', 'rides_started', 'rides_ended', 'net_flow', 'total_activity']].copy()
	    display_df['action_required'] = display_df['net_flow'].apply(
	        lambda x: f"ADD {abs(int(x))} bikes" if x < 0 else f"REMOVE {int(x)} bikes"
	    )
	    
	    # Rename columns for display
	    display_df.columns = ['Station', 'Rides Started', 'Rides Ended', 'Net Flow', 'Total Activity', 'Action Required']
	    
	    st.dataframe(
	        display_df,
	        use_container_width=True,
	        hide_index=True
	    )
	
	    # ------------------------------------------------
	    # Notes section
	    # ------------------------------------------------
	    st.markdown("""
	    ---
	    **Interpretation:**
	    - **Red bars (Receivers)** → Stations where more rides END than START — bikes are accumulating, need **removal**.
	    - **Green bars (Donors)** → Stations where more rides START than END — bikes are depleting, need **addition**.
	    - Negative net flow = needs bikes added (more departures than arrivals)
	    - Positive net flow = needs bikes removed (more arrivals than departures)
	
	    **Operational Takeaway:**  
	    Implement dynamic restocking runs during **6–7 AM** and **4–5 PM** based on forecasted net flow 
	    to maintain balanced availability across the network and prevent both shortages and overflow.
	    """)
	
	    # ------------------------------------------------
	    # Download option
	    # ------------------------------------------------
	    csv = display_df.to_csv(index=False)
	    st.download_button(
	        label="📥 Download Station Data as CSV",
	        data=csv,
	        file_name=f"bike_restocking_month{selected_month}_day{selected_day}_hour{selected_hour}.csv",
	        mime="text/csv"
	    )












# ───────────────────────────────────────────────
# PAGE 6: WATERFRONT EXPANSION OPPORTUNITIES
# ───────────────────────────────────────────────
elif page == "Waterfront Expansion Opportunities":
    st.title("Waterfront Expansion Opportunities")
    st.markdown("""
    Explore **spatial demand clusters** along **Hudson and East River** to identify where 
    new stations could relieve congestion and serve leisure riders.
    """)

    # ============================================================================
    # QUESTION & APPROACH
    # ============================================================================
    st.markdown("### **Question:** How to determine how many more stations to add along the water?")
    st.markdown("""
    **Approach Overview:**  
    This analysis applies a **supply-demand framework** to identify capacity gaps.

    **Methodology:**
    1. Define *waterfront stations* based on longitude thresholds  
       *(Hudson River: < -74.01, East River: > -73.95)*
    2. Calculate **Supply** → % of all stations located near the water  
    3. Calculate **Demand** → % of trips that start *or* end near the water  
    4. Perform **Gap Analysis** → If demand exceeds supply, the waterfront is underserved  
    5. Identify **Peak-Months** to support targeted expansion
    """)

    # ============================================================================
    # KEPLER MAP
    # ============================================================================
    st.markdown("### Waterfront Station Distribution (≤ 400m from Shoreline)")
    st.markdown("""
    The map below displays all **stations located within 400 meters of the shoreline**.  
    These stations are classified as *waterfront locations* and represent the **supply base** for this analysis.
    """)
    kepler_html_path = "02 Streamlit/waterfront_stations_kepler.html"
    with open(kepler_html_path, "r", encoding="utf-8") as f:
        st.components.v1.html(f.read(), height=600)

    # --- SUPPLY ANALYSIS SUMMARY ---
    st.markdown("""
    ---
    ### **SUPPLY ANALYSIS (shoreline-based)**
    *Total stations:* 1,757  
    *Waterfront stations (≤ 400m):* 268  
    *Waterfront supply share:* **15.3%**
    """)

    # ============================================================================
    # DEMAND VS SUPPLY CHART
    # ============================================================================
    st.markdown("### Waterfront Demand vs Supply — Monthly Comparison")

    fig = go.Figure()

    # Line for demand (orange)
    fig.add_trace(go.Scatter(
        x=monthly_waterfront["month"],
        y=monthly_waterfront["monthly_demand_share"],
        mode="lines+markers",
        name="Monthly Demand (% of trips touching waterfront)",
        line=dict(width=3, color="#ff7f0e"),
        marker=dict(size=8, color="#ff7f0e")
    ))

    # Flat dashed line for supply (blue)
    fig.add_trace(go.Scatter(
        x=monthly_waterfront["month"],
        y=monthly_waterfront["supply_share"],
        mode="lines",
        name="Waterfront Supply (% of stations on waterfront)",
        line=dict(width=4, dash="dash", color="#1f77b4")
    ))

    fig.update_layout(
        title="Waterfront Demand vs Supply — By Month",
        yaxis_tickformat=".0%",
        xaxis_title="Month",
        yaxis_title="% of Network",
        height=500,
        legend=dict(title="Metrics"),
        plot_bgcolor="white"
    )
    fig.update_yaxes(range=[0.10, 0.30], gridcolor="lightgray")
    st.plotly_chart(fig, use_container_width=True)
	    # ============================================================================
    # HOTSPOT FLOWS — Sankey Diagram
    # ============================================================================
    st.markdown("### Top Waterfront Origin → Destination Flows")

    st.markdown("""
    The Sankey diagram below highlights **the top 20 waterfront routes** with the highest trip counts.  
    Each connection represents a major flow of trips between two waterfront stations, indicating 
    **pressure zones** where additional docks could balance supply and ease congestion.
    """)

    # take top 20 busiest OD pairs
    top_flows = waterfront_trips.head(20)

    # build node labels
    nodes = list(set(top_flows['start_station_name']).union(top_flows['end_station_name']))

    # map station names to index positions
    node_index = {station: idx for idx, station in enumerate(nodes)}

    # create Sankey structure
    sankey_data = dict(
        type='sankey',
        node=dict(
            pad=20,
            thickness=15,
            line=dict(color="black", width=0.5),
            label=nodes,
			color='orange',
			hoverlabel=dict(font=dict(color="black"))

        ),
        link=dict(
            source=[node_index[s] for s in top_flows["start_station_name"]],
            target=[node_index[e] for e in top_flows["end_station_name"]],
            value=top_flows["value"],
			color='steelblue'  
        )
    )

    fig = go.Figure(data=[sankey_data])

    fig.update_layout(
        title="Top Waterfront Origin → Destination Flows (Stations with Highest Trip Pressure)",
        height=1000,
        font=dict(size=15, color="black", family="Arial"),
		paper_bgcolor='white',  # Transparent background
		plot_bgcolor='white'     # Transparent plot area
    )

    st.plotly_chart(fig, use_container_width=True)

    # ============================================================================
    # ORIGIN–DESTINATION MATRIX (HEATMAP) — FIXED LABEL CUT-OFF
    # ============================================================================
    st.markdown("### Origin–Destination Matrix — Top Waterfront Routes")

    st.markdown("""
    The matrix below shows **trip volumes between the busiest waterfront station pairs**.  
    Darker cells indicate stronger flow intensity (higher trip counts).
    """)

    # Create a pivot table: rows = start stations, columns = end stations
    df_matrix = top_flows.pivot_table(
        index='start_station_name',
        columns='end_station_name',
        values='value',
        fill_value=0
    )

    # Optional: sort by total flow
    df_matrix = df_matrix.loc[df_matrix.sum(axis=1).sort_values(ascending=False).index]

    # Optional: shorten labels slightly (if very long)
    df_matrix.index = [name[:25] + "..." if len(name) > 25 else name for name in df_matrix.index]
    df_matrix.columns = [name[:25] + "..." if len(name) > 25 else name for name in df_matrix.columns]

    # Create heatmap
    fig = px.imshow(
        df_matrix,
        color_continuous_scale='Oranges',
        aspect='auto',
        labels=dict(x="Destination Station", y="Origin Station", color="Trips"),
        title="Origin–Destination Matrix — Top Waterfront Routes"
    )

    # --- Layout tweaks for readability ---
    fig.update_layout(
        width=1000,
        height=600,
        margin=dict(l=200, r=200, t=80, b=200),
        xaxis=dict(
            showticklabels=True,
            tickangle=90,
            tickfont=dict(size=11, color="black"),
            automargin=True
        ),
        yaxis=dict(
            showticklabels=True,
            tickfont=dict(size=11, color="black"),
            automargin=True
        ),
        title=dict(font=dict(size=22, color="black")),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    st.plotly_chart(fig, use_container_width=True)
	
	# ============================================================================
    # RECOMMENDATION — WATERFRONT EXPANSION
    # ============================================================================
    st.markdown("""
    ---
    ### Recommendation — Waterfront Expansion

    **Finding:**  
    Waterfront stations make up only **15.3%** of the entire network, while nearly **24% of all trips** start or end near the riverside.  
    This indicates a **demand–supply gap of approximately 9 percentage points**.

    **Recommendation:**  
    To close this gap, CitiBike should add around **150 new docking stations** along the **Hudson River** and **East River**.  
    Expansion should prioritize **high-pressure OD corridors** highlighted in the Sankey diagram — for example:  
    - *Soissons Landing ↔ Vesey St & Church St*  
    - *Roosevelt Island ↔ Pier 40 — Hudson River Park*  

    **Expected Impact:**  
    - Reduce bike shortages at popular leisure and commuter waterfront routes  
    - Improve accessibility for weekend and tourist riders  
    - Balance network capacity between inner-city and riverside zones  

    ---
    """)



# ───────────────────────────────────────────────
# PAGE 7: RECOMMENDATIONS
# ───────────────────────────────────────────────
elif page == "Recommendations":
    st.title("Strategic Recommendations")

    st.markdown("""
    - **Scale Back Fleet During Off-Season (Nov–Apr)** → reduce active bikes by **30–40%**  
    - **Expand Docking Stations Along the Waterfront** → target **Hudson & East River corridors**  
    - **Implement Predictive Redistribution** → rebalance **7–9 AM & 5–7 PM**  
    - **Prioritize Top 600 Stations** covering **80% of trips**  
    - **Adjust Maintenance & Staffing** in line with seasonal demand
    """)

