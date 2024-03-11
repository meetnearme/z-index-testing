import struct
from datetime import datetime

def map_float_to_sortable_int(float_value):
    """
    Maps a floating-point value to an unsigned integer that can be lexicographically sorted
    """
    float_bytes = struct.pack('>f', float_value)

    # apply mapping function
    if float_value >= 0:
        # XOR operation for flipping first bit to make unsigned integer representation of positive float come after negative
        sortable_bytes = bytes([(float_bytes[0] ^ 0x80)] + list(float_bytes[1:]))
    else:
        # XOR to flip all bits, to make negative floats come first from lowest to highest in unsigned integer representation
        sortable_bytes = bytes([b ^ 0xFF for b in float_bytes])

    # convert mapped bytes to an unsigned integer
    sortable_int = int.from_bytes(sortable_bytes, byteorder='big', signed=False)

    return sortable_int


def calculate_z_order_index(start_time, lon, lat):
    # Get current timestamp as index creation time
    index_creation_time_bin = bin(int(datetime.now().timestamp()))[2:].zfill(32)

    # Convert dimensions to binary representations
    start_time_bin = bin(int(start_time.timestamp()))[2:].zfill(32)

    # Map floating point values to sortable unsigned integers
    lon_sortable_int = map_float_to_sortable_int(lon)
    lat_sortable_int = map_float_to_sortable_int(lat)
    
    # Convert sortable integers to binary string
    lon_bin = bin(lon_sortable_int)[2:].zfill(32)
    lat_bin = bin(lat_sortable_int)[2:].zfill(32)

    # Convert the index creation time to binary string

    # interleave binary representations
    z_index_bin = ''.join(
            start_time_bin[i:i+1] + lon_bin[i:i+1] + lat_bin[i:i+1]
            for i in range(0, 32, 1)
    )

    z_index_with_creation_time_bin = z_index_bin + index_creation_time_bin

    return z_index_bin
