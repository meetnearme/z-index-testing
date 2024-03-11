import time
from datetime import datetime, timedelta, time

import pytz
import boto3
import botocore
from boto3.dynamodb.conditions import Key, Attr
from botocore.config import Config

from ..benchmarks.metrics import extract_metrics
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


def query_point(lon, lat, start_time, end_time):
    """
    Query events near a specific longitude and latitude.
    """

    # Set the start date to midnight and the end date to 23:59:59
    start_date = datetime.combine(start_time.date(), time.min).replace(tzinfo=pytz.UTC)
    end_date = (datetime.combine(end_time.date(), time.max).replace(microsecond=999999) - timedelta(seconds=0.000001)).replace(tzinfo=pytz.UTC)

    # Calculate min and max bounds for Z-order index
    epsilon = 0.00001
    min_index = calculate_z_order_index(start_date, lon - 0.0001 - epsilon, lat - 0.0001 - epsilon, 'min')
    max_index = calculate_z_order_index(end_date, lon + 0.0001 + epsilon, lat + 0.0001 + epsilon, 'max')

    start_time_bench = time.time()
    try:
        response = table.query(
            KeyConditionExpression=Key('EventType').eq('MeetNearMeEvent') &
            Key('ZOrderIndex').between(min_index.encode(), max_index.encode())
        )
        metrics = extract_metrics(response, start_time_bench)
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


def query_range(min_lat, max_lat, min_lon, max_lon, start_time, end_time):
    """
    Query events within a bounding box defined by minimum and maximum latitude and longitude.
    """
    # Set the start date to midnight and the end date to 23:59:59
    start_date = datetime.combine(start_time.date(), time.min).replace(tzinfo=pytz.UTC)
    end_date = (datetime.combine(end_time.date(), time.max).replace(microsecond=999999) - timedelta(seconds=0.000001)).replace(tzinfo=pytz.UTC)

    # Calculate min and max bounds for Z-order index
    epsilon = 0.00001
    min_index = calculate_z_order_index(start_date, min_lon - 0.0001 - epsilon, min_lat - 0.0001 - epsilon, 'min')
    max_index = calculate_z_order_index(end_date, max_lon + 0.0001 + epsilon, max_lat + 0.0001 + epsilon, 'max')

    # Query on Z-order index range and partition key of EventType
    start_time_bench = time.time()
    try:
        response = table.query(
            KeyConditionExpression=Key('EventType').eq('MeetNearMeEvent') &
            Key('ZOrderIndex').between(min_index.encode(), max_index.encode())
        )
        metrics = extract_metrics(response, start_time_bench)
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
