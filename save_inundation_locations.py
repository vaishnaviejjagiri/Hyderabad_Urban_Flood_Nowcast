import requests
import csv
from pathlib import Path

URL = "https://tgrac.telangana.gov.in/arcgis/rest/services/GHMCNalas_Folder/GHMCNalas_vul/MapServer/1/query"

params = {
    "where": "1=1",
    "outFields": "Name,FolderPath,SymbolID",
    "returnGeometry": "true",
    "outSR": "4326",
    "f": "json"
}

response = requests.get(URL, params=params, timeout=30)
response.raise_for_status()

data = response.json()
features = data.get("features", [])

output = Path("data/processed/hyderabad_inundation_locations.csv")
output.parent.mkdir(parents=True, exist_ok=True)

with open(output, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "location_name",
        "latitude",
        "longitude",
        "source_type"
    ])

    for feature in features:
        attrs = feature.get("attributes", {})
        geometry = feature.get("geometry", {})

        writer.writerow([
            attrs.get("Name"),
            geometry.get("y"),
            geometry.get("x"),
            "Official TGRAC/GHMC waterlogging location"
        ])

print("========== SAVING OFFICIAL DATA ==========")
print("Records saved:", len(features))
print("Output:", output)
print("==========================================")