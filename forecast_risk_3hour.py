import requests
from datetime import datetime

LATITUDE = 17.3850
LONGITUDE = 78.4867

print("=" * 65)
print("HYDERABAD URBAN FLOOD - 3 HOUR AHEAD RISK")
print("=" * 65)

try:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}"
        f"&longitude={LONGITUDE}"
        "&hourly=precipitation"
        "&past_days=7"
        "&forecast_days=2"
        "&timezone=Asia%2FKolkata"
    )

    response = requests.get(url, timeout=20)
    response.raise_for_status()
    data = response.json()

    times = data["hourly"]["time"]
    rainfall = data["hourly"]["precipitation"]

    current_time = datetime.now().strftime("%Y-%m-%dT%H:00")

    # Find the current hour in the forecast timeline
    if current_time in times:
        index = times.index(current_time)
    else:
        index = next(
            (i for i, t in enumerate(times) if t >= current_time),
            None
        )

    if index is None or index + 2 >= len(rainfall):
        raise ValueError("Three forecast hours are unavailable.")

    forecast_values = [
        float(rainfall[index + i] or 0)
        for i in range(3)
    ]

    # Previous 24 hours of rainfall
    recent_values = rainfall[max(0, index - 24):index]
    rainfall_24h = sum(float(v or 0) for v in recent_values)

    # Total forecast rainfall for the next 3 hours
    forecast_3h = sum(forecast_values)

    # Combined rainfall indicator
    combined_rainfall = rainfall_24h + forecast_3h

    # Calculate rainfall-based risk score
    risk_score = min(100, (combined_rainfall / 40) * 100)

    if combined_rainfall < 10:
        risk_level = "LOW"
    elif combined_rainfall < 25:
        risk_level = "MODERATE"
    elif combined_rainfall < 50:
        risk_level = "HIGH"
    else:
        risk_level = "VERY HIGH"

    print("\nWeather data source: Open-Meteo")
    print("Location: Hyderabad, Telangana")
    print(f"\nCurrent hour: {times[index]}")

    print("\nNext 3 forecast hours:")
    for i, value in enumerate(forecast_values, start=1):
        print(f"{times[index + i - 1]}: {value:.2f} mm")

    print(f"\nRecent 24-hour rainfall: {rainfall_24h:.2f} mm")
    print(f"Next 3-hour forecast rainfall: {forecast_3h:.2f} mm")
    print(f"Combined rainfall indicator: {combined_rainfall:.2f} mm")

    print(f"\n3-HOUR-AHEAD RISK SCORE: {risk_score:.2f}/100")
    print(f"3-HOUR-AHEAD RISK LEVEL: {risk_level}")

    if risk_level == "VERY HIGH":
        print("\nWARNING: Very high rainfall-based risk indicator.")
    elif risk_level == "HIGH":
        print("\nWARNING: High rainfall-based risk indicator.")
    elif risk_level == "MODERATE":
        print("\nCAUTION: Continue monitoring rainfall conditions.")
    else:
        print("\nNORMAL: Low rainfall-based risk indicator.")

    print("=" * 65)
    print(
        "NOTE: This is an experimental rainfall-based indicator, "
        "not a confirmed street-level flood prediction."
    )
    print("=" * 65)

except Exception as error:
    print("\nERROR: Unable to calculate the 3-hour risk.")
    print("Details:", error)