import uuid as uuid_mod
import random
import json
import struct
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

city_lons = {
    'New York': (-74.5, -73.5),
    'Chicago': (-88.0, -87.5),
    'Los Angeles': (-118.5, -118.0),
    'Houston': (-95.75, -95.25),
    'Phoenix': (-112.5, -111.5),
    'Seattle': (-122.75, -121.5)
}

city_lats = {
    'New York': (40.5, 41.2),
    'Chicago': (41.5, 42.0),
    'Los Angeles': (33.5, 34.5),
    'Houston': (29.45, 30.0),
    'Phoenix': (33.0, 34.0),
    'Seattle': (47.0, 48.0)
}

CITIES = [
    'New York', 'Chicago', 'Los Angeles', 'Houston', 'Phoenix', 'Seattle'
]

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
    # Convert dimensions to binary representations
    start_time_bin = bin(int(start_time.timestamp()))[2:].zfill(32)

    # Map floating point values to sortable unsigned integers
    lon_sortable_int = map_float_to_sortable_int(lon)
    lat_sortable_int = map_float_to_sortable_int(lat)
    
    # Convert sortable integers to binary string
    lon_bin = bin(lon_sortable_int)[2:].zfill(32)
    lat_bin = bin(lat_sortable_int)[2:].zfill(32)

    # interleave binary representations
    z_index_bin = ''.join(
            start_time_bin[i:i+1] + lon_bin[i:i+1] + lat_bin[i:i+1]
            for i in range(0, 32, 1)
    )

    return z_index_bin


def generate_events(num_events, output_file):
    with open(output_file, 'w') as f:
        for _ in range(num_events):
            # Randomly pick a city
            city = random.choice(CITIES)

            # Randomly generate longitude and latitude within ranges
            # approximating the city's geographic area
            lon = random.uniform(city_lons[city][0], city_lons[city][1])
            lat = random.uniform(city_lats[city][0], city_lats[city][1])

            # Randomly generate start date within the past year
            # start = fake.date_time_between(start_date='-1y', end_date='now')

            # Randomly choose event duration between 1 to 8 hours
            # duration = random.randint(1, 8)
            # end = start + timedelta(hours=duration)

            # set fixed start date and duration
            start = datetime(2024, 6, 1, 12, 0, 0)
            duration = 3
            end = start + timedelta(hours=duration)

            # generate random name and description
            name = fake.sentence(nb_words=4)
            description = fake.paragraph(nb_sentences=5)

            # Generate a random UUID
            uuid = str(uuid_mod.uuid4())

            # Calculate z order index
            z_order_index = calculate_z_order_index(start, lon, lat)

            event = {
                'city': city,
                'start_time': start.isoformat(),
                'end_time': end.isoformat(),
                'lon': lon,
                'lat': lat,
                'uuid': str(uuid),
                'name': name,
                'description': description,
                'z_order_index': z_order_index
            }

            event_json = json.dumps(event)
            f.write(event_json + '\n')


# Longitude and latitude bounds for each city


# Generate 1000 events
events = generate_events(1000, 'events.json')
