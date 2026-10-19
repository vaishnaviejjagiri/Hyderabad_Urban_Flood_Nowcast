import json
from pathlib import Path

# Hyderabad approximate bounding box
HYD_LAT_MIN = 17.20
HYD_LAT_MAX = 17.60

HYD_LON_MIN = 78.20
HYD_LON_MAX = 78.70

file = Path("data/raw/telangana_flooding_area.geojson")

with open(file, "r", encoding="utf-8") as f:
    data = json.load(f)

features = data.get("features", [])

print("========== FLOOD AREA CHECK ==========")

print("Total official flood polygons:", len(features))

intersecting = []

for i, feature in enumerate(features):

    geometry = feature.get("geometry", {})
    coordinates = geometry.get("coordinates", [])

    if not coordinates:
        continue

    # Get all polygon coordinate points
    points = []

    for ring in coordinates:
        for point in ring:
            if len(point) >= 2:
                lon = point[0]
                lat = point[1]
                points.append((lon, lat))

    if not points:
        continue

    # Polygon bounding box
    min_lon = min(p[0] for p in points)
    max_lon = max(p[0] for p in points)
    min_lat = min(p[1] for p in points)
    max_lat = max(p[1] for p in points)

    # Check bounding-box overlap with Hyderabad
    overlaps = not (
        max_lon < HYD_LON_MIN
        or min_lon > HYD_LON_MAX
        or max_lat < HYD_LAT_MIN
        or min_lat > HYD_LAT_MAX
    )

    if overlaps:
        intersecting.append({
            "feature": i + 1,
            "min_lon": min_lon,
            "max_lon": max_lon,
            "min_lat": min_lat,
            "max_lat": max_lat
        })

print("\nFlood polygons overlapping Hyderabad area:",
      len(intersecting))

for item in intersecting:
    print("\nPolygon:", item["feature"])
    print("Longitude:", item["min_lon"], "to", item["max_lon"])
    print("Latitude :", item["min_lat"], "to", item["max_lat"])

print("\n========== COMPLETE ==========")