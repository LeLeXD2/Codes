import pandas as pd
import numpy as np
import os

folder = "data/raw"
stock_data = {}

# =====================================================
# LOAD ALL STOCKS
# =====================================================

for file in os.listdir(folder):

    if not file.endswith(".csv"):
        continue

    ticker = file.replace(".csv", "")

    df = pd.read_csv(f"{folder}/{file}")

    # Remove Yahoo Finance extra rows
    df = df.iloc[2:].reset_index(drop=True)

    df.rename(columns={"Price": "Date"}, inplace=True)

    df["Date"] = pd.to_datetime(df["Date"])

    numeric_cols = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.dropna(inplace=True)

    stock_data[ticker] = df

print(f"Loaded {len(stock_data)} stocks")


# =====================================================
# BUILD EQUAL-WEIGHT MARKET INDEX
# =====================================================

market_prices = []

for ticker, df in stock_data.items():

    temp = df[["Date", "Close"]].copy()

    temp.rename(
        columns={"Close": ticker},
        inplace=True
    )

    market_prices.append(
        temp.set_index("Date")
    )

market = pd.concat(
    market_prices,
    axis=1
)

market["Market_Close"] = market.mean(axis=1)

market = market[["Market_Close"]].reset_index()

market["Market_Return"] = market["Market_Close"].pct_change()

market["Market_Return20"] = market["Market_Close"].pct_change(20)

market["Market_Momentum"] = (
    market["Market_Close"].pct_change(20)
)

# =====================================================
# FEATURE ENGINEERING
# =====================================================

final_data = []

for ticker, df in stock_data.items():

    df = df.copy()

    ####################################################
    # MERGE MARKET DATA FIRST
    ####################################################

    df = df.merge(
        market,
        on="Date",
        how="left"
    )

    ####################################################
    # RETURNS
    ####################################################

    df["Return_1d"] = df["Close"].pct_change()

    df["Return_5d"] = df["Close"].pct_change(5)

    df["Future_Return_5d"] = (
        df["Close"].shift(-5)
        /
        df["Close"]
        - 1
    )

    ####################################################
    # VOLATILITY
    ####################################################

    df["Vol_20"] = (
        df["Return_1d"]
        .rolling(20)
        .std()
    )

    ####################################################
    # MOMENTUM
    ####################################################

    df["Momentum_5"] = (
        df["Close"].pct_change(5)
    )

    df["Momentum_20"] = (
        df["Close"].pct_change(20)
    )

    df["Momentum_Accel"] = (
        df["Momentum_5"]
        -
        df["Momentum_20"]
    )

    df["MomentumRiskAdj"] = (
        df["Momentum_20"]
        /
        (df["Vol_20"] + 1e-9)
    )
    ####################################################
    # TREND
    ####################################################

    ma10 = df["Close"].rolling(10).mean()

    ma50 = df["Close"].rolling(50).mean()

    df["Trend_Strength"] = (
        (ma10 - ma50)
        /
        (ma50 + 1e-9)
    )

    ####################################################
    # VOLUME
    ####################################################

    vol_mean = (
        df["Volume"]
        .rolling(20)
        .mean()
    )

    vol_std = (
        df["Volume"]
        .rolling(20)
        .std()
    )

    df["Volume_Z"] = (
        (df["Volume"] - vol_mean)
        /
        (vol_std + 1e-9)
    )

    ####################################################
    # RELATIVE FEATURES
    ####################################################

    df["Relative_Return"] = (
        df["Return_1d"]
        -
        df["Market_Return"]
    )

    df["Relative_Momentum"] = (
        df["Momentum_20"]
        -
        df["Market_Momentum"]
    )

    ####################################################
    # DRAWDOWN
    ####################################################

    rolling_max = (
        df["Close"]
        .rolling(60)
        .max()
    )

    drawdown = (
        df["Close"]
        /
        rolling_max
        - 1
    )

    df["Rolling_MaxDD"] = (
        drawdown
        .rolling(60)
        .min()
    )

    ####################################################
    # CLEAN
    ####################################################

    df.dropna(inplace=True)

    df["Ticker"] = ticker

    df.drop(
        columns=[
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ],
        inplace=True
    )

    final_data.append(df)

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    df.to_csv(
        f"data/processed/{ticker}.csv",
        index=False
    )


# =====================================================
# FINAL DATASET
# =====================================================

final_df = pd.concat(
    final_data,
    ignore_index=True
)

os.makedirs(
    "data/final",
    exist_ok=True
)

final_df.to_csv(
    "data/final/final_ml_dataset.csv",
    index=False
)

print("\nDONE")
print(final_df.shape)

print("\nTarget Distribution")
print(final_df["Future_Return_5d"].describe())

print("\nColumns")
print(final_df.columns)