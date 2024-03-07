import time
from datetime import datetime, timedelta

import boto3
import botocore
from boto3.dynamodb.conditions import Key, Attr
from botocore.config import Config

from ..indexing.z_order import calculate_z_order_index

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

    # Query on partition-key and Z-order index range
    start_time_bench = time.time()
    try:
        response = table.query(
            KeyConditionExpression=Key('EventType').eq('MeetNearMeEvent') &
            Key('ZOrderIndex').between(min_index.encode(), max_index.encode())
        )
    except botocore.exceptions.ClientError as e:
        # Handle any DynamoDB-related exceptions
        print(f"DynamoDB query failed: {e}")
        return [], {
            'read_capacity_units': 0,
            'write_capacity_units': 0,
            'throttled_requests': 0,
            'conditional_check_failed': 0,
            'item_size_bytes': 0,
                'latency': 0,
                'item_count': 0,
                'timestamp': time.time()
            }
        end_time_bench = time.time()
        metrics = {
            'read_capacity_units': response['ConsumedCapacity']['CapacityUnits'],
            'write_capacity_units': 0,
            'throttled_requests': response['ConsumedCapacity'].get('ThrottledRequests', 0),
            'conditional_check_failed': response.get('ConditionalCheckFailedCount', 0),
            'item_size_bytes': sum(len(item.encode('utf-8')) for item in response['Items']),
            'latency': end_time_bench - start_time_bench,
            'item_count': len(response['Items']),
            'timestamp': time.time()
        }
        return response['Items'], metrics


def query_range(min_lat, max_lat, min_lon, max_lon):
    """
    Query events within a bounding box defined by minimum and maximum latitude and longitude.
    """
    # Calculate min and max bounds for Z-order index
    start_time = datetime(2024, 6, 1, 12, 0, 0)
    epsilon = 0.01
    min_index = calculate_z_order_index(start_time, min_lon - epsilon, min_lat - epsilon)
    max_index = calculate_z_order_index(start_time, max_lon + epsilon, max_lat + epsilon)

    # Query on Z-order index range and partition key of EventType
    start_time_bench = time.time()
    try:
        response = table.query(
            KeyConditionExpression=Key('EventType').eq('MeetNearMeEvent') &
            Key('ZOrderIndex').between(min_index.encode(), max_index.encode())
        )
    except botocore.exceptions.ClientError as e:
        # Handle any DynamoDB-related exceptions
        print(f"DynamoDB query failed: {e}")
        return [], {
            'read_capacity_units': 0,
            'write_capacity_units': 0,
            'throttled_requests': 0,
            'conditional_check_failed': 0,
            'item_size_bytes': 0,
            'latency': 0,
            'item_count': 0,
            'timestamp': time.time()
        }
    end_time_bench = time.time()
    metrics = {
        'read_capacity_units': response['ConsumedCapacity']['CapacityUnits'],
        'write_capacity_units': 0,
        'throttled_requests': response['ConsumedCapacity'].get('ThrottledRequests', 0),
        'conditional_check_failed': response.get('ConditionalCheckFailedCount', 0),
        'item_size_bytes': sum(len(item.encode('utf-8')) for item in response['Items']),
        'latency': end_time_bench - start_time_bench,
        'item_count': len(response['Items']),
        'timestamp': time.time()
    }
    return response['Items'], metrics
