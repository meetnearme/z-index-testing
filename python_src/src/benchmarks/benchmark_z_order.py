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

    @pytest.mark.benchmark(group='z_order')
    def test_benchmark_query_point(self, benchmark):
        for params in point_query_params:
            result, metrics = benchmark(query_point, params['lon'], params['lat'])
            self.capture_metrics(result, metrics['start_time'], metrics['end_time'])
            self.store_metrics('metrics/z_order.csv')
        self.generate_report()

    @pytest.mark.benchmark(group='z_order')
    def test_benchmark_query_range(self, benchmark):
        for params in range_query_params:
            result, metrics = benchmark(query_range, params['min_lat'], params['max_lat'], params['min_lon'], params['max_lon'])
            self.capture_metrics(result, metrics['start_time'], metrics['end_time'])
            self.store_metrics('metrics/z_order.csv')
        self.generate_report()

    def generate_report(self):
        aggregated_metrics = aggregate_metrics(self.metrics_collector.metrics)
        generate_report(aggregated_metrics)
