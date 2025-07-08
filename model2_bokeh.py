
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, DatetimeTickFormatter
from bokeh.plotting import figure, curdoc
from bokeh.driving import linear
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Simulate a preprocessed dataset
n_points = 100
timestamps = pd.date_range(start='2025-07-07 08:00', periods=n_points, freq='30min')
occupancy = np.random.randint(10, 50, size=n_points)
capacity = 50
queue = np.random.randint(0, 10, size=n_points)
traffic = np.random.choice([1.0, 0.5, 0.1], size=n_points)
special_day = np.random.choice([0, 1], size=n_points)
vehicle_weight = np.random.choice([1.0, 0.5, 1.5], size=n_points)

# Demand Function
α, β, γ, δ, ε = 2.0, 1.0, 1.5, 2.0, 1.0
demand_raw = (
    α * (occupancy / capacity)
    + β * queue
    - γ * traffic
    + δ * special_day
    + ε * vehicle_weight
)

scaler = MinMaxScaler()
demand_norm = scaler.fit_transform(demand_raw.reshape(-1, 1)).flatten()

BASE_PRICE = 10
LAMBDA = 0.5
MIN_PRICE = 5
MAX_PRICE = 20
prices = BASE_PRICE * (1 + LAMBDA * demand_norm)
prices = np.clip(prices, MIN_PRICE, MAX_PRICE)

source = ColumnDataSource(data=dict(x=[], y=[]))

p = figure(title="Real-Time Parking Price Plot (Model 2)",
           x_axis_type='datetime', width=800, height=400)
p.line(x='x', y='y', source=source, line_width=2, color='green')
p.xaxis.formatter = DatetimeTickFormatter(minutes="%H:%M", hours="%H:%M")
p.yaxis.axis_label = "Price ($)"
p.xaxis.axis_label = "Time"

index = dict(i=0)

@linear()
def update(step):
    i = index['i']
    if i >= len(timestamps):
        return
    new_data = dict(x=[timestamps[i]], y=[prices[i]])
    source.stream(new_data, rollover=200)
    index['i'] += 1

curdoc().add_root(column(p))
curdoc().add_periodic_callback(update, 500)


