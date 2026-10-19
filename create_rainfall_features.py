import pandas as pd
from pathlib import Path

input_file = Path("data/processed/hyderabad_rainfall_2022.csv")
output_file = Path("data/processed/hyderabad_rainfall_features_2022.csv")

df = pd.read_csv(input_file)

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values("date").reset_index(drop=True)

# Real rainfall from the official NetCDF dataset
df["rainfall_24h_mm"] = df["rainfall_mm"]

# Rolling rainfall accumulation
df["rainfall_3day_mm"] = (
    df["rainfall_mm"]
    .rolling(window=3, min_periods=1)
    .sum()
)

df["rainfall_7day_mm"] = (
    df["rainfall_mm"]
    .rolling(window=7, min_periods=1)
    .sum()
)

# Rainfall intensity category
def classify_intensity(rain):
    if rain == 0:
        return "No Rain"
    elif rain < 10:
        return "Light"
    elif rain < 25:
        return "Moderate"
    elif rain < 50:
        return "Heavy"
    else:
        return "Very Heavy"

df["rainfall_intensity"] = df["rainfall_mm"].apply(
    classify_intensity
)

output_file.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_file, index=False)

print("========== RAINFALL FEATURES ==========")
print("Records:", len(df))
print("Output:", output_file)

print("\nColumns:")
for column in df.columns:
    print("-", column)

print("\nFirst 10 records:")
print(df.head(10).to_string(index=False))

print("\n========================================")