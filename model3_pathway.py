"""
model3_pathway.py (Real Pathway Version)

This script defines a real-time processing pipeline using the Pathway framework.
It simulates Model 3: Competitive Pricing, where parking prices are adjusted
based on demand and nearby competitors' prices using geo-distance filtering.
"""

import pathway as pw
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2

# Pathway Schema Definition
class ParkingSchema(pw.Schema):
    SystemCodeNumber: str
    Latitude: float
    Longitude: float
    Capacity: int
    Occupancy: int
    QueueLength: int
    VehicleType: str
    TrafficConditionNear: str
    IsSpecialDay: int
    Timestamp: pw.DateTimeUtc

# Haversine Distance Function
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    return R * 2 * np.arcsin(np.sqrt(a))

# Core UDF: Compute Adjusted Price
@pw.udf
def compute_adjusted_batch(rows):
    df = pd.DataFrame(rows)

    vehicle_weights = {"car": 1.0, "bike": 0.5, "truck": 1.5}
    traffic_weights = {"low": 1.0, "medium": 0.5, "high": 0.1}

    df["VehicleWeight"] = df["VehicleType"].map(vehicle_weights)
    df["TrafficScore"] = df["TrafficConditionNear"].map(traffic_weights)

    
    # Demand calculation
    α, β, γ, δ, ε = 2.0, 1.0, 1.5, 2.0, 1.0
    df["Demand"] = (
        α * (df["Occupancy"] / df["Capacity"])
        + β * df["QueueLength"]
        - γ * df["TrafficScore"]
        + δ * df["IsSpecialDay"]
        + ε * df["VehicleWeight"]
    )

    demand_min, demand_max = df["Demand"].min(), df["Demand"].max()
    df["DemandNorm"] = (df["Demand"] - demand_min) / (demand_max - demand_min + 1e-6)

    # Base price
    BASE = 10
    LAMBDA = 0.5
    df["BasePrice"] = BASE * (1 + LAMBDA * df["DemandNorm"])
    df["BasePrice"] = df["BasePrice"].clip(5, 20)

    # Adjusted pricing with competitors
    adjusted = []
    for idx, row in df.iterrows():
        lat1, lon1 = row["Latitude"], row["Longitude"]
        time = row["Timestamp"]
        lot = row["SystemCodeNumber"]

        nearby = df[(df["Timestamp"] == time) & (df["SystemCodeNumber"] != lot)].copy()
        nearby["Distance"] = nearby.apply(lambda x: haversine(lat1, lon1, x["Latitude"], x["Longitude"]), axis=1)
        nearby = nearby[nearby["Distance"] <= 500]

        theta = 0.1
        if not nearby.empty:
            avg_price = nearby["BasePrice"].mean()
            adj = row["BasePrice"] + theta * (row["BasePrice"] - avg_price)
        else:
            adj = row["BasePrice"]

        adjusted.append(np.clip(adj, 5, 20))

    df["AdjustedPrice"] = adjusted
    return df[["SystemCodeNumber", "Timestamp", "AdjustedPrice"]].to_dict("records")

# Main Pathway Execution
def main():
    table = pw.io.csv.read(
        "data/cleaned_dataset.csv",
        schema=ParkingSchema,
        mode="streaming"
    )

    grouped = table.groupby(table.Timestamp).collect()

    processed = grouped.select_rows(
        compute_adjusted_batch(pw.this.rows)
    )

    pw.io.csv.write(processed, "model3_output.csv")
    pw.run()

if __name__ == "__main__":
    main()