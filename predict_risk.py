import pandas as pd
import numpy as np

# ---------------------------------------------------------
# Hyderabad Urban Flood Nowcast
# Step 9: Rainfall Risk Prediction
# ---------------------------------------------------------

INPUT_FILE = "data/processed/hyderabad_rainfall_features_2022.csv"


def calculate_risk(rainfall_24h, rainfall_3day, rainfall_7day):
    """
    Calculate rainfall-based urban flood risk.

    Uses the same percentile thresholds learned
    from the real 2022 Hyderabad rainfall dataset.
    """

    df = pd.read_csv(INPUT_FILE)

    columns = [
        "rainfall_24h_mm",
        "rainfall_3day_mm",
        "rainfall_7day_mm"
    ]

    components = []

    values_to_predict = [
        rainfall_24h,
        rainfall_3day,
        rainfall_7day
    ]

    for column, value in zip(columns, values_to_predict):

        historical_values = df[column].astype(float).to_numpy()

        low = np.percentile(historical_values, 5)
        high = np.percentile(historical_values, 95)

        if high == low:
            normalized = 0
        else:
            normalized = (value - low) / (high - low)

        normalized = np.clip(normalized, 0, 1)

        components.append(normalized)

    # Same weights used in Step 8
    risk_score = (
        0.50 * components[0] +
        0.30 * components[1] +
        0.20 * components[2]
    ) * 100

    risk_score = round(float(risk_score), 2)

    if risk_score < 25:
        risk_level = "LOW"
    elif risk_score < 50:
        risk_level = "MODERATE"
    elif risk_score < 75:
        risk_level = "HIGH"
    else:
        risk_level = "VERY HIGH"

    return risk_score, risk_level


# ---------------------------------------------------------
# Test prediction
# ---------------------------------------------------------

print()
print("==============================================")
print("HYDERABAD URBAN FLOOD NOWCAST")
print("Step 9 - Prediction Test")
print("==============================================")

# Example rainfall values
rainfall_24h = 40.0
rainfall_3day = 80.0
rainfall_7day = 120.0

score, level = calculate_risk(
    rainfall_24h,
    rainfall_3day,
    rainfall_7day
)

print()
print("Input rainfall:")
print(f"24-hour rainfall : {rainfall_24h} mm")
print(f"3-day rainfall   : {rainfall_3day} mm")
print(f"7-day rainfall   : {rainfall_7day} mm")

print()
print("Prediction:")
print(f"Risk score       : {score}/100")
print(f"Risk level       : {level}")

print()
print("==============================================")