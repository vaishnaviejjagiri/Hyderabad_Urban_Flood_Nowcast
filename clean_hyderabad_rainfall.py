from netCDF4 import Dataset
from pathlib import Path
import numpy as np
import pandas as pd

# --------------------------------------------------
# 1. REAL NETCDF FILE
# --------------------------------------------------

file = Path("data/raw/RF25_ind2022_rfp25.nc")

# Hyderabad approximate coordinates
HYDERABAD_LAT = 17.3850
HYDERABAD_LON = 78.4867

# --------------------------------------------------
# 2. OPEN REAL DATA
# --------------------------------------------------

with Dataset(file, "r") as nc:

    latitude = nc.variables["LATITUDE"][:]
    longitude = nc.variables["LONGITUDE"][:]
    time = nc.variables["TIME"][:]
    rainfall = nc.variables["RAINFALL"][:]

    # Convert masked array to normal array
    rainfall = np.ma.filled(rainfall, np.nan)

    # --------------------------------------------------
    # 3. FIND NEAREST GRID CELL TO HYDERABAD
    # --------------------------------------------------

    lat_index = np.abs(latitude - HYDERABAD_LAT).argmin()
    lon_index = np.abs(longitude - HYDERABAD_LON).argmin()

    selected_lat = latitude[lat_index]
    selected_lon = longitude[lon_index]

    print("========== HYDERABAD GRID ==========")

    print("Target latitude :", HYDERABAD_LAT)
    print("Target longitude:", HYDERABAD_LON)

    print("Selected latitude :", selected_lat)
    print("Selected longitude:", selected_lon)

    print("Latitude index :", lat_index)
    print("Longitude index:", lon_index)

    # --------------------------------------------------
    # 4. EXTRACT RAINFALL FOR THAT GRID CELL
    # --------------------------------------------------

    hyderabad_rainfall = rainfall[:, lat_index, lon_index]

    print("\n========== RAINFALL ==========")

    print("Number of daily records:", len(hyderabad_rainfall))

    print("Minimum rainfall:",
          np.nanmin(hyderabad_rainfall))

    print("Maximum rainfall:",
          np.nanmax(hyderabad_rainfall))

    # --------------------------------------------------
    # 5. CONVERT TIME
    # --------------------------------------------------

    from netCDF4 import num2date

    time_dates = num2date(
        time,
        nc.variables["TIME"].units
    )

    dates = [
        date.strftime("%Y-%m-%d")
        for date in time_dates
    ]

# --------------------------------------------------
# 6. CREATE CLEAN DATAFRAME
# --------------------------------------------------

df = pd.DataFrame({
    "date": dates,
    "latitude": selected_lat,
    "longitude": selected_lon,
    "rainfall_mm": hyderabad_rainfall
})

# Remove missing rainfall records
df = df.dropna(subset=["rainfall_mm"])

# Reset index
df = df.reset_index(drop=True)

print("\n========== CLEAN DATA ==========")

print("Rows:", len(df))
print("\nFirst 10 rows:")
print(df.head(10))

print("\nLast 10 rows:")
print(df.tail(10))

print("\nMissing values:")
print(df.isna().sum())

# --------------------------------------------------
# 7. SAVE CLEAN DATA
# --------------------------------------------------

output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "hyderabad_rainfall_2022.csv"

df.to_csv(output_file, index=False)

print("\n========== COMPLETE ==========")
print("Clean file saved to:")
print(output_file)