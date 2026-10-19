import pandas as pd
from pathlib import Path

file = Path(
    "data/processed/hyderabad_rainfall_features_2022.csv"
)

df = pd.read_csv(file)

df["date"] = pd.to_datetime(df["date"])

print("========== FEATURE VALIDATION ==========")

print("\nTotal records:", len(df))

print("\nMissing values:")
print(df.isnull().sum())

print("\nRainfall statistics:")
print(df[
    [
        "rainfall_24h_mm",
        "rainfall_3day_mm",
        "rainfall_7day_mm"
    ]
].describe())

print("\nRainfall intensity counts:")
print(df["rainfall_intensity"].value_counts())

print("\nTop 15 highest daily rainfall events:")

top = df.sort_values(
    "rainfall_24h_mm",
    ascending=False
).head(15)

print(
    top[
        [
            "date",
            "rainfall_24h_mm",
            "rainfall_3day_mm",
            "rainfall_7day_mm",
            "rainfall_intensity"
        ]
    ].to_string(index=False)
)

print("\n========================================")