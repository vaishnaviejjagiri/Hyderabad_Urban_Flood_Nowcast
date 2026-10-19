import requests

URL = "https://tgrac.telangana.gov.in/arcgis/rest/services/GHMCNalas_Folder/GHMCNalas_vul/MapServer/1/query"

params = {
    "where": "1=1",
    "outFields": "*",
    "returnGeometry": "true",
    "outSR": "4326",
    "f": "json"
}

response = requests.get(URL, params=params, timeout=30)
response.raise_for_status()

data = response.json()

features = data.get("features", [])

print("========== OFFICIAL INUNDATION AREAS ==========")
print("Total records:", len(features))

for i, feature in enumerate(features, start=1):
    attrs = feature.get("attributes", {})
    geometry = feature.get("geometry", {})

    print("\n--------------------------------")
    print("Record:", i)

    print("Name:", attrs.get("Name"))
    print("FolderPath:", attrs.get("FolderPath"))
    print("SymbolID:", attrs.get("SymbolID"))

    print("Longitude:", geometry.get("x"))
    print("Latitude :", geometry.get("y"))

print("\n========== COMPLETE ==========")