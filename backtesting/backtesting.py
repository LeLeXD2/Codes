import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("data/final/final_ml_dataset.csv")

df["Date"] = pd.to_datetime(df["Date"])

df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna()

model = joblib.load("model/lgb_model.pkl")

features = [
    'Return_1d',
    'Return_5d',
    'Vol_20',
    'Trend_Strength',
    'Momentum_Accel',
    'Volume_Z',
    'Rolling_MaxDD',
    'Relative_Return',
    'Relative_Momentum',
    'MomentumRiskAdj',
]

# =========================
# TEST PERIOD
# =========================
# TRAIN / TEST SPLIT
latest_date = df["Date"].max()

split_date = latest_date - pd.DateOffset(years=2)

test_df = df[df["Date"] >= split_date].copy()

# =========================
# MODEL PREDICTIONS
# =========================

test_df["Predicted_Return"] = model.predict(
    test_df[features]
)

# =========================
# REBALANCE EVERY 5 DAYS
# =========================

rebalance_dates = sorted(
    test_df["Date"].unique()
)[::5]

test_df = test_df[
    test_df["Date"].isin(rebalance_dates)
].copy()

# =========================
# RANK STOCKS
# =========================

test_df["rank"] = (
    test_df.groupby("Date")["Predicted_Return"]
           .rank(pct=True)
)

# =========================
# SIGNAL SETTINGS
# =========================

BUY_THRESHOLD = 0.95
SELL_THRESHOLD = 0.05

test_df["Signal"] = "HOLD"

test_df.loc[
    test_df["rank"] >= BUY_THRESHOLD,
    "Signal"
] = "BUY"

test_df.loc[
    test_df["rank"] <= SELL_THRESHOLD,
    "Signal"
] = "SELL"

# =========================
# SOFT POSITION SIZING
# =========================

test_df["position"] = 0.0

buy_mask = test_df["rank"] >= BUY_THRESHOLD

sell_mask = test_df["rank"] <= SELL_THRESHOLD

test_df.loc[buy_mask, "position"] = (
    (test_df.loc[buy_mask, "rank"] - BUY_THRESHOLD)
    / (1 - BUY_THRESHOLD)
)

test_df.loc[sell_mask, "position"] = -(
    (SELL_THRESHOLD - test_df.loc[sell_mask, "rank"])
    / SELL_THRESHOLD
)

# =========================
# EQUAL WEIGHT PORTFOLIO
# =========================

active = test_df["position"] != 0

# Count active positions each rebalance day
active_count = (
    test_df[active]
    .groupby("Date")["Ticker"]
    .transform("count")
)

# Equal weight every active stock
test_df["weight"] = 0.0

test_df.loc[active, "weight"] = (
    np.sign(test_df.loc[active, "position"])
    /
    active_count
)

# =========================
# TRANSACTION COST
# =========================

TRANSACTION_COST = 0.001

test_df = test_df.sort_values(
    ["Ticker", "Date"]
)

test_df["prev_weight"] = (

    test_df.groupby("Ticker")["weight"]

    .shift(1)

    .fillna(0)
)

test_df["turnover"] = (

    test_df["weight"]
    - test_df["prev_weight"]

).abs()

# =========================
# RETURNS
# =========================

test_df["gross_return"] = (

    test_df["weight"]

    * test_df["Future_Return_5d"]
)

test_df["net_return"] = (

    test_df["gross_return"]

    - TRANSACTION_COST

    * test_df["turnover"]
)

# =========================
# PORTFOLIO
# =========================

portfolio = (

    test_df.groupby("Date")["net_return"]

    .sum()

    .reset_index()
)

portfolio["equity"] = (

    1 + portfolio["net_return"]

).cumprod()

# =========================
# BUY & HOLD
# =========================

buyhold = (

    test_df.groupby("Date")["Future_Return_5d"]

    .mean()

    .reset_index()
)

buyhold["equity"] = (

    1 + buyhold["Future_Return_5d"]

).cumprod()

# =========================
# METRICS
# =========================

returns = portfolio["net_return"]

sharpe = (

    np.sqrt(252 / 5)

    * returns.mean()

    / (returns.std() + 1e-9)
)

cummax = portfolio["equity"].cummax()

drawdown = (

    portfolio["equity"]

    / cummax

    - 1
)

max_drawdown = drawdown.min()

downside = returns[returns < 0]

sortino = (

    np.sqrt(252 / 5)

    * returns.mean()

    / (downside.std() + 1e-9)
)

volatility = (

    returns.std()

    * np.sqrt(252 / 5)
)

years = len(portfolio) / (252 / 5)

cagr = (

    portfolio["equity"].iloc[-1]

    ** (1 / years)

    - 1
)

win_rate = (returns > 0).mean()

coverage = (

    test_df["position"] != 0

).mean()

num_trades = (

    test_df["position"] != 0

).sum()

# =========================
# SIGNAL QUALITY
# =========================

top = test_df[
    test_df["rank"] >= BUY_THRESHOLD
]

bottom = test_df[
    test_df["rank"] <= SELL_THRESHOLD
]

spread = (

    top["Future_Return_5d"].mean()

    - bottom["Future_Return_5d"].mean()
)

# =========================
# RESULTS
# =========================

print("\n========== PRODUCTION BACKTEST ==========")

print(f"CAGR: {cagr:.2%}")
print(f"Sharpe: {sharpe:.3f}")
print(f"Sortino: {sortino:.3f}")
print(f"Volatility: {volatility:.2%}")
print(f"Win Rate: {win_rate:.2%}")
print(f"Trade Coverage: {coverage:.2%}")
print(f"Number of Trades: {num_trades}")
print(f"Max Drawdown: {max_drawdown:.2%}")
print(f"Final Equity: {portfolio['equity'].iloc[-1]:.3f}")

print("\nSignal Quality")

print(
    "Top Avg Return:",
    top["Future_Return_5d"].mean()
)

print(
    "Bottom Avg Return:",
    bottom["Future_Return_5d"].mean()
)

# =========================
# SAVE CHATBOT SIGNALS
# =========================

test_df[[
    "Ticker",
    "Date",
    "Predicted_Return",
    "rank",
    "Signal",
    "position",
    "weight",
    "Future_Return_5d"
]].to_csv(
    "data/final/chatbot_signals.csv",
    index=False
)

print("\nSaved chatbot_signals.csv")

# =========================
# PLOT
# =========================

plt.figure(figsize=(12, 6))

plt.plot(
    portfolio["Date"],
    portfolio["equity"],
    label="Strategy"
)

plt.plot(
    buyhold["Date"],
    buyhold["equity"],
    label="Buy & Hold"
)

plt.title(
    "LightGBM Strategy vs Buy & Hold"
)

plt.xlabel("Date")

plt.ylabel("Equity")

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.show()

