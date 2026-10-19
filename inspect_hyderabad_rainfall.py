import pandas as pd
from pathlib import Path

file = Path("data/processed/hyderabad_rainfall_2022.csv")

df = pd.read_csv(file)

print("========== DATASET SUMMARY ==========")
print("Rows:", len(df))
print("Columns:", list(df.columns))

print("\n========== RAINFALL STATISTICS ==========")
print(df["rainfall_mm"].describe())

print("\n========== DAYS WITH RAIN ==========")
rain_days = (df["rainfall_mm"] > 0).sum()
print("Rainy days:", rain_days)

print("Dry days:", (df["rainfall_mm"] == 0).sum())

print("\n========== HEAVY RAINFALL DAYS ==========")

for threshold in [10, 25, 50]:
    count = (df["rainfall_mm"] >= threshold).sum()
    print(f">= {threshold} mm:", count, "days")

print("\n========== TOP 20 RAINFALL DAYS ==========")

top20 = df.nlargest(20, "rainfall_mm")

print(
    top20[
        ["date", "latitude", "longitude", "rainfall_mm"]
    ].to_string(index=False)
)

print("\n========== MONTHLY RAINFALL ==========")

df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.month

monthly = (
    df.groupby("month")["rainfall_mm"]
    .agg(["sum", "mean", "max", "count"])
)

print(monthly)

print("\n========== INSPECTION COMPLETE ==========")