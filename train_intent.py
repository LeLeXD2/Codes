import joblib
import os

import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.linear_model import (
    LogisticRegression
)

from sklearn.pipeline import Pipeline

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    "data/intent/intent_data.csv"
)


print("\nDataset:")
print(df.head())


print("\nIntent distribution:")
print(
    df["intent"].value_counts()
)


print("\nTotal examples:")
print(len(df))

X = df["text"]
y = df["intent"]

X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )
)


print("Training examples:", len(X_train))
print("Testing examples:", len(X_test))

intent_model = Pipeline([

    (
        "tfidf",

        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )
    ),

    (
        "classifier",

        LogisticRegression(
            max_iter=1000,
            random_state=42,
            class_weight="balanced"
        )
    )

])

# ==========================================
# TRAIN MODEL
# ==========================================

intent_model.fit(
    X_train,
    y_train
)

print("\nIntent model trained.")

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


predictions = intent_model.predict(
    X_test
)


accuracy = accuracy_score(
    y_test,
    predictions
)


print("\n================================")
print("INTENT CLASSIFIER RESULTS")
print("================================")

print(
    f"Accuracy: {accuracy:.2%}"
)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions
    )
)


print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        predictions
    )
)

os.makedirs(
    "model",
    exist_ok=True
)


joblib.dump(
    intent_model,
    "model/intent_classifier.pkl"
)


print(
    "\nSaved model to "
    "model/intent_classifier.pkl"
)