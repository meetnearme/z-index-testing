import pytest

from .benchmarks_base import BenchmarkBase
from ..queries.z_order import query_point, query_range
from .query_params import point_query_params, range_query_params
from .reporting import aggregate_metrics, generate_report


class TestBenchmarkZOrder(BenchmarkBase):
    def setup_method(self):
        super().setup_method('EventsTableZOrder')

    def teardown_method(self):
        super().teardown_method()

    def benchmark(self, benchmark):
        return benchmark

    @pytest.mark.parametrize('params', point_query_params)
    @pytest.mark.benchmark(group='z_order')
    def test_benchmark_query_point(self, benchmark, params):
        result, metrics = benchmark(query_point, params['lon'], params['lat'])
        start_time, end_time = metrics.get('start_time', 0), metrics.get('end_time', 0)
        self.capture_metrics(result, metrics, start_time, end_time)
        self.store_metrics('z_order_point.csv')
        self.generate_report()

    @pytest.mark.parametrize('params', range_query_params)
    @pytest.mark.benchmark(group='z_order')
    def test_benchmark_query_range(self, benchmark, params):
        result, metrics = benchmark(query_range, params['min_lat'], params['max_lat'], params['min_lon'], params['max_lon'])
        start_time, end_time = metrics.get('start_time', 0), metrics.get('end_time', 0)
        self.capture_metrics(result, metrics, start_time, end_time)
        self.store_metrics('z_order_range.csv')
        self.generate_report()

    def generate_report(self):
        aggregated_metrics = aggregate_metrics(self.metrics_collector.metrics)
        generate_report(aggregated_metrics)
