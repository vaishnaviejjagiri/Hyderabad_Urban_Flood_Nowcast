import json
import urllib.request
from datetime import datetime

# ============================================================
# HYDERABAD
# ============================================================

LATITUDE = 17.3850
LONGITUDE = 78.4867

# ============================================================
# OPEN-METEO FORECAST API
# Get hourly precipitation forecast
# ============================================================

url = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=17.3850"
    "&longitude=78.4867"
    "&hourly=precipitation"
    "&forecast_hours=6"
    "&timezone=Asia%2FKolkata"
)

print("=" * 60)
print("HYDERABAD 3-HOUR FLOOD FORECAST")
print("=" * 60)

try:

    with urllib.request.urlopen(url, timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))

    times = data["hourly"]["time"]
    precipitation = data["hourly"]["precipitation"]

    if len(times) < 3 or len(precipitation) < 3:
        raise ValueError("Less than 3 hours of forecast data received.")

    # --------------------------------------------------------
    # Next 3 hours
    # --------------------------------------------------------

    next_3_hours = precipitation[:3]

    total_3hour_rainfall = sum(
        value if value is not None else 0
        for value in next_3_hours
    )

    # Individual hourly rainfall
    rain_hour_1 = next_3_hours[0] or 0
    rain_hour_2 = next_3_hours[1] or 0
    rain_hour_3 = next_3_hours[2] or 0

    # --------------------------------------------------------
    # Simple 3-hour forecast risk
    #
    # This is a rainfall-based early-warning indicator.
    # It is NOT a claim of observed flooding.
    # --------------------------------------------------------

    if total_3hour_rainfall < 5:

        risk_level = "LOW"

    elif total_3hour_rainfall < 15:

        risk_level = "MODERATE"

    elif total_3hour_rainfall < 30:

        risk_level = "HIGH"

    else:

        risk_level = "VERY HIGH"

    # --------------------------------------------------------
    # Output
    # --------------------------------------------------------

    print()
    print("Forecast starting from:")
    print(times[0])

    print()

    print("Next 1 hour rainfall : "
          f"{rain_hour_1:.2f} mm")

    print("Next 2 hours rainfall: "
          f"{rain_hour_2:.2f} mm")

    print("Next 3 hours rainfall: "
          f"{rain_hour_3:.2f} mm")

    print()

    print("Total rainfall forecast for next 3 hours:")
    print(f"{total_3hour_rainfall:.2f} mm")

    print()

    print("3-HOUR-AHEAD RAINFALL RISK:")
    print(risk_level)

    print()

    print("=" * 60)
    print("IMPORTANT")
    print("=" * 60)

    print(
        "This forecast estimates rainfall-driven urban flood risk."
    )

    print(
        "It does NOT mean flooding is guaranteed to occur."
    )

    print("=" * 60)

except Exception as error:

    print()
    print("ERROR:")
    print(error)