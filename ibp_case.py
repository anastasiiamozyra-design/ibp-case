import numpy as np
import pandas as pd

np.random.seed(42)

# -----------------------------
# 1. Generate demand data
# -----------------------------
days = 60
base_demand = 100
noise = np.random.normal(0, 12, days)
trend = np.linspace(0, 10, days)
seasonality = 8 * np.sin(np.arange(days) / 5)

demand = np.maximum(20, (base_demand + trend + seasonality + noise)).round().astype(int)

df = pd.DataFrame({
    "day": np.arange(1, days + 1),
    "demand": demand
})

# -----------------------------
# 2. Parameters
# -----------------------------
lead_time = 3
initial_inventory = 220
order_quantity = 250
before_reorder_point = 120

forecast_window = 7
service_factor = 0.8
order_up_to_days = 3

# -----------------------------
# 3. Simulation
# -----------------------------
def simulate_inventory(data, mode="before"):
    inventory = initial_inventory
    pipeline_orders = []
    records = []

    for i in range(len(data)):
        day = int(data.loc[i, "day"])
        actual_demand = int(data.loc[i, "demand"])

        arrivals_today = sum(qty for arrival_day, qty in pipeline_orders if arrival_day == day)
        inventory += arrivals_today
        pipeline_orders = [(d, q) for d, q in pipeline_orders if d != day]

        sales = min(inventory, actual_demand)
        stockout = max(0, actual_demand - inventory)
        inventory -= sales

        if mode == "after":
            history_start = max(0, i - forecast_window + 1)
            demand_history = data.loc[history_start:i, "demand"]

            forecast_mean = demand_history.mean()
            forecast_std = demand_history.std(ddof=0) if len(demand_history) > 1 else 0

            safety_stock = service_factor * forecast_std * np.sqrt(lead_time)
            reorder_point = forecast_mean * lead_time + safety_stock
            target_stock = forecast_mean * (lead_time + order_up_to_days) + safety_stock

            inventory_position = inventory + sum(q for _, q in pipeline_orders)

            if inventory_position < reorder_point:
                order_qty = max(0, int(round(target_stock - inventory_position)))
                if order_qty > 0:
                    pipeline_orders.append((day + lead_time, order_qty))
            else:
                order_qty = 0

        else:
            if inventory <= before_reorder_point:
                order_qty = order_quantity
                pipeline_orders.append((day + lead_time, order_qty))
            else:
                order_qty = 0

        records.append({
            "day": day,
            "demand": actual_demand,
            "closing_inventory": inventory,
            "stockout": stockout,
            "order": order_qty
        })

    result = pd.DataFrame(records)

    total_demand = result["demand"].sum()
    total_sales = total_demand - result["stockout"].sum()

    kpis = {
        "avg_inventory": round(float(result["closing_inventory"].mean()), 1),
        "service_level": round(float(total_sales / total_demand * 100), 1),
        "total_stockouts": int(result["stockout"].sum())
    }

    return kpis

before_kpis = simulate_inventory(df, "before")
after_kpis = simulate_inventory(df, "after")

print("BEFORE:", before_kpis)
print("AFTER:", after_kpis)