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

```mermaid
graph TD
    A[cleaned_dataset.csv] --> B[Python Program for Models]
    B --> C[Price Calculation Logic]
    C --> D[Bokeh Visualization]
    D --> E[Ngrok Public URL]






