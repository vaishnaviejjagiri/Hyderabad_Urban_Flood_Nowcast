import json
import urllib.parse
import urllib.request
from datetime import datetime

# ---------------------------------------------------------
# Hyderabad Urban Flood Nowcast
# Step 10 - Live Rainfall Pipeline
# ---------------------------------------------------------

LATITUDE = 17.3850
LONGITUDE = 78.4867

API_URL = "https://api.open-meteo.com/v1/forecast"


def get_live_rainfall():

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": "precipitation",
        "past_days": 7,
        "forecast_days": 1,
        "timezone": "Asia/Kolkata"
    }

    url = API_URL + "?" + urllib.parse.urlencode(params)

    print()
    print("Connecting to live rainfall data...")
    print("Source: Open-Meteo")
    print(f"Location: Hyderabad ({LATITUDE}, {LONGITUDE})")

    with urllib.request.urlopen(url, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))

    times = data["hourly"]["time"]
    precipitation = data["hourly"]["precipitation"]

    records = []

    for time_value, rainfall_value in zip(times, precipitation):

        if rainfall_value is None:
            rainfall_value = 0.0

        records.append({
            "time": time_value,
            "rainfall_mm": float(rainfall_value)
        })

    return records


def calculate_rainfall_windows(records):

    rainfall_values = [
        record["rainfall_mm"]
        for record in records
    ]

    # Last 24 hourly observations
    rainfall_24h = sum(rainfall_values[-24:])

    # Last 72 hourly observations
    rainfall_3day = sum(rainfall_values[-72:])

    # Last 168 hourly observations
    rainfall_7day = sum(rainfall_values[-168:])

    return rainfall_24h, rainfall_3day, rainfall_7day


def calculate_risk(rainfall_24h, rainfall_3day, rainfall_7day):

    # Thresholds based on the real 2022 Hyderabad
    # rainfall dataset used in Step 8.

    thresholds = {
        "rainfall_24h_mm": (0.0, 95.0),
        "rainfall_3day_mm": (0.0, 70.0),
        "rainfall_7day_mm": (0.0, 100.0)
    }

    values = [
        rainfall_24h,
        rainfall_3day,
        rainfall_7day
    ]

    components = []

    for value, key in zip(values, thresholds):

        low, high = thresholds[key]

        if high == low:
            normalized = 0.0
        else:
            normalized = (value - low) / (high - low)

        normalized = max(0.0, min(1.0, normalized))

        components.append(normalized)

    risk_score = (
        0.50 * components[0] +
        0.30 * components[1] +
        0.20 * components[2]
    ) * 100

    risk_score = round(risk_score, 2)

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
# Main program
# ---------------------------------------------------------

print()
print("==============================================")
print("HYDERABAD URBAN FLOOD NOWCAST")
print("STEP 10 - LIVE RAINFALL")
print("==============================================")

try:

    records = get_live_rainfall()

    rainfall_24h, rainfall_3day, rainfall_7day = (
        calculate_rainfall_windows(records)
    )

    risk_score, risk_level = calculate_risk(
        rainfall_24h,
        rainfall_3day,
        rainfall_7day
    )

    print()
    print("Latest rainfall windows:")
    print(f"24-hour rainfall : {rainfall_24h:.2f} mm")
    print(f"3-day rainfall   : {rainfall_3day:.2f} mm")
    print(f"7-day rainfall   : {rainfall_7day:.2f} mm")

    print()
    print("NOWCAST RESULT")
    print("----------------------------------------------")
    print(f"Risk score       : {risk_score}/100")
    print(f"Risk level       : {risk_level}")

    print()
    print("Last available observation:")
    print(f"Time             : {records[-1]['time']}")
    print(f"Rainfall         : {records[-1]['rainfall_mm']:.2f} mm")

    print()
    print("==============================================")

except Exception as error:

    print()
    print("ERROR")
    print("----------------------------------------------")
    print(error)
    print()