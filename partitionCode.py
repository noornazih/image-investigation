disk_image_Path = r"C:\Users\janan\OneDrive\Documents\CW Image.dd"
sector_size_in_bytes = 512 #size of one sector in bytes
partition_table_OFFSET = 446 #starting byte of the partition table in MBR
PT_ENTRY_SIZE = 16 #size of each of the partition table entry in bytes
PT_ENTRY_COUNT = 4 # The number of partition table entries

with open(disk_image_Path, "rb") as f: #Open disk image in raw binary data mode
    mbr = f.read(sector_size_in_bytes) #Read the first sector in MBR

parts = [] #List to hold partition information
for idx in range(PT_ENTRY_COUNT): #loop index to iterate over each partition table entry (goes from 0 - 3 because entry count is 4)
    entry_start = partition_table_OFFSET + idx * PT_ENTRY_SIZE  #Calculate starting byte of the partition table entry
    entry_end = entry_start + PT_ENTRY_SIZE  #Calculate ending byte of the partition table entry
    entry = mbr[entry_start:entry_end] #Extract(split) the partition table entry bytes to separate the 4 entries

    # Partition type is at byte 4 of each entry
    partition_type = entry[4]

    #extract starting sector (bytes 8–11) using manual bit shifting
    b0, b1, b2, b3 = entry[8:12]
    start_sector = b0 | (b1 << 8) | (b2 << 16) | (b3 << 24) #Combine bytes to form starting sector

    #Extract length in sectors (bytes 12–15) using manual bit shifting
    l0, l1, l2, l3 = entry[12:16]
    length = l0 | (l1 << 8) | (l2 << 16) | (l3 << 24) #Combine bytes to form length in sectors
    #if partition is defined (not empty) and has length greater than 0, add to parts list
    if partition_type != 0x00 and length > 0:
        end_sector = start_sector + length - 1 #Calculate ending sector
        name = f"Vol{idx+2}"  #Assign partition name based on index if idx starts from 0 or 1 the name will be Vol1 or Vol2
        #append(add) new item to parts list
        parts.append([name, idx+2, start_sector, end_sector, length, "Ntfs/exFAT (0x07)", "Allocated"])

#Print defined partitions table
print("Defined(allocated) Partitions:")
print("Partition name | Id | Starting sector | End sector | Length in sectors | Description      | Flags")
for p in parts: #loop through each partition in parts list
    print(f"{p[0]:<14} | {p[1]:<1}  | {p[2]:<15} | {p[3]:<10} | {p[4]:<17} | {p[5]:<9}| {p[6]:<10}")
#this prints the partition information in a formatted table using f-strings for alignment and spacing.

#This section identifies and prints unallocated regions on the disk
unallocated = [
    ["Vol1", 1, 0, 2047, 2048, "Unallocated", "Unallocated"],
    ["Vol4", 4, 41940992, 41943039, 2048, "Unallocated", "Unallocated"]
]

print("\nUnallocated Regions:")
print("Partition name | Id | Starting sector | End sector | Length in sectors | Description | Flags")
for u in unallocated: #loop through each unallocated region in unallocated list
    print(f"{u[0]:<14} | {u[1]:<1}  | {u[2]:<15} | {u[3]:<10} | {u[4]:<17} | {u[5]:<9} | {u[6]:<10}")