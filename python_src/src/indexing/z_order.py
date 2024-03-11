import struct
from datetime import datetime

from indexing_utils import map_float_to_sortable_int

def calculate_z_order_index(start_time, lat, lon, index_type='actual'):
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

    if index_type == 'min':
        index_creation_time_bin = '0' * 32
    elif index_type == 'max':
        index_creation_time_bin = '1' * 32

    z_index_with_creation_time_bin = z_index_bin + index_creation_time_bin

    return z_index_bin
