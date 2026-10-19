def calculate_risk(recent_24h, next_3h):

    combined = recent_24h + next_3h

    if combined < 10:
        score = (combined / 10) * 25
        level = "LOW"

    elif combined < 25:
        score = 25 + ((combined - 10) / 15) * 25
        level = "MODERATE"

    elif combined < 50:
        score = 50 + ((combined - 25) / 25) * 25
        level = "HIGH"

    else:
        score = 75 + min(
            25,
            ((combined - 50) / 50) * 25
        )
        level = "VERY HIGH"

    return score, level


tests = [
    ("LOW rainfall", 2, 1),
    ("MODERATE rainfall", 10, 8),
    ("HIGH rainfall", 20, 20),
    ("VERY HIGH rainfall", 40, 30)
]


print("=" * 60)
print("3-HOUR FLOOD RISK MODEL TEST")
print("=" * 60)

for name, recent, forecast in tests:

    score, level = calculate_risk(
        recent,
        forecast
    )

    print()
    print(name)
    print("Recent 24h rainfall:", recent, "mm")
    print("Next 3h rainfall:", forecast, "mm")
    print("Risk score:", round(score, 2), "/100")
    print("Risk level:", level)

print()
print("=" * 60)
print("MODEL TEST COMPLETED")
print("=" * 60)