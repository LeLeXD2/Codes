import pandas as pd
import numpy as np
from pathlib import Path

INPUT_PATH = Path("data/final/final_ml_dataset.csv")
OUTPUT_PATH = Path("data/deployment/latest_stock_features.csv")

FEATURES = [
    "Return_1d",
    "Return_5d",
    "Vol_20",
    "Trend_Strength",
    "Momentum_Accel",
    "Volume_Z",
    "Rolling_MaxDD",
    "Relative_Return",
    "Relative_Momentum",
    "MomentumRiskAdj",
]

# Load only columns needed by the deployed chatbot
required_columns = [
    "Date",
    "Ticker",
    *FEATURES
]

print("Loading final dataset...")

df = pd.read_csv(
    INPUT_PATH,
    usecols=required_columns
)

df["Date"] = pd.to_datetime(df["Date"])

df = df.replace(
    [np.inf, -np.inf],
    np.nan
).dropna()

# Use the latest date available across the market
latest_date = df["Date"].max()

latest = df[
    df["Date"] == latest_date
].copy()

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

latest.to_csv(
    OUTPUT_PATH,
    index=False
)

print(f"Latest date: {latest_date}")
print(f"Stocks saved: {len(latest)}")
print(f"Saved to: {OUTPUT_PATH}")