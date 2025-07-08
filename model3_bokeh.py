import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import ColumnDataSource, Legend
from math import radians, sin, cos, sqrt, atan2

output_notebook()

# ----------------------------
# Helper: Haversine formula
# ----------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# ----------------------------
# Load your processed DataFrame
# (should include: SystemCodeNumber, Timestamp, AdjustedPrice, Latitude, Longitude)
# ----------------------------
df = pd.read_csv("your_adjusted_model3_output.csv")  # Replace this
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# ----------------------------
# Select one lot to visualize
# ----------------------------
target_lot = df["SystemCodeNumber"].unique()[0]
target_df = df[df["SystemCodeNumber"] == target_lot].copy()
lat1, lon1 = target_df.iloc[0]["Latitude"], target_df.iloc[0]["Longitude"]

# ----------------------------
# Calculate nearby competitor prices for each timestamp
# ----------------------------
competitor_prices = []

for t in target_df["Timestamp"]:
    same_time = df[df["Timestamp"] == t].copy()
    same_time = same_time[same_time["SystemCodeNumber"] != target_lot]
    same_time["Distance"] = same_time.apply(
        lambda x: haversine(lat1, lon1, x["Latitude"], x["Longitude"]), axis=1
    )
    nearby = same_time[same_time["Distance"] <= 500]

    if not nearby.empty:
        competitor_prices.append(nearby["AdjustedPrice"].mean())
    else:
        competitor_prices.append(np.nan)

target_df["CompetitorAvgPrice"] = competitor_prices

# ----------------------------
# Plot using Bokeh
# ----------------------------
source = ColumnDataSource(target_df)

p = figure(title=f"Model 3: Price vs Competitor Avg — Lot {target_lot}",
           x_axis_type='datetime', width=800, height=400)

line1 = p.line(x="Timestamp", y="AdjustedPrice", source=source, color="green", line_width=2, legend_label="Your Price")
line2 = p.line(x="Timestamp", y="CompetitorAvgPrice", source=source, color="orange", line_width=2, legend_label="Nearby Avg Price")

p.xaxis.axis_label = "Time"
p.yaxis.axis_label = "Price ($)"
p.legend.location = "top_left"

show(p)