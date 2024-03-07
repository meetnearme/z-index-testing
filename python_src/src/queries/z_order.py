import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.config import Config
from ..indexing.z_order import calculate_z_order_index
from datetime import datetime, timedelta

db_config = Config(
    region_name='us-east-1',
    signature_version='v4',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)

# connect to Dynamodb
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url="http://localhost:8000",
    config=db_config
)

table = dynamodb.Table('EventsTableZOrder')

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


def query_point(lon, lat):
    """
    Query events near a specific longitude and latitude.
    """
    # Calculate min and max bounds for Z-order index
    start_time = datetime(2024, 6, 1, 12, 0, 0)  # Fixed start time for all events
    epsilon = 0.00001
    min_index = calculate_z_order_index(start_time, lon - 0.0001 - epsilon, lat - 0.0001 - epsilon)
    max_index = calculate_z_order_index(start_time, lon + 0.0001 + epsilon, lat + 0.0001 + epsilon)

    # Calculate min and max bounds for Z-order index
    # min_index = calculate_z_order_index(start_time, min_lon - epsilon, min_lat - epsilon)
    # max_index = calculate_z_order_index(start_time, max_lon + epsilon, max_lat + epsilon)

    # Query on partition-key and Z-order index range
    response = table.query(
        KeyConditionExpression=Key('EventType').eq('MeetNearMeEvent') &
        Key('ZOrderIndex').between(min_index.encode(), max_index.encode())
    )
    return response['Items']

def query_range(min_lat, max_lat, min_lon, max_lon):
    """
    Query events within a bounding box defined by minimum and maximum latitude and longitude.
    """
    # Calculate min and max bounds for Z-order index
    start_time = datetime(2024, 6, 1, 12, 0, 0)
    epsilon = 0.01
    min_index = calculate_z_order_index(start_time, min_lon - epsilon, min_lat - epsilon)
    max_index = calculate_z_order_index(start_time, max_lon + epsilon, max_lat + epsilon)

    # Pretty-print min_index and max_index
    # min_index_binary = bin(int(min_index, 2))[2:].zfill(96)
    # max_index_binary = bin(int(max_index, 2))[2:].zfill(96)

    # pretty_min_index = ' '.join([min_index_binary[i:i+8] for i in range(0, len(min_index_binary), 8)])
    # pretty_max_index = ' '.join([max_index_binary[i:i+8] for i in range(0, len(max_index_binary), 8)])

    # print(f"Min Index: {pretty_min_index}")
    # print(f"Max Index: {pretty_max_index}")

    # Query on Z-order index range and partition key of EventType
    response = table.query(
        KeyConditionExpression=Key('EventType').eq('MeetNearMeEvent') &
        Key('ZOrderIndex').between(min_index.encode(), max_index.encode())
    )
    return response['Items']
