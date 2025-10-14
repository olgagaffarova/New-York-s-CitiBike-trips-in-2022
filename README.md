# New York’s Citi Bike 2022 — Strategic Dashboard Project

### **Project Overview**
The goal of this project is to analyze user behavior and identify opportunities for optimizing the **distribution and expansion** of Citi Bike stations across the city.  

The dashboard that will be developed from this analysis will support the business strategy department in diagnosing **bike availability issues** and guiding **data-driven decisions** to ensure a balanced, sustainable, and efficient service network.

---

### **Objective**
The main objective is to perform a **descriptive analysis** of Citi Bike’s 2022 data and generate **actionable insights** about:
- Where and when bike shortages or surpluses occur;
- Which stations experience the highest demand;
- How seasonality and weather affect bike usage;
- Whether current station placement ensures fair coverage across the city.

The insights derived will feed into an **interactive strategic dashboard**, designed to communicate results clearly to non-technical stakeholders and help guide future station expansion.

---

### **Data Context**
Since its launch in 2013, Citi Bike has grown into New York City’s largest bike-sharing program and one of the biggest worldwide.  
Rising demand—especially since the COVID-19 pandemic—has exposed weaknesses in station capacity and bike distribution. Stations in busy commuter areas often run out of bikes, while others remain full, preventing returns.  

This project investigates the causes of such imbalances and provides data-backed recommendations to improve operational efficiency and customer satisfaction.

---

### **Data Sources**
1. **Citi Bike System Data (2022)**  
   Open-source monthly trip data from:  
   [https://s3.amazonaws.com/tripdata/index.html](https://s3.amazonaws.com/tripdata/index.html)  
   Includes start and end times, station names, locations, and bike types.

2. **NOAA Weather Data (LaGuardia Airport Station)**  
   Daily temperature and precipitation data collected using NOAA’s public API:  
   [https://www.noaa.gov/](https://www.noaa.gov/)  

---

### **Tools and Technologies**
- **Programming Language:** Python (v3.10)  
- **Libraries:** pandas, requests, matplotlib, seaborn, plotly, kepler.gl, streamlit  
- **Environment:** Jupyter Notebook / Anaconda  
- **API:** NOAA (National Centers for Environmental Information)

---

### **Project Workflow**
#### **1. Project Planning**
- Formulated analytical questions to guide dashboard development:
  - What are the most popular start and end stations?
  - Which months show the highest and lowest usage levels?
  - Is there a relationship between weather and trip volume?
  - Are stations evenly distributed across the city?
- Designed a visualization plan pairing each question with an appropriate chart or map.

#### **2. Data Sourcing and Preparation**
- Downloaded Citi Bike 2022 trip data and sourced daily weather data from NOAA’s API.
- Used **list comprehension** and **generators** to efficiently read and combine multiple monthly CSV files.
- Cleaned datasets, standardized date formats, and merged the trip and weather data for combined analysis.

#### **3. Descriptive and Exploratory Analysis**
- Calculated trip frequencies by station and month to identify demand peaks.
- Analyzed seasonal trends and correlations with temperature and precipitation.
- Mapped the geographic distribution of stations to identify underserved areas.

#### **4. Visualization and Dashboard Development**
- Created visualizations using **Matplotlib**, **Seaborn**, and **Plotly**.  
- Designed interactive geospatial maps in **Kepler.gl**.  
- Built a prototype dashboard in **Streamlit**, organizing visual outputs into clear sections:
  - Popular Stations  
  - Seasonal Patterns  
  - Weather Impact  
  - Station Distribution  
- The final dashboard will include an introduction, individual graph sections, and a recommendation page.

---

### **Deliverables**
- A **clean and merged dataset** combining trip and weather data.  
- A **series of visualizations** explaining key demand and distribution patterns.  
- A **Streamlit dashboard** presenting insights interactively.  
- A **recommendations summary** highlighting strategies for improving bike distribution and planning new stations.

---

### **Expected Outcomes**
- Clear identification of high-demand stations and routes.  
- Evidence of seasonal and weather-driven variations in trip volume.  
- A visual representation of station density and gaps across New York City.  
- Actionable recommendations to support management’s strategic decisions.

---

### **Author**
**Olga Gaffarova**  
