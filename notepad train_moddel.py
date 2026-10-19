import os
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# ---------------------------------------------------------
# 1. File paths
# ---------------------------------------------------------

INPUT_FILE = "data/processed/hyderabad_rainfall_features_2022.csv"
OUTPUT_FILE = "data/processed/hyderabad_rainfall_risk_2022.csv"
MODEL_DIR = "models"

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# ---------------------------------------------------------
# 2. Load REAL rainfall data
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

df["date"] = pd.to_datetime(df["date"])

print("\nReal rainfall data loaded")
print("Records:", len(df))
print("Date range:", df["date"].min().date(), "to", df["date"].max().date())

# ---------------------------------------------------------
# 3. Features
# ---------------------------------------------------------

features = [
    "rainfall_24h_mm",
    "rainfall_3day_mm",
    "rainfall_7day_mm"
]

X = df[features].copy()

# Safety check
if X.isnull().any().any():
    raise ValueError("Missing values found in rainfall features.")

# ---------------------------------------------------------
# 4. Standardize features
# ---------------------------------------------------------

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---------------------------------------------------------
# 5. Train REAL-DATA anomaly detection model
# ---------------------------------------------------------

model = IsolationForest(
    n_estimators=300,
    contamination=0.10,
    random_state=42
)

model.fit(X_scaled)

# ---------------------------------------------------------
# 6. Calculate anomaly score
# ---------------------------------------------------------

df["anomaly_prediction"] = model.predict(X_scaled)
df["anomaly_score"] = -model.decision_function(X_scaled)

# Higher score = more unusual rainfall condition

# ---------------------------------------------------------
# 7. Convert anomaly score into 0-100 risk score
# ---------------------------------------------------------

min_score = df["anomaly_score"].min()
max_score = df["anomaly_score"].max()

if max_score == min_score:
    df["risk_score"] = 0
else:
    df["risk_score"] = (
        (df["anomaly_score"] - min_score)
        / (max_score - min_score)
        * 100
    )

df["risk_score"] = df["risk_score"].round(2)

# ---------------------------------------------------------
# 8. Add rainfall-based intensity
# ---------------------------------------------------------

def risk_level(score):
    if score < 25:
        return "LOW"
    elif score < 50:
        return "MODERATE"
    elif score < 75:
        return "HIGH"
    else:
        return "VERY HIGH"

df["risk_level"] = df["risk_score"].apply(risk_level)

# ---------------------------------------------------------
# 9. Save results
# ---------------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)

# ---------------------------------------------------------
# 10. Display important results
# ---------------------------------------------------------

print("\nML TRAINING COMPLETED")
print("----------------------------------------")

print("Output file:")
print(OUTPUT_FILE)

print("\nHighest rainfall-risk days:")

top = df.sort_values(
    "risk_score",
    ascending=False
)[
    [
        "date",
        "rainfall_24h_mm",
        "rainfall_3day_mm",
        "rainfall_7day_mm",
        "risk_score",
        "risk_level"
    ]
].head(15)

print(top.to_string(index=False))

print("\nRisk-level counts:")
print(df["risk_level"].value_counts())

print("\nModel completed using REAL 2022 Hyderabad rainfall observations.")