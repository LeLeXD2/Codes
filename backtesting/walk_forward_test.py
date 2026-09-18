import pandas as pd
import numpy as np
import joblib

from lightgbm import LGBMRegressor, early_stopping
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score
)

# TRAIN / TEST SPLIT
from lightgbm import LGBMRegressor
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score
)

# LOAD DATA
df = pd.read_csv("data/final/final_ml_dataset.csv")
df["Date"] = pd.to_datetime(df["Date"])

df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna()

# FEATURES
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

test_years = [
    2015,
    2016,
    2017,
    2018,
    2019,
    2020,
    2021,
    2022,
    2023,
    2024
]

results = []

for year in test_years:

    print(f"\nTesting {year}...")

    train_df = df[
        df["Date"] < f"{year}-01-01"
    ].copy()

    test_df = df[
        (df["Date"] >= f"{year}-01-01") &
        (df["Date"] < f"{year+1}-01-01")
    ].copy()

    X_train = train_df[features]
    y_train = train_df["Future_Return_5d"]

    X_test = test_df[features]
    y_test = test_df["Future_Return_5d"]

    model = LGBMRegressor(
        objective="regression",

        learning_rate=0.005351878686308595,
        n_estimators=799,

        num_leaves=15,
        max_depth=12,
        min_child_samples=89,

        subsample=0.6077385073471486,
        colsample_bytree=0.6473840362560956,

        reg_alpha=1.8090553453520448,
        reg_lambda=0.3659591772774496,

        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    rmse = np.sqrt(
        mean_squared_error(y_test, preds)
    )

    mae = mean_absolute_error(
        y_test, preds
    )

    r2 = r2_score(
        y_test, preds
    )

    ic = np.corrcoef(
        preds,
        y_test
    )[0, 1]

    test_df["Predicted_Return"] = preds

    test_df["rank"] = (
        test_df
        .groupby("Date")["Predicted_Return"]
        .rank(pct=True)
    )

    top = test_df[
        test_df["rank"] >= 0.95
    ]

    bottom = test_df[
        test_df["rank"] <= 0.05
    ]

    spread = (
        top["Future_Return_5d"].mean()
        - bottom["Future_Return_5d"].mean()
    )

    results.append({
        "Year": year,
        "RMSE": rmse,
        "MAE": mae,
        "R2": r2,
        "IC": ic,
        "Spread": spread
    })

results_df = pd.DataFrame(results)

print("\n========== WALK FORWARD RESULTS ==========")
print(results_df)

print("\n========== SUMMARY ==========")

print(
    results_df[
        ["RMSE", "MAE", "IC", "Spread"]
    ].mean()
)

print("\nPositive spread years:")

print(
    (results_df["Spread"] > 0).sum(),
    "/",
    len(results_df)
)