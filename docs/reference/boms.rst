..
    This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
    Copyright 2022-2024 Kurt McKee <contactme@kurtmckee.org>
    SPDX-License-Identifier: MIT

Byte Order Marks (BOMs)
#######################

Chipshot initially reads all files as binary.
If the first bytes correspond to a known byte order mark (BOM),
Chipshot will decode the file using the encoding scheme indicated by the BOM.

The encoding associated with the BOM is always respected,
even if Chipshot is configured to expect a different encoding.
If the file cannot be decoded using the BOM-indicated encoding,
Chipshot will not try to use any other encoding.

If Chipshot updates the file, the BOM will be retained.

These are the BOMs that Chipshot understands,
and the associated encoding that will be used if a BOM is encountered.

..  csv-table::
    :header: "BOM characters", "Encoding"

    "``00 00 fe ff``", "UTF-32 (Big Endian)"
    "``ff fe 00 00``", "UTF-32 (Little Endian)"
    "``fe ff``", "UTF-16 (Big Endian)"
    "``ff fe``", "UTF-16 (Little Endian)"
    "``ef bb bf``", "UTF-8"
