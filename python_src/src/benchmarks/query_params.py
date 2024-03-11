point_query_params = [
    # New York
    {'lon': -73.98517, 'lat': 40.74921},  # Midtown Manhattan
    {'lon': -73.97968, 'lat': 40.75895},  # Upper East Side
    {'lon': -73.99045, 'lat': 40.73477},  # Greenwich Village
    {'lon': -73.94398, 'lat': 40.82828},  # Harlem
    {'lon': -73.95141, 'lat': 40.65538},  # Brooklyn Heights

    # Chicago
    {'lon': -87.63241, 'lat': 41.88425},  # The Loop
    {'lon': -87.64988, 'lat': 41.92857},  # Lincoln Park
    {'lon': -87.64724, 'lat': 41.94424},  # Wrigleyville
    {'lon': -87.72159, 'lat': 41.87897},  # Pilsen
    {'lon': -87.58659, 'lat': 41.74309},  # Hyde Park

    # Los Angeles
    {'lon': -118.24368, 'lat': 34.05223},  # Downtown LA
    {'lon': -118.32840, 'lat': 34.09834},  # Hollywood
    {'lon': -118.44150, 'lat': 34.02134},  # Santa Monica
    {'lon': -118.26627, 'lat': 34.10158},  # Griffith Park
    {'lon': -118.30490, 'lat': 33.98756},  # South LA

    # Houston
    {'lon': -95.36327, 'lat': 29.76328},  # Downtown Houston
    {'lon': -95.41074, 'lat': 29.74194},  # Montrose
    {'lon': -95.52509, 'lat': 29.65483},  # Sugar Land
    {'lon': -95.12898, 'lat': 29.55735},  # Pasadena
    {'lon': -95.62677, 'lat': 29.78772},  # Katy

    # Phoenix
    {'lon': -112.07404, 'lat': 33.44838},  # Downtown Phoenix
    {'lon': -111.92983, 'lat': 33.50905},  # Camelback East
    {'lon': -112.26468, 'lat': 33.63646},  # Deer Valley
    {'lon': -112.22149, 'lat': 33.38222},  # Ahwatukee Foothills
    {'lon': -111.90237, 'lat': 33.30728},  # South Mountain

    # Seattle
    {'lon': -122.33207, 'lat': 47.60621},  # Downtown Seattle
    {'lon': -122.32944, 'lat': 47.62535},  # Capitol Hill
    {'lon': -122.34511, 'lat': 47.65338},  # Fremont
    {'lon': -122.38506, 'lat': 47.56208},  # West Seattle
    {'lon': -122.27700, 'lat': 47.53009},  # Rainier Beach
]

