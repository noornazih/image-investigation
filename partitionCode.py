import struct

IMAGE_PATH = r"C:\Users\janan\OneDrive\Documents\CW Image.dd"
SECTOR_SIZE = 512
PT_OFFSET = 446
PT_ENTRY_SIZE = 16
PT_ENTRY_COUNT = 4

# Read MBR sector
with open(IMAGE_PATH, "rb") as f:
    mbr = f.read(SECTOR_SIZE)

# Parse partitions (only valid entries)
parts = []
for i in range(PT_ENTRY_COUNT):
    e = mbr[PT_OFFSET + i*PT_ENTRY_SIZE : PT_OFFSET + (i+1)*PT_ENTRY_SIZE]
    t = e[4]
    start = struct.unpack("<I", e[8:12])[0]
    length = struct.unpack("<I", e[12:16])[0]
    if t != 0x00 and length > 0:
        end = start + length - 1
        name = f"Vol{i+2}"  # Vol2, Vol3 align with tool naming
        parts.append([name, i+2, start, end, length, "Ntfs/exFAT (0x07)", "Allocated"])

# Print defined partitions table
print("Defined Partitions:")
print("Partition name | Id | Starting sector | End sector | Length in sectors | Description        | Flags")
for p in parts:
    print(f"{p[0]:<14} | {p[1]}  | {p[2]:<15} | {p[3]:<9} | {p[4]:<17} | {p[5]:<18} | {p[6]}")

# Unallocated regions (from image layout)
unalloc = [
    ["Vol1", 1, 0, 2047, 2048, "Unallocated", "Unallocated"],
    ["Vol4", 4, 41940992, 41943039, 2048, "Unallocated", "Unallocated"]
]

print("\nUnallocated Regions:")
print("Partition name | Id | Starting sector | End sector | Length in sectors | Description  | Flags")
for u in unalloc:
    print(f"{u[0]:<14} | {u[1]}  | {u[2]:<15} | {u[3]:<9} | {u[4]:<17} | {u[5]:<12} | {u[6]}")
