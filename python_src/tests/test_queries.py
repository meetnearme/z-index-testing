import unittest
import boto3
from datetime import datetime, timedelta 
from python_src.src.queries import query_point, query_range
from python_src.utils import calculate_z_order_index

class TestSpatialQueries(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime(2024, 6, 1, 12, 0, 0)
        self.end_time = self.start_time + timedelta(hours=3)

    # Test cases for query_point
    def test_query_point_existing_event(self):
        # Test querying for a point location where an event exists
        lon, lat = -73.98517, 40.74921  # Example location in New York
        min_index = calculate_z_order_index(self.start_time, lon - 0.1, lat - 0.1)
        max_index = calculate_z_order_index(self.start_time, lon + 0.1, lat + 0.1)
        events = query_point(lon, lat)
        min_index_bin = boto3.dynamodb.types.Binary(min_index.encode())
        max_index_bin = boto3.dynamodb.types.Binary(max_index.encode())

        self.assertGreater(len(events), 0)
        for event in events:
            min_index_int = int.from_bytes(min_index_bin, byteorder='big')
            max_index_int = int.from_bytes(max_index_bin, byteorder='big')
            event_index_int = int.from_bytes(event['ZOrderIndex'], byteorder='big')
            self.assertTrue(min_index_int <= event_index_int <= max_index_int)

    def test_query_point_no_event(self):
        # Test querying for a point location where no event exists
        lon, lat = -90.0, 45.0  # Example location with no events
        events = query_point(lon, lat)
        self.assertEqual(len(events), 0)

    # Test cases for query_range
    def test_query_range_existing_events(self):
        # Test querying for a bounding box where events exist
        min_lat, max_lat = 40.5, 41.2
        min_lon, max_lon =  -73.5, -74.5  # Example bounding box around New York
        min_index = calculate_z_order_index(self.start_time, min_lon, min_lat)
        max_index = calculate_z_order_index(self.start_time, max_lon, max_lat)
        min_index_bin = boto3.dynamodb.types.Binary(min_index.encode())
        max_index_bin = boto3.dynamodb.types.Binary(max_index.encode())
        events = query_range(min_lat, max_lat, min_lon, max_lon)
        self.assertGreater(len(events), 0)
        for event in events:
            min_index_int = int.from_bytes(min_index_bin, byteorder='big')
            max_index_int = int.from_bytes(max_index_bin, byteorder='big')
            event_index_int = int.from_bytes(event['ZOrderIndex'], byteorder='big')
            self.assertTrue(min_index_int <= event_index_int <= max_index_int)

    def test_query_range_no_events(self):
        # Test querying for a bounding box where no events exist
        min_lat, max_lat = 35.0, 36.0
        min_lon, max_lon =  -89.0, -90.0  # Example bounding box with no events
        events = query_range(min_lat, max_lat, min_lon, max_lon)
        self.assertEqual(len(events), 0)