range_query_params = [
    # New York
    {
        'min_lat': 40.5, 'max_lat': 41.2,
        'min_lon': -74.5, 'max_lon': -73.5
    },  # Greater New York area
    {
        'min_lat': 40.7, 'max_lat': 40.8,
        'min_lon': -74.0, 'max_lon': -73.9
    },  # Manhattan
    {
        'min_lat': 40.6, 'max_lat': 40.7,
        'min_lon': -74.0, 'max_lon': -73.9
    },  # Lower Manhattan
    {
        'min_lat': 40.7, 'max_lat': 40.8,
        'min_lon': -73.9, 'max_lon': -73.8
    },  # Upper Manhattan
    {
        'min_lat': 40.6, 'max_lat': 40.7,
        'min_lon': -73.9, 'max_lon': -73.8
    },  # Brooklyn

    # Chicago
    {
        'min_lat': 41.5, 'max_lat': 42.0,
        'min_lon': -88.0, 'max_lon': -87.5
    },  # Greater Chicago area
    {
        'min_lat': 41.8, 'max_lat': 41.9,
        'min_lon': -87.7, 'max_lon': -87.6
    },  # Downtown Chicago
    {
        'min_lat': 41.9, 'max_lat': 42.0,
        'min_lon': -87.7, 'max_lon': -87.6
    },  # North Side Chicago
    {
        'min_lat': 41.8, 'max_lat': 41.9,
        'min_lon': -87.6, 'max_lon': -87.5
    },  # West Side Chicago
    {
        'min_lat': 41.7, 'max_lat': 41.8,
        'min_lon': -87.7, 'max_lon': -87.6
    },  # South Side Chicago

    # Los Angeles
    {
        'min_lat': 33.5, 'max_lat': 34.5,
        'min_lon': -118.5, 'max_lon': -118.0
    },  # Greater Los Angeles area
    {
        'min_lat': 34.0, 'max_lat': 34.1,
        'min_lon': -118.3, 'max_lon': -118.2
    },  # Downtown Los Angeles
    {
        'min_lat': 34.1, 'max_lat': 34.2,
        'min_lon': -118.4, 'max_lon': -118.3
    },  # Hollywood
    {
        'min_lat': 34.0, 'max_lat': 34.1,
        'min_lon': -118.5, 'max_lon': -118.4
    },  # Santa Monica
    {
        'min_lat': 33.9, 'max_lat': 34.0,
        'min_lon': -118.3, 'max_lon': -118.2
    },  # South Los Angeles

    # Houston
    {
        'min_lat': 29.45, 'max_lat': 30.0,
        'min_lon': -95.75, 'max_lon': -95.25
    },  # Greater Houston area
    {
        'min_lat': 29.7, 'max_lat': 29.8,
        'min_lon': -95.4, 'max_lon': -95.3
    },  # Downtown Houston
    {
        'min_lat': 29.8, 'max_lat': 29.9,
        'min_lon': -95.4, 'max_lon': -95.3
    },  # North Houston
    {
        'min_lat': 29.7, 'max_lat': 29.8,
        'min_lon': -95.5, 'max_lon': -95.4
    },  # West Houston
    {
        'min_lat': 29.6, 'max_lat': 29.7,
        'min_lon': -95.4, 'max_lon': -95.3
    },  # South Houston

    # Phoenix
    {
        'min_lat': 33.0, 'max_lat': 34.0,
        'min_lon': -112.5, 'max_lon': -111.5
    },  # Greater Phoenix area
    {
        'min_lat': 33.4, 'max_lat': 33.5,
        'min_lon': -112.1, 'max_lon': -112.0
    },  # Downtown Phoenix
    {
        'min_lat': 33.5, 'max_lat': 33.6,
        'min_lon': -112.1, 'max_lon': -112.0
    },  # North Phoenix
    {
        'min_lat': 33.4, 'max_lat': 33.5,
        'min_lon': -112.2, 'max_lon': -112.1
    },  # West Phoenix
    {
        'min_lat': 33.3, 'max_lat': 33.4,
        'min_lon': -112.1, 'max_lon': -112.0
    },  # South Phoenix

    # Seattle
    {
        'min_lat': 47.0, 'max_lat': 48.0,
        'min_lon': -122.75, 'max_lon': -121.5
    },  # Greater Seattle area
    {
        'min_lat': 47.6, 'max_lat': 47.7,
        'min_lon': -122.4, 'max_lon': -122.3
    },  # Downtown Seattle
    {
        'min_lat': 47.7, 'max_lat': 47.8,
        'min_lon': -122.4, 'max_lon': -122.3
    },  # North Seattle
    {
        'min_lat': 47.6, 'max_lat': 47.7,
        'min_lon': -122.5, 'max_lon': -122.4
    },  # West Seattle
    {
        'min_lat': 47.5, 'max_lat': 47.6,
        'min_lon': -122.4, 'max_lon': -122.3
    },  # South Seattle
]

temporal_query_params = [
    {
        'start_time': '2099-01-01T00:00:00Z',
        'end_time': '2099-03-31T23:59:59Z'
    },  # Full three-month range
    {
        'start_time': '2099-01-01T00:00:00Z',
        'end_time': '2099-01-31T23:59:59Z'
    },  # Full month of January
    {
        'start_time': '2099-02-01T00:00:00Z',
        'end_time': '2099-02-28T23:59:59Z'
    },  # Full month of February
    {
        'start_time': '2099-03-01T00:00:00Z',
        'end_time': '2099-03-31T23:59:59Z'
    },  # Full month of March
    {
        'start_time': '2099-01-01T00:00:00Z',
        'end_time': '2099-01-15T23:59:59Z'
    },  # First half of January
    {
        'start_time': '2099-01-16T00:00:00Z',
        'end_time': '2099-01-31T23:59:59Z'
    },  # Second half of January
    {
        'start_time': '2099-02-01T00:00:00Z',
        'end_time': '2099-02-14T23:59:59Z'
    },  # First half of February
    {
        'start_time': '2099-02-15T00:00:00Z',
        'end_time': '2099-02-28T23:59:59Z'
    },  # Second half of February
    {
        'start_time': '2099-03-01T00:00:00Z',
        'end_time': '2099-03-15T23:59:59Z'
    },  # First half of March
    {
        'start_time': '2099-03-16T00:00:00Z',
        'end_time': '2099-03-31T23:59:59Z'
    },  # Second half of March
    {
        'start_time': '2099-01-01T00:00:00Z',
        'end_time': '2099-01-07T23:59:59Z'
    },  # First week of January
    {
        'start_time': '2099-02-01T00:00:00Z',
        'end_time': '2099-02-07T23:59:59Z'
    },  # First week of February
    {
        'start_time': '2099-03-01T00:00:00Z',
        'end_time': '2099-03-07T23:59:59Z'
    },  # First week of March
]
