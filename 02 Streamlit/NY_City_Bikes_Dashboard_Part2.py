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
        "Member vs Casual Patterns",
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
    The following chart highlights the **15 busiest start stations**, mostly in **central Manhattan**, 
    where daily commuter demand is highest.
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

# ───────────────────────────────────────────────
# PAGE 2: MEMBER VS CASUAL PATTERNS
# ───────────────────────────────────────────────
elif page == "Member vs Casual Patterns":
    st.title("👥 Member vs Casual User Patterns")

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
# PAGE 3: WEATHER IMPACT + FLEET OPTIMIZATION
# ───────────────────────────────────────────────
elif page == "Weather Impact and Fleet Optimization (Nov–Apr)":
    st.title("🌦️ Weather Impact and Fleet Optimization (Nov–Apr)")

    st.markdown("""
    This section analyzes how **temperature** and **rainfall** influence ridership, 
    and recommends **fleet reduction by 30–40% during November–April**.
    """)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df_group['date'], y=df_group['bike_rides_daily'], name='Bike Rides',
                             mode='lines', line=dict(color=blue, width=2)), secondary_y=False)
    fig.add_trace(go.Scatter(x=df_daily_weather['date'], y=df_daily_weather['avgTemp'],
                             name='Avg Temperature (°C)', mode='lines',
                             line=dict(color=orange, width=2, dash='dot')), secondary_y=True)
    fig.update_layout(template='plotly_white', hovermode='x unified',
                      legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                      height=600, margin=dict(l=40, r=40, t=80, b=40))
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Number of Bike Rides", secondary_y=False)
    fig.update_yaxes(title_text="Average Temperature (°C)", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Daily Bike Rides and Precipitation (2022)")
    figp = make_subplots(specs=[[{"secondary_y": True}]])
    figp.add_trace(go.Scatter(x=df_daily_precipitations.index, y=df_daily_precipitations['bike_rides_daily'],
                              name='Bike Rides', mode='lines', line=dict(color=blue, width=2)), secondary_y=False)
    figp.add_trace(go.Scatter(x=df_daily_precipitations.index, y=df_daily_precipitations['daily_rain_mm'],
                              name='Total Precipitation (mm)', mode='lines',
                              line=dict(color=orange, width=2, dash='dot')), secondary_y=True)
    figp.update_layout(template='plotly_white', hovermode='x unified',
                       legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                       height=600, margin=dict(l=40, r=40, t=80, b=40))
    figp.update_xaxes(title_text="Date")
    figp.update_yaxes(title_text="Number of Bike Rides", secondary_y=False)
    figp.update_yaxes(title_text="Total Precipitation (mm)", secondary_y=True)
    st.plotly_chart(figp, use_container_width=True)

    st.markdown("""
    **Recommendation:**  
    Reduce active bikes by **30–40% between November–April** to match lower ridership, 
    cutting storage and maintenance costs without affecting service.
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
    Introduces **dynamic redistribution** and **predictive scheduling** for morning (7–9 AM) 
    and evening (5–7 PM) peaks to prevent shortages and overflow.
    """)


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
    5. Identify **Peak-Hour Pressure Points** to support targeted expansion
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
            label=nodes
        ),
        link=dict(
            source=[node_index[s] for s in top_flows["start_station_name"]],
            target=[node_index[e] for e in top_flows["end_station_name"]],
            value=top_flows["value"],
            color="rgba(255,127,14,0.5)"
        )
    )

    fig = go.Figure(data=[sankey_data])

    fig.update_layout(
        title="Top Waterfront Origin → Destination Flows (Stations with Highest Trip Pressure)",
        height=800,
        font=dict(size=13, color="black"),
        plot_bgcolor="white",
        paper_bgcolor="white"
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

    import plotly.express as px
    import pandas as pd

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
	
	st.markdown("""
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
    """)
	



# ───────────────────────────────────────────────
# PAGE 7: RECOMMENDATIONS
# ───────────────────────────────────────────────
elif page == "Recommendations":
    st.title("💡 Strategic Recommendations")

    st.markdown("""
    - **Scale Back Fleet During Off-Season (Nov–Apr)** → reduce active bikes by **30–40%**  
    - **Expand Docking Stations Along the Waterfront** → target **Hudson & East River corridors**  
    - **Implement Predictive Redistribution** → rebalance **7–9 AM & 5–7 PM**  
    - **Prioritize Top 600 Stations** covering **80% of trips**  
    - **Adjust Maintenance & Staffing** in line with seasonal demand
    """)

