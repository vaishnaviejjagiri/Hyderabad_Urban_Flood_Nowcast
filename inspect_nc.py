from pathlib import Path

file_path = Path("data/raw/RF25_ind2022_rfp25.nc")

with open(file_path, "rb") as f:
    data = f.read(20000)

print("File size:", file_path.stat().st_size)
print("\nFirst 2000 bytes:")
print(data[:2000])