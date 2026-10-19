import requests

url = (
    "https://tgrac.telangana.gov.in/arcgis/rest/services/"
    "TCUR_Folder/TCUR_Telangana_Core_Urban_Region_V2/"
    "MapServer/89"
)

params = {
    "f": "json"
}

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()

data = response.json()

print("========== OFFICIAL FLOODING AREA LAYER ==========")

print("Layer name:")
print(data.get("name"))

print("\nGeometry type:")
print(data.get("geometryType"))

print("\nDescription:")
print(data.get("description"))

print("\nSpatial reference:")
print(data.get("spatialReference"))

print("\n========== FIELDS ==========")

for field in data.get("fields", []):
    print(
        field.get("name"),
        "|",
        field.get("type"),
        "|",
        field.get("alias")
    )

print("\n========== EXTENT ==========")

print(data.get("extent"))

print("\n========== COMPLETE ==========")