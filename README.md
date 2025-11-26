Code explanation: 

The partition table is stored in the MBR (Master Boot Record), which is located in the first 512 bytes of the disk. This is called the sector size.
It includes:
- The partition table offset: the first 446 bytes
- The partition table (4 entries describing the partition size and type, 16 bytes each)
This code reads the first 512 bytes of the disk image, extracts (splits), and decodes the four partition entries:
- Partition ID (number)
- Starting sector (where the partition starts)
- Size in sectors
- The file system type (0x07 = NTFS/exFAT or undefined/empty = 0x00)

The raw image.dd shows 4 volumes:
- Vol1 – unallocated space (0–2047 sectors)
- Vol2 – NTFS/exFAT partition (2048–206847)
- Vol3 – NTFS/exFAT partition (206848–41940991)
- Vol4 – unallocated space (41940992–41943039)

Only Vol2 and Vol3 are real partitions defined in the MBR. Vol1 and Vol4 are unallocated and undefined regions. Vol1 is invisible to the operating system; it can be hidden since it is not assigned to any active partition. However, it may contain deleted files. Moreover, the disk has 2 partitions and 2 unallocated regions.

The start sector (bytes 8–11) and the partition length (bytes 12–15) were added. Because the data is stored in little‑endian format (from the least significant bit), manual bit shifting was used instead of importing libraries to combine the bytes into proper 32‑bit numbers. The end sector was then calculated as start + length – 1, which avoids counting one sector too many. To keep the output consistent with Autopsy, f‑strings were used to automatically name the partitions (Vol2, Vol3). Finally, each partition’s details — name, number, start, end, length, type, and status — were added into a list that was displayed or formatted as a table. This produced a clear partition map that matched Autopsy’s results, showing both accuracy and proper forensic validation.
