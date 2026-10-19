import xarray as xr
import pandas as pd
import glob
import os

# Hyderabad Uppal location
HYD_LAT = 17.4065
HYD_LON = 78.5522

# Path to your downloaded files
files = glob.glob("../data/raw/RF25_*.nc")
print(f"Found files: {files}")

all_df = []
for f in files:
    print(f"Reading {f}...")
    ds = xr.open_dataset(f)
    # IMD files use variable name 'rainfall' or 'rf'
    # Check variable names
    print("Variables:", list(ds.data_vars))
    
    # Extract nearest grid to Hyderabad
    # ds coords are lat, lon
    hyd_data = ds.sel(lat=HYD_LAT, lon=HYD_LON, method='nearest')
    df = hyd_data.to_dataframe().reset_index()
    df['source_file'] = os.path.basename(f)
    all_df.append(df)

final_df = pd.concat(all_df, ignore_index=True)

# Keep only important cols
# IMD daily file has 'time' and 'rainfall'
final_df['date'] = pd.to_datetime(final_df['time'])
final_df = final_df[['date','lat','lon','rainfall','source_file']].sort_values('date')

# Save real CSV
os.makedirs("../data/processed", exist_ok=True)
final_df.to_csv("../data/processed/hyderabad_daily_rainfall_2022-2024.csv", index=False)

print("\n--- SUCCESS ---")
print(final_df.head())
print(final_df.tail())
print(f"Total days: {len(final_df)}")
print(f"Max rainfall day: {final_df.loc[final_df['rainfall'].idxmax()]}")
print("Saved to: data/processed/hyderabad_daily_rainfall_2022-2024.csv")