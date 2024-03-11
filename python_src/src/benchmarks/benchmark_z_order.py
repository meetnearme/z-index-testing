import pytest
import pytz

from datetime import datetime

from .benchmarks_base import BenchmarkBase
from ..queries.z_order import query_point, query_range
from .query_params import point_query_params, range_query_params, temporal_query_params
from .reporting import aggregate_metrics, generate_report


class TestBenchmarkZOrder(BenchmarkBase):
    def setup_method(self):
        super().setup_method('EventsTableZOrder')

    def teardown_method(self):
        super().teardown_method()

    def benchmark(self, benchmark):
        return benchmark

    @pytest.mark.parametrize('params_spatial', point_query_params)
    @pytest.mark.parametrize('params_temporal', temporal_query_params)
    @pytest.mark.benchmark(group='z_order')
    def test_benchmark_query_point(self, benchmark, params_spatial, params_temporal):
        start_date = pytz.UTC.localize(datetime.fromisoformat(params_temporal['start_time']))
        end_date = pytz.UTC.localize(datetime.fromisoformat(params_temporal['end_time']))
        result, metrics = benchmark(query_point, params_spatial['lon'], params_spatial['lat'], start_date, end_date)
        start_time, end_time = metrics.get('start_time', 0), metrics.get('end_time', 0)
        self.capture_metrics(result, metrics, start_time, end_time)
        self.store_metrics('z_order_point.csv')
        self.generate_report('point')

    @pytest.mark.parametrize('params_spatial_spatial', range_query_params)
    @pytest.mark.parametrize('params_temporal', temporal_query_params)
    @pytest.mark.benchmark(group='z_order')
    def test_benchmark_query_range(self, benchmark, params_spatial, params_temporal):
        start_date = pytz.UTC.localize(datetime.fromisoformat(params_temporal['start_time']))
        end_date = pytz.UTC.localize(datetime.fromisoformat(params_temporal['end_time']))
        result, metrics = benchmark(query_range, params_spatial['min_lat'], params_spatial['max_lat'], params_spatial['min_lon'], params_spatial['max_lon'], start_date, end_date)
        start_time, end_time = metrics.get('start_time', 0), metrics.get('end_time', 0)
        self.capture_metrics(result, metrics, start_time, end_time)
        self.store_metrics('z_order_range.csv')
        self.generate_report('range')

    def generate_report(self, query_type):
        aggregated_metrics = aggregate_metrics(self.metrics_collector.metrics)
        indexing_schemes = [
                {'name': 'Z-Order Index', 'metrics': aggregated_metrics}
        ]
        generate_report(indexing_schemes, query_type)
