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

    start_time_bench = time.time()
    try:
        response = table.query(
            KeyConditionExpression=Key('EventType').eq('MeetNearMeEvent') &
            Key('ZOrderIndex').between(min_index.encode(), max_index.encode())
        )
        end_time_bench = time.time()
        metrics = {
            'start_time': start_time_bench,
            'end_time': end_time_bench,
            'read_capacity_units': response.get('ConsumedCapacity', {}).get('CapacityUnits', 0),
            'write_capacity_units': 0,
            'conditional_check_failed': response.get('ConditionalCheckFailedCount', 0),
            'item_size_bytes': sum(len(str(item).encode('utf-8')) for item in response.get('Items', [])),
            'latency': time.time() - start_time_bench,
            'item_count': len(response.get('Items', [])),
            'timestamp': time.time()
        }
        return response.get('Items', []), metrics
    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            print(f"Table does not exist: {e}")
        elif error_code == 'AccessDeniedException':
            print(f"Access denied to the table: {e}")
        else:
            print(f"Unexpected error occurred: {e}")
        return [], {
            'read_capacity_units': 0,
            'write_capacity_units': 0,
            'conditional_check_failed': 0,
            'item_size_bytes': 0,
            'latency': 0,
            'item_count': 0,
            'timestamp': time.time()
        }
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return [], {
            'read_capacity_units': 0,
            'write_capacity_units': 0,
            'conditional_check_failed': 0,
            'item_size_bytes': 0,
            'latency': 0,
            'item_count': 0,
            'timestamp': time.time()
        }


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
        end_time_bench = time.time()
        metrics = {
            'start_time': start_time_bench,
            'end_time': end_time_bench,
            'read_capacity_units': response.get('ConsumedCapacity', {}).get('CapacityUnits', 0),
            'write_capacity_units': 0,
            'conditional_check_failed': response.get('ConditionalCheckFailedCount', 0),
            'item_size_bytes': sum(len(str(item).encode('utf-8')) for item in response.get('Items', [])),
            'latency': time.time() - start_time_bench,
            'item_count': len(response.get('Items', [])),
            'timestamp': time.time()
        }
        return response.get('Items', []), metrics
    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            print(f"Table does not exist: {e}")
        elif error_code == 'AccessDeniedException':
            print(f"Access denied to the table: {e}")
        else:
            print(f"Unexpected error occurred: {e}")
        return [], {
            'read_capacity_units': 0,
            'write_capacity_units': 0,
            'conditional_check_failed': 0,
            'item_size_bytes': 0,
            'latency': 0,
            'item_count': 0,
            'timestamp': time.time()
        }
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return [], {
            'read_capacity_units': 0,
            'write_capacity_units': 0,
            'conditional_check_failed': 0,
            'item_size_bytes': 0,
            'latency': 0,
            'item_count': 0,
            'timestamp': time.time()
        }
