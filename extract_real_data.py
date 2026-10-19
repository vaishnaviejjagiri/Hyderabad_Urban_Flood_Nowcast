import struct
from pathlib import Path

FILE = Path("data/raw/RF25_ind2022_rfp25.nc")


def read_i32(f):
    data = f.read(4)
    if len(data) != 4:
        raise EOFError("Unexpected end of file while reading int32")
    return struct.unpack(">i", data)[0]


def read_u32(f):
    data = f.read(4)
    if len(data) != 4:
        raise EOFError("Unexpected end of file while reading uint32")
    return struct.unpack(">I", data)[0]


def read_i64(f):
    data = f.read(8)
    if len(data) != 8:
        raise EOFError("Unexpected end of file while reading int64")
    return struct.unpack(">q", data)[0]


def read_name(f):
    n = read_u32(f)
    data = f.read(n)

    if len(data) != n:
        raise EOFError("Unexpected end of file while reading name")

    padding = (4 - (n % 4)) % 4
    if padding:
        f.read(padding)

    return data.decode("ascii", errors="replace")


def read_attrs(f):
    tag = read_u32(f)

    # NC_ATTRIBUTE = 12
    if tag == 0:
        return {}

    if tag != 12:
        raise ValueError(f"Unexpected attribute tag: {tag}")

    count = read_u32(f)
    attrs = {}

    for _ in range(count):

        name = read_name(f)
        xtype = read_i32(f)
        n = read_u32(f)

        if xtype == 1:          # BYTE
            raw = f.read(n)
            value = raw

        elif xtype == 2:        # CHAR
            raw = f.read(n)
            value = raw.decode("ascii", errors="replace")

        elif xtype == 3:        # SHORT
            raw = f.read(2 * n)
            value = struct.unpack(">" + "h" * n, raw)

        elif xtype == 4:        # INT
            raw = f.read(4 * n)
            value = struct.unpack(">" + "i" * n, raw)

        elif xtype == 5:        # FLOAT
            raw = f.read(4 * n)
            value = struct.unpack(">" + "f" * n, raw)

        elif xtype == 6:        # DOUBLE
            raw = f.read(8 * n)
            value = struct.unpack(">" + "d" * n, raw)

        else:
            raise ValueError(f"Unknown NetCDF data type: {xtype}")

        # Values are padded to a 4-byte boundary.
        size = {
            1: n,
            2: n,
            3: 2 * n,
            4: 4 * n,
            5: 4 * n,
            6: 8 * n
        }[xtype]

        padding = (4 - (size % 4)) % 4

        if padding:
            f.read(padding)

        attrs[name] = value

    return attrs


with open(FILE, "rb") as f:

    # --------------------------------
    # File format
    # --------------------------------
    magic = f.read(4)

    print("File format:", magic)

    if magic != b"CDF\x01":
        raise ValueError("This script expects NetCDF classic CDF-1.")

    num_records = read_u32(f)

    print("Number of records:", num_records)

    # --------------------------------
    # Dimensions
    # --------------------------------
    dim_tag = read_u32(f)

    print("Dimension tag:", dim_tag)

    dimensions = []

    if dim_tag == 0:
        print("No dimensions.")

    elif dim_tag == 10:

        number_dimensions = read_u32(f)

        print("Number of dimensions:", number_dimensions)

        for _ in range(number_dimensions):

            name = read_name(f)
            length = read_u32(f)

            dimensions.append((name, length))

    else:
        raise ValueError("Invalid dimension list.")

    # --------------------------------
    # Global attributes
    # --------------------------------
    global_attributes = read_attrs(f)

    # --------------------------------
    # Variables
    # --------------------------------
    var_tag = read_u32(f)

    print("Variable tag:", var_tag)

    variables = []

    if var_tag == 0:

        print("No variables.")

    elif var_tag == 11:

        number_variables = read_u32(f)

        print("Number of variables:", number_variables)

        for _ in range(number_variables):

            name = read_name(f)

            number_dimensions = read_u32(f)

            dimension_ids = []

            for _ in range(number_dimensions):
                dimension_ids.append(read_u32(f))

            attributes = read_attrs(f)

            vsize = read_u32(f)

            # CDF-1 uses a 4-byte begin offset.
            begin = read_u32(f)

            variables.append({
                "name": name,
                "dimension_ids": dimension_ids,
                "attributes": attributes,
                "vsize": vsize,
                "begin": begin
            })

    else:
        raise ValueError("Invalid variable list.")

print()
print("=" * 60)
print("REAL NETCDF STRUCTURE")
print("=" * 60)

print("\nDIMENSIONS")

for i, (name, length) in enumerate(dimensions):
    print(f"  ID {i}: {name} = {length}")

print("\nVARIABLES")

for variable in variables:

    print()
    print("  Name:", variable["name"])
    print("  Dimension IDs:", variable["dimension_ids"])
    print("  Variable size:", variable["vsize"])
    print("  Data begins at byte:", variable["begin"])

    print("  Attributes:")

    for name, value in variable["attributes"].items():
        print(f"    {name}: {value}")

print()
print("=" * 60)
print("IMPORTANT VARIABLES")
print("=" * 60)

for variable in variables:

    if variable["name"] in [
        "LONGITUDE",
        "LATITUDE",
        "TIME",
        "RAINFALL"
    ]:

        print()
        print(variable["name"])

        print("  Dimension IDs:",
              variable["dimension_ids"])

        for name, value in variable["attributes"].items():
            print(f"  {name}: {value}")

print()
print("=" * 60)
print("INSPECTION COMPLETE")
print("=" * 60)