import pytest
from .benchmarks import BenchmarkBase
from src.queries import query_point, query_range
from src.indexing.z_order import calculate_z_order_index
from .query_params import point_query_params, range_query_params


class BenchmarkZOrder(BenchmarkBase):
    def setup_method(self):
        super().setup_method('EventsTableZOrder')

    def teardown_method(self):
        super().teardown_method()

    @pytest.mark.benchmark(group='z_order')
    def benchmark_query_point(self, benchmark):
        for params in point_query_params:
            result = benchmark(query_point, params['lon'], params['lat'])

    @pytest.mark.benchmark(group='z_order')
    def benchmark_query_range(self, benchmark):
        for params in range_query_params:
            result = benchmark(query_range, params['min_lat'], params['max_lat'], params['min_lon'], params['max_lon'])
