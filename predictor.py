import joblib
import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "model" / "lgb_model.pkl"
DATA_PATH = BASE_DIR / "data" / "deployment" / "latest_stock_features.csv"

# ============================================================
# FEATURES
# ============================================================

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

# ============================================================
# LOAD MODEL AND DEPLOYMENT DATA
# ============================================================

model = joblib.load(MODEL_PATH)

df = pd.read_csv(DATA_PATH)

df["Date"] = pd.to_datetime(df["Date"])

df = (
    df.replace([np.inf, -np.inf], np.nan)
      .dropna(subset=["Ticker", *FEATURES])
)

# ============================================================
# PREDICT MARKET
# ============================================================

def predict_market():

    latest = df.copy()

    latest["Predicted_Return"] = model.predict(
        latest[FEATURES]
    )

    latest["Rank"] = (
        latest["Predicted_Return"]
        .rank(pct=True)
    )

    latest["Signal"] = "HOLD"

    latest.loc[
        latest["Rank"] >= 0.95,
        "Signal"
    ] = "BUY"

    latest.loc[
        latest["Rank"] <= 0.05,
        "Signal"
    ] = "SELL"

    return latest


# ============================================================
# RECOMMEND INDIVIDUAL STOCK
# ============================================================

def recommend_stock(ticker):

    market = predict_market()

    ticker = ticker.upper()

    stock = market[
        market["Ticker"] == ticker
    ]

    if stock.empty:
        return None

    return stock.iloc[0]


# ============================================================
# RETURN TOP-RANKED STOCKS
# ============================================================

def top_stocks(n=5):

    market = predict_market()

    if market.empty:
        return []

    ranked_stocks = market.sort_values(
        "Predicted_Return",
        ascending=False
    )

    top = ranked_stocks.head(n)

    return top[
        [
            "Ticker",
            "Predicted_Return",
            "Rank",
            "Signal"
        ]
    ].to_dict("records")