import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# 1. PAGE SETUP
# -------------------------
st.set_page_config(
    page_title="Retail Performance Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Retail Performance Dashboard")
st.caption("Demo dashboard with dummy data (sales, margin, inventory risk)")

# -------------------------
# 2. DUMMY DATA GENERATION
# -------------------------

np.random.seed(42)

# We'll pretend this is weekly data for 4 stores
weeks = pd.date_range(start="2025-07-01", periods=12, freq="W")
stores = ["Port Louis", "Curepipe", "Quatre Bornes", "Grand Baie"]

data_rows = []
for store in stores:
    base_sales = np.random.randint(80_000, 140_000)
    for w in weeks:
        weekly_sales = base_sales + np.random.randint(-15_000, 15_000)
        cogs = weekly_sales * np.random.uniform(0.6, 0.8)  # cost of goods sold
        profit = weekly_sales - cogs
        footfall = np.random.randint(800, 1400)
        inventory_value = np.random.randint(200_000, 400_000)

        data_rows.append({
            "week": w,
            "store": store,
            "sales": round(weekly_sales, 2),
            "cogs": round(cogs, 2),
            "profit": round(profit, 2),
            "footfall": footfall,
            "inventory_value": inventory_value
        })

df = pd.DataFrame(data_rows)

# Product-level table (pretend last 30 days)
products = [
    "Premium Cat Food 5kg",
    "Dog Chew Toy XL",
    "Aquarium Filter Pro",
    "Organic Bird Seeds",
    "Flea & Tick Shampoo",
    "Puppy Starter Kit",
    "LED Tank Light 60cm",
    "Fish Flakes Bulk Jar",
]
product_rows = []
for p in products:
    price = np.random.randint(200, 2500)
    units_sold = np.random.randint(20, 200)
    revenue = price * units_sold
    margin_pct = np.random.uniform(0.25, 0.55)
    margin_value = revenue * margin_pct
    stock_left = np.random.randint(0, 80)

    product_rows.append({
        "product": p,
        "price": price,
        "units_sold": units_sold,
        "revenue": round(revenue, 2),
        "margin_pct": round(margin_pct * 100, 1),
        "margin_value": round(margin_value, 2),
        "stock_left": stock_left
    })

df_products = pd.DataFrame(product_rows)

# -------------------------
# 3. FILTERS (sidebar)
# -------------------------
st.sidebar.header("Filters")

# pick store(s)
store_filter = st.sidebar.multiselect(
    "Select store(s)",
    options=stores,
    default=stores
)

# pick date range
min_date = df["week"].min()
max_date = df["week"].max()

date_range = st.sidebar.date_input(
    "Date range (week ending)",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# apply filters
start_date, end_date = date_range
mask = (
    df["store"].isin(store_filter) &
    (df["week"] >= pd.to_datetime(start_date)) &
    (df["week"] <= pd.to_datetime(end_date))
)
df_filtered = df[mask]

# -------------------------
# 4. TOP-LEVEL KPIs
# -------------------------
total_sales = df_filtered["sales"].sum()
total_profit = df_filtered["profit"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
avg_basket = (df_filtered["sales"].sum() / df_filtered["footfall"].sum()
              if df_filtered["footfall"].sum() > 0 else 0)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales (MUR)",
    f"{total_sales:,.0f}"
)
col2.metric(
    "Total Profit (MUR)",
    f"{total_profit:,.0f}",
    help="Sales - COGS"
)
col3.metric(
    "Profit Margin",
    f"{profit_margin:,.1f}%",
    help="Profit / Sales"
)
col4.metric(
    "Avg Basket Size (MUR)",
    f"{avg_basket:,.0f}",
    help="Sales / Footfall"
)

st.divider()

# -------------------------
# 5. SALES TREND (line chart)
# -------------------------
st.subheader("📈 Weekly Sales Trend")

trend_df = (
    df_filtered
    .groupby("week", as_index=False)
    .agg({"sales": "sum", "profit": "sum"})
    .sort_values("week")
)

fig, ax = plt.subplots()
ax.plot(trend_df["week"], trend_df["sales"], marker="o", label="Sales (MUR)")
ax.plot(trend_df["week"], trend_df["profit"], marker="o", label="Profit (MUR)")
ax.set_title("Sales vs Profit Over Time")
ax.set_xlabel("Week")
ax.set_ylabel("MUR")
ax.legend()
ax.grid(alpha=0.3)

st.pyplot(fig)

# -------------------------
# 6. STORE PERFORMANCE (bar chart + table)
# -------------------------
st.subheader("🏬 Store Performance")

store_perf = (
    df_filtered
    .groupby("store", as_index=False)
    .agg({
        "sales": "sum",
        "profit": "sum",
        "footfall": "sum",
        "inventory_value": "mean"
    })
    .rename(columns={
        "sales": "Total Sales (MUR)",
        "profit": "Total Profit (MUR)",
        "footfall": "Total Footfall",
        "inventory_value": "Avg Inventory Value (MUR)"
    })
)

# bar chart of sales per store
fig2, ax2 = plt.subplots()
ax2.bar(store_perf["store"], store_perf["Total Sales (MUR)"])
ax2.set_title("Total Sales by Store")
ax2.set_xlabel("Store")
ax2.set_ylabel("MUR")
ax2.grid(axis="y", alpha=0.3)

st.pyplot(fig2)

st.dataframe(
    store_perf.style.format({
        "Total Sales (MUR)": "{:,.0f}",
        "Total Profit (MUR)": "{:,.0f}",
        "Avg Inventory Value (MUR)": "{:,.0f}"
    })
)

st.caption("Inventory Value = average stock value sitting in that store during the selected period.")

st.divider()

# -------------------------
# 7. TOP PRODUCTS TABLE
# -------------------------
st.subheader("🏆 Top Products (Last 30 Days)")

# Sort products by revenue desc
top_products = df_products.sort_values("revenue", ascending=False)

# Risk flag: low stock but high revenue
def stock_risk(row):
    if row["stock_left"] < 10 and row["revenue"] > top_products["revenue"].median():
        return "⚠️ Low stock"
    elif row["stock_left"] < 5:
        return "🔴 Critical"
    else:
        return "OK"

top_products["restock_flag"] = top_products.apply(stock_risk, axis=1)

st.dataframe(
    top_products[
        [
            "product",
            "units_sold",
            "revenue",
            "margin_pct",
            "stock_left",
            "restock_flag"
        ]
    ].style.format({
        "revenue": "MUR {:,.0f}",
        "margin_pct": "{:,.1f}%",
        "stock_left": "{:,.0f}"
    })
)

st.caption("Red = you're about to go out of stock on something that actually makes money. That's bad 🙂")

# -------------------------
# 8. NOTES / NEXT ACTIONS
# -------------------------
st.markdown("### 🧠 Quick Insights")
# These are simple heuristics. In real life you'd compute them.
high_margin_product = top_products.sort_values("margin_pct", ascending=False).iloc[0]
low_stock_hits = top_products[top_products["restock_flag"] != "OK"]

st.write(
    f"- `{high_margin_product['product']}` has ~{high_margin_product['margin_pct']}% margin. Push this in promos."
)
if not low_stock_hits.empty:
    st.write(
        "- You have high sellers with low stock. Urgent reorder:"
    )
    for _, r in low_stock_hits.iterrows():
        st.write(
            f"  - {r['product']} | Stock left: {r['stock_left']} | Revenue: MUR {r['revenue']:,.0f} | {r['restock_flag']}"
        )
else:
    st.write("- No critical stock issues detected ✅")
