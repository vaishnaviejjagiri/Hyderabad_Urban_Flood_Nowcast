import requests
import json
from pathlib import Path

URL = (
    "https://tgrac.telangana.gov.in/arcgis/rest/services/"
    "TCUR_Folder/TCUR_Telangana_Core_Urban_Region_V2/"
    "MapServer/89/query"
)

params = {
    "where": "1=1",
    "outFields": "OBJECTID,Flood,Shape_Area",
    "returnGeometry": "true",
    "outSR": "4326",
    "f": "json"
}

print("Downloading official Telangana Flooding Area data...")

response = requests.get(
    URL,
    params=params,
    timeout=60
)

print("HTTP status:", response.status_code)

response.raise_for_status()

data = response.json()

# Check for ArcGIS error response
if "error" in data:
    print("\nArcGIS returned an error:")
    print(data["error"])
    raise SystemExit(1)

features = data.get("features", [])

print("Download successful.")
print("Number of flood polygons:", len(features))

# Convert ArcGIS JSON to GeoJSON
geojson = {
    "type": "FeatureCollection",
    "features": []
}

for feature in features:

    attributes = feature.get("attributes", {})
    geometry = feature.get("geometry")

    if geometry is None:
        continue

    # ArcGIS polygon geometry
    rings = geometry.get("rings", [])

    geojson["features"].append({
        "type": "Feature",
        "properties": attributes,
        "geometry": {
            "type": "Polygon",
            "coordinates": rings
        }
    })

# Create output directory
output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "telangana_flooding_area.geojson"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(geojson, f, indent=2)

print("\nSaved official flood data to:")
print(output_file)

print("\nSaved features:", len(geojson["features"]))

print("\n========== COMPLETE ==========")