import pandas as pd
import numpy as np
import optuna

from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("data/final/final_ml_dataset.csv")
df["Date"] = pd.to_datetime(df["Date"])

df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna()

# =========================
# FEATURES
# =========================

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

TARGET = "Future_Return_5d"

# =========================
# WALK FORWARD YEARS
# =========================

TEST_YEARS = list(range(2015, 2025))

print("=" * 60)
print("Walk Forward Validation")
print("=" * 60)

print("Years used:")

for y in TEST_YEARS:
    print(y)

print()

print("Train always uses ALL data before each year.")
print("Validation uses that single year.")

# =========================
# OPTUNA OBJECTIVE
# =========================

def objective(trial):

    params = {

        "objective": "regression",

        "learning_rate": trial.suggest_float(
            "learning_rate",
            0.001,
            0.006,
            log=True
        ),

        "n_estimators": trial.suggest_int(
            "n_estimators",
            500,
            800
        ),

        "num_leaves": trial.suggest_int(
            "num_leaves",
            10,
            100
        ),

        "max_depth": trial.suggest_int(
            "max_depth",
            10,
            15
        ),

        "min_child_samples": trial.suggest_int(
            "min_child_samples",
            20,
            100
        ),

        "subsample": trial.suggest_float(
            "subsample",
            0.6,
            1.0
        ),

        "colsample_bytree": trial.suggest_float(
            "colsample_bytree",
            0.6,
            1.0
        ),

        "reg_alpha": trial.suggest_float(
            "reg_alpha",
            0,
            5
        ),

        "reg_lambda": trial.suggest_float(
            "reg_lambda",
            0,
            5
        ),

        "random_state":42,
        "verbosity":-1,
        "n_jobs":-1

    }

    yearly_ic = []
    yearly_spread = []

    # =====================================
    # WALK FORWARD VALIDATION
    # =====================================

    for year in TEST_YEARS:

        train = df[
            df["Date"] < f"{year}-01-01"
        ].copy()

        valid = df[
            (df["Date"] >= f"{year}-01-01") &
            (df["Date"] < f"{year+1}-01-01")
        ].copy()

        if len(train) == 0 or len(valid) == 0:
            continue

        X_train = train[features]
        y_train = train[TARGET]

        X_valid = valid[features]
        y_valid = valid[TARGET]

        model = LGBMRegressor(**params)

        model.fit(
            X_train,
            y_train
        )

        prediction = model.predict(X_valid)

        # -----------------------------
        # Information Coefficient
        # -----------------------------

        ic = np.corrcoef(
            prediction,
            y_valid
        )[0, 1]

        if np.isnan(ic):
            ic = 0

        # -----------------------------
        # Ranking
        # -----------------------------

        temp = valid.copy()

        temp["Prediction"] = prediction

        temp["Rank"] = (
            temp.groupby("Date")["Prediction"]
                .rank(pct=True)
        )

        top = temp[
            temp["Rank"] >= 0.95
        ]

        bottom = temp[
            temp["Rank"] <= 0.05
        ]

        spread = (
            top[TARGET].mean()
            -
            bottom[TARGET].mean()
        )

        if np.isnan(spread):
            spread = 0

        yearly_ic.append(ic)
        yearly_spread.append(spread)

    # =====================================
    # FINAL SCORE
    # =====================================

    average_ic = np.mean(yearly_ic)

    average_spread = np.mean(yearly_spread)

    score = (
        24 * average_ic
        + 120 * average_spread
        - np.std(yearly_ic)
        - 0.5 * np.std(yearly_spread)
    )

    trial.set_user_attr(
        "Average IC",
        average_ic
    )

    trial.set_user_attr(
        "Average Spread",
        average_spread
    )

    return score

# =========================
# RUN OPTUNA
# =========================

study = optuna.create_study(
    direction="maximize"
)

study.optimize(
    objective,
    n_trials=100,
    show_progress_bar=True
)

print("\n==============================")
print("BEST SCORE")
print(study.best_value)

print()

print("Average IC")
print(study.best_trial.user_attrs["Average IC"])

print()

print("Average Spread")
print(study.best_trial.user_attrs["Average Spread"])

print("\n==============================")
print("BEST PARAMETERS")

for k, v in study.best_params.items():
    print(f"{k}: {v}")