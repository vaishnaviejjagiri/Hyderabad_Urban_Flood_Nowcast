from netCDF4 import Dataset
from pathlib import Path

# Real NetCDF file
file = Path("data/raw/RF25_ind2022_rfp25.nc")

print("Opening real NetCDF file...")
print("File:", file)
print("Exists:", file.exists())
print("Size:", file.stat().st_size, "bytes")

# Open NetCDF file
with Dataset(file, "r") as nc:

    print("\n========== DIMENSIONS ==========")

    for name, dimension in nc.dimensions.items():
        print(name, "=", len(dimension))

    print("\n========== VARIABLES ==========")

    for name, variable in nc.variables.items():
        print(
            name,
            "| shape =", variable.shape,
            "| dtype =", variable.dtype
        )

    print("\n========== VARIABLE DETAILS ==========")

    for name, variable in nc.variables.items():
        print("\nVariable:", name)
        print("Dimensions:", variable.dimensions)
        print("Shape:", variable.shape)

        if hasattr(variable, "units"):
            print("Units:", variable.units)

        if hasattr(variable, "long_name"):
            print("Long name:", variable.long_name)

    print("\n========== SAMPLE VALUES ==========")

    # Longitude
    longitude = nc.variables["LONGITUDE"][:]
    print("\nLONGITUDE first 10:")
    print(longitude[:10])

    # Latitude
    latitude = nc.variables["LATITUDE"][:]
    print("\nLATITUDE first 10:")
    print(latitude[:10])

    # Time
    time = nc.variables["TIME"][:]
    print("\nTIME first 10:")
    print(time[:10])

    # Rainfall
    rainfall = nc.variables["RAINFALL"][:]

    print("\nRAINFALL shape:")
    print(rainfall.shape)

    print("\nRAINFALL first values:")
    print(rainfall.flatten()[:20])

    print("\nRAINFALL minimum:")
    print(rainfall.min())

    print("\nRAINFALL maximum:")
    print(rainfall.max())

print("\n========== INSPECTION COMPLETE ==========")