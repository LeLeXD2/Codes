import pandas as pd
import numpy as np
import joblib

from lightgbm import LGBMRegressor, early_stopping
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score
)

# LOAD DATA
df = pd.read_csv("data/final/final_ml_dataset.csv")
df['Date'] = pd.to_datetime(df['Date'])

df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

print("Dataset:", df.shape)

# TRAIN / TEST SPLIT
latest_date = df["Date"].max()

test_start = latest_date - pd.DateOffset(years=2)
valid_start = latest_date - pd.DateOffset(years=3)

train_df = df[df["Date"] < valid_start].copy()

valid_df = df[
    (df["Date"] >= valid_start) &
    (df["Date"] < test_start)
].copy()

test_df = df[df["Date"] >= test_start].copy()

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

# TARGET
X_train = train_df[features]
y_train = train_df["Future_Return_5d"]

X_valid = valid_df[features]
y_valid = valid_df["Future_Return_5d"]

X_test = test_df[features]
y_test = test_df["Future_Return_5d"]

# LIGHTGBM REGRESSOR
model = LGBMRegressor(
    objective="regression",

    learning_rate=0.003972505390447075,
    n_estimators=743,

    num_leaves=20,
    max_depth=11,
    min_child_samples=87,

    subsample=0.6080498455712349,
    colsample_bytree=0.9593471498107699,

    reg_alpha=0.026447239852232435,
    reg_lambda=3.9464521739130474,

    random_state=42,
    n_jobs=-1
)

print("\nTraining LightGBM...")

# Training with early stopping
model.fit(
    X_train,
    y_train,
    eval_set=[(X_valid, y_valid)],
    eval_metric="rmse",
    callbacks=[early_stopping(100)]
)

# PREDICTIONS
test_df = test_df.copy()

test_df["Predicted_Return"] = model.predict(X_test)

# REGRESSION METRICS
rmse = np.sqrt(
    mean_squared_error(
        y_test,
        test_df["Predicted_Return"]
    )
)

mae = mean_absolute_error(
    y_test,
    test_df["Predicted_Return"]
)

r2 = r2_score(
    y_test,
    test_df["Predicted_Return"]
)

corr = np.corrcoef(
    test_df["Predicted_Return"],
    y_test
)[0,1]

print("\n========== REGRESSION RESULTS ==========")

print(f"RMSE : {rmse:.6f}")
print(f"MAE  : {mae:.6f}")
print(f"R²   : {r2:.4f}")
print(f"IC (Correlation): {corr:.4f}")

# FEATURE IMPORTANCE
importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    "Importance",
    ascending=False
)

print("\n========== FEATURE IMPORTANCE ==========")
print(importance)

# SAVE MODEL
joblib.dump(
    model,
    "model/lgb_model.pkl"
)

# SAVE PREDICTIONS
output = test_df[[
    "Ticker",
    "Date",
    "Predicted_Return",
    "Future_Return_5d"
]]

output.to_csv(
    "data/final/lgb_predictions.csv",
    index=False
)

print("\nSaved:")
print("data/final/lgb_model.pkl")
print("data/final/lgb_predictions.csv")