import uuid as uuid_mod
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

CITIES = ['New York', 'Chicago', 'Los Angeles', 'Houston', 'Phoenix', 'Seattle']

def generate_events(num_events):
    events = []
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

        # Generate a random UUID
        uuid = str(uuid_mod.uuid4())

        event = {
            'city': city,
            'start': start,
            'end': end,
            'lon': lon,
            'lat': lat,
            'uuid': uuid
        }

        events.append(event)

    return events


# Longitude and latitude bounds for each city
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

# Generate 1000 events
events = generate_events(1000)

# View the first 5 event records
print(events[:5])
