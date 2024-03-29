import unittest
import boto3
import uuid
import pytz
from decimal import Decimal
from datetime import datetime, timedelta
from ..src.queries.z_order import query_point, query_range
from ..src.indexing.z_order import calculate_z_order_index
from botocore.config import Config

db_config = Config(
    region_name='us-east-1',
    signature_version='v4',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)

class TestSpatialQueriesZOrder(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime(2099, 1, 1, tzinfo=pytz.UTC)
        self.end_time = self.start_time + timedelta(days=90)
        self.dynamodb = boto3.resource(
                'dynamodb', 
                endpoint_url="http://localhost:8000",
                config=db_config
                )
        self.table = self.dynamodb.Table('EventsTableZOrder')

    # Test cases for query_point
    def test_query_point_existing_event(self):
        # Test querying for a point location where an event exists
        lon, lat = -73.98517, 40.74921  # Example location in New York
        min_index = calculate_z_order_index(self.start_time, lon - 0.5, lat - 0.5, 'min')
        max_index = calculate_z_order_index(self.end_time, lon + 0.5, lat + 0.5, 'max')

        duration = 3
        end = self.start_time + timedelta(hours=duration)

        # Insert a record at the specified latitude and longitude 
        lon_dec = Decimal(str(lon))
        lat_dec = Decimal(str(lat))

        event_uuid = str(uuid.uuid4())
        z_order_index = calculate_z_order_index(self.start_time, lon, lat, 'actual')
        self.table.put_item(
            Item={
                'EventType': 'MeetNearMeEvent',
                'ZOrderIndex': z_order_index.encode(),
                'UUID': event_uuid,
                'Longitude': lon_dec,
                'Latitude': lat_dec,
                'Name': 'Test event query point existing',
                'Description': "test test",
                'StartTime': self.start_time.isoformat(),
                'EndTime': end.isoformat(),
                'City': 'New York'
            }
        )

        inserted_item = self.table.get_item(
                Key={'EventType': 'MeetNearMeEvent', 'ZOrderIndex': z_order_index.encode()}
        )['Item']

        print("Inserted Item", inserted_item)

        events, _ = query_point(lon, lat, self.start_time, self.end_time)
        min_index_bin = min_index.encode()
        max_index_bin = max_index.encode()

        self.assertGreater(len(events), 0)
        for event in events:
            event_index_bin = event['ZOrderIndex'].value
            self.assertTrue(min_index_bin <= event_index_bin <= max_index_bin)

    def test_query_point_no_event(self):
        # Test querying for a point location where no event exists
        lon, lat = -90.0, 45.0  # Example location with no events
        events, _ = query_point(lon, lat, self.start_time, self.end_time)
        self.assertEqual(len(events), 0)

    # Test cases for query_range
    def test_query_range_existing_events(self):
        # Test querying for a bounding box where events exist
        min_lat, max_lat = 40.5, 41.2
        min_lon, max_lon = -74.5, -73.5  # Example bounding box around New York
        min_index = calculate_z_order_index(self.start_time, min_lon, min_lat, 'min')
        max_index = calculate_z_order_index(self.start_time, max_lon, max_lat, 'max')
        min_index_bin = boto3.dynamodb.types.Binary(min_index.encode())
        max_index_bin = boto3.dynamodb.types.Binary(max_index.encode())
        events, _ = query_range(min_lat, max_lat, min_lon, max_lon, self.start_time, self.end_time)
        self.assertGreater(len(events), 0)
        for event in events:
            min_index_int = int.from_bytes(min_index_bin, byteorder='big')
            max_index_int = int.from_bytes(max_index_bin, byteorder='big')
            event_index_int = int.from_bytes(event['ZOrderIndex'], byteorder='big')
            self.assertTrue(min_index_int <= event_index_int <= max_index_int)

    def test_query_range_no_events(self):
        # Test querying for a bounding box where no events exist
        min_lat, max_lat = 35.0, 36.0
        min_lon, max_lon =  -90.0, -89.0,  # Example bounding box with no events
        events, _ = query_range(min_lat, max_lat, min_lon, max_lon, self.start_time, self.end_time)
        self.assertEqual(len(events), 0)

    def tearDown(self):
        self.dynamodb.meta.client.close()
