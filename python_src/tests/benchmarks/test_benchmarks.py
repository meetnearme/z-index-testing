import pytest

# from benchmarks import BenchmarkBase
from python_src.src.benchmarks.benchmarks import BenchmarkBase


class TestBenchmarking(BenchmarkBase):
    def test_setup_method(self):
        # Test that initializes the dynamodb resource and table
        self.setup_method('EventsTable')
        # Assert that the dynamodb resource and table are initialized
        assert self.dynamodb is not None
        assert self.table is not None
        assert self.table.name == 'EventsTable'

    def test_teardown_method(self):
        # test that teardown resets the dynamodb resource and table
        self.setup_method('EventsTable')
        self.teardown_method()
        # Assert that the dynamodb resource and table are reset
        assert self.dynamodb is None
        assert self.table is None

    def test_query_point_placeholder(self):
        # Test that query_point method is callable 
        self.setup_method('EventsTable')
        lon, lat = -73.98517, 40.74921
        result = self.query_point(lon, lat)
        assert result is None

    def test_query_range_placeholder(self):
        # Test that query_range method is callable 
        self.setup_method('EventsTable')
        min_lat, max_lat = 40.5, 41.2 
        min_lon, max_lon = -74.5, -73.5
        result = self.query_range(min_lat, max_lat, min_lon, max_lon)
        assert result is None


