# parking_prices_dynamic 

# Dynamic Parking Pricing Engine (Real-Time)

This project simulates real-time dynamic pricing for parking lots using demand and competition-based models.

✅ Implements 3 pricing models  
✅ Simulates real-time ingestion (Pathway-inspired)  
✅ Visualizes results using Bokeh (with Colab + ngrok)


## Tech Stack

- Python
- Bokeh
- Pandas, NumPy
- Pathway (simulated)
- Google Colab
- GitHub Pages (optional for hosting visuals)


## Models Overview

### Model 1: Baseline
- Uses only occupancy ratio to compute price
- Static notebook with basic plot

### Model 2: Demand-Based Dynamic Pricing
- Factors in queue length, traffic, special days, vehicle type
- Uses Bokeh for real-time simulation
- Hosted in Colab with ngrok

### Model 3: Competitive Pricing
- Adds geolocation + nearby competitor prices
- Adjusts pricing based on surrounding lots
- Simulated real-time via fake Pathway + Bokeh

## Sample Screenshots / GIFs

![Model 2 Demo] :
 <img width="802" alt="Screenshot 2025-07-07 at 10 43 50 PM" src="https://github.com/user-attachments/assets/9e00a9cf-6d3f-407a-a7a5-0b30d09b3c3b" />


![Model 3 Demo] :
<img width="813" alt="Screenshot 2025-07-07 at 10 39 04 PM" src="https://github.com/user-attachments/assets/95064b9c-d5ef-4ef2-ad67-e122798cc3ba" />



## Architecture Flow


## Architecture & Workflow

### Overview
This system is designed to calculate real-time parking prices using live-like data and visualize them via Bokeh. It supports multiple pricing models, including demand-based and competition-aware pricing.

### Step-by-Step Flow

1. **`cleaned_dataset.csv` — Input Dataset**
   - Contains simulated real-time parking data for 5 lots
   - Covers 7 days, from 8:00 AM to 4:30 PM (18 slots per day)
   - Fields include: Timestamp, Occupancy, Capacity, Queue, VehicleType, Traffic, etc.

2. **Python Program for Models**
   - Executes Model 1, 2, or 3
   - Implemented in `.py` files or Colab notebooks
   - Model selection determines how prices are calculated

3. **Price Calculation Logic**
   - Model 1: Simple based on occupancy
   - Model 2: Demand score using multiple weighted features
   - Model 3: Adds Haversine distance and adjusts price based on competitor proximity
   - Normalization and clipping ensure safe pricing

4. **Bokeh Visualization**
   - Uses `ColumnDataSource` to stream prices in real time
   - Updates the graph every few seconds
   - Colab-friendly and interactive

5. **Ngrok Public URL**
   - Ngrok tunnels the local Bokeh server to a public web URL
   - Lets evaluators or users open the plot live

### Workflow Summary
```plaintext
cleaned_dataset.csv (simulated stream)
        ↓
Python program (model2 / model3)
        ↓
Apply price logic (demand + location)
        ↓
Stream result into Bokeh plot
        ↓
Public link via ngrok for real-time access
```


```mermaid
graph TD
    A[cleaned_dataset.csv] --> B[Python Program for Models]
    B --> C[Price Calculation Logic]
    C --> D[Bokeh Visualization]
    D --> E[Ngrok Public URL]





