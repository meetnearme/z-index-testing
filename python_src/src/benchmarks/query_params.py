point_query_params = [
    {'lon': -73.98517, 'lat': 40.74921},  # New York
    {'lon': -87.63241, 'lat': 41.88425},  # Chicago
    {'lon': -118.24368, 'lat': 34.05223},  # Los Angeles
    {'lon': -95.36327, 'lat': 29.76328},  # Houston
    {'lon': -112.07404, 'lat': 33.44838},  # Phoenix
    {'lon': -122.33207, 'lat': 47.60621},  # Seattle
]

range_query_params = [
    {
        'min_lat': 40.5, 'max_lat': 41.2,
        'min_lon': -74.5, 'max_lon': -73.5
    },  # New York
    {
        'min_lat': 41.5, 'max_lat': 42.0,
        'min_lon': -88.0, 'max_lon': -87.5
    },  # Chicago
    {
        'min_lat': 33.5, 'max_lat': 34.5,
        'min_lon': -118.5, 'max_lon': -118.0
    },  # Los Angeles
    {
        'min_lat': 29.45, 'max_lat': 30.0,
        'min_lon': -95.75, 'max_lon': -95.25
    },  # Houston
    {
        'min_lat': 33.0, 'max_lat': 34.0,
        'min_lon': -112.5, 'max_lon': -111.5
    },  # Phoenix
    {
        'min_lat': 47.0, 'max_lat': 48.0,
        'min_lon': -122.75, 'max_lon': -121.5
    },  # Seattle
]

temporal_query_params = [
    {
        'start_time': '2024-06-01T00:00:00',
        'end_time': '2024-09-01T23:59:59'
    },  # Full three-month range
    {
        'start_time': '2024-06-15T00:00:00',
        'end_time': '2024-06-30T23:59:59'
    },  # Second half of June
    {
        'start_time': '2024-07-01T00:00:00',
        'end_time': '2024-07-31T23:59:59'
    },  # Full month of July
    {
        'start_time': '2024-08-01T00:00:00',
        'end_time': '2024-08-15T23:59:59'
    },  # First half of August
]
