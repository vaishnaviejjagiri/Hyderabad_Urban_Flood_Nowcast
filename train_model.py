import pandas as pd
import numpy as np
from pathlib import Path

# ---------------------------------------------------------
# Hyderabad Urban Flood Nowcast
# Real-data rainfall risk model
# ---------------------------------------------------------

INPUT_FILE = Path("data/processed/hyderabad_rainfall_features_2022.csv")
OUTPUT_FILE = Path("data/processed/hyderabad_rainfall_risk_2022.csv")

# Load real rainfall features
df = pd.read_csv(INPUT_FILE)

features = [
    "rainfall_24h_mm",
    "rainfall_3day_mm",
    "rainfall_7day_mm"
]

# Check required columns
missing = [column for column in features if column not in df.columns]

if missing:
    raise ValueError(f"Missing columns: {missing}")

# Make sure values are numeric
X = df[features].astype(float)

# ---------------------------------------------------------
# Robust normalization using percentile ranges
# ---------------------------------------------------------

risk_components = []

for column in features:
    values = X[column].to_numpy()

    low = np.percentile(values, 5)
    high = np.percentile(values, 95)

    if high == low:
        normalized = np.zeros(len(values))
    else:
        normalized = (values - low) / (high - low)

    normalized = np.clip(normalized, 0, 1)

    risk_components.append(normalized)

# Weighted rainfall risk
# Recent rainfall gets the highest importance.
risk_score = (
    0.50 * risk_components[0] +
    0.30 * risk_components[1] +
    0.20 * risk_components[2]
) * 100

df["risk_score"] = np.round(risk_score, 2)

# ---------------------------------------------------------
# Risk categories
# ---------------------------------------------------------

def classify_risk(score):
    if score < 25:
        return "LOW"
    elif score < 50:
        return "MODERATE"
    elif score < 75:
        return "HIGH"
    else:
        return "VERY HIGH"

df["risk_level"] = df["risk_score"].apply(classify_risk)

# ---------------------------------------------------------
# Save result
# ---------------------------------------------------------

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)

print()
print("==============================================")
print("Hyderabad Rainfall Risk Model Completed")
print("==============================================")
print(f"Input records : {len(df)}")
print(f"Output file   : {OUTPUT_FILE}")
print()

print("Risk-level counts:")
print(df["risk_level"].value_counts())

print()
print("Top 10 highest-risk rainfall events:")
print(
    df[
        [
            "date",
            "rainfall_24h_mm",
            "rainfall_3day_mm",
            "rainfall_7day_mm",
            "risk_score",
            "risk_level"
        ]
    ]
    .sort_values("risk_score", ascending=False)
    .head(10)
    .to_string(index=False)
)

print()
print("==============================================")