import unittest
import time
import pytest

from ...src.benchmarks.metrics import extract_metrics, MetricsCollector
from unittest.mock import patch

class TestMetricsExtraction(unittest.TestCase):
    def setUp(self):
        self.mock_response = {
            'Items': [{'id': '1'}, {'id': '2'}],
            'Count': 2,
            'ScannedCount': 5,
            'ConsumedCapacity': {
                'TableName': 'MyTable',
                'CapacityUnits': 1.5,
                'ReadCapacityUnits': 1.0,
                'WriteCapacityUnits': 0.5,
                'Table': {
                    'ReadCapacityUnits': 0.8,
                    'WriteCapacityUnits': 0.4,
                    'CapacityUnits': 1.2
                }
            }
        }
        self.start_time = time.time()

    def test_extract_metrics(self):
        expected_metrics = {
            'start_time': self.start_time,
            'end_time': pytest.approx(time.time(), abs=1),
            'read_capacity_units': 1.0,
            'write_capacity_units': 0.5,
            'table_read_capacity_units': 0.8,
            'table_write_capacity_units': 0.4,
            'table_capacity_units': 1.2,
            'conditional_check_failed': 0,
            'item_size_bytes': 22,
            'scanned_count': 5,
            'latency': pytest.approx(time.time() - self.start_time, abs=1),
            'item_count': 2,
            'timestamp': pytest.approx(time.time(), abs=1)
        }
        metrics = extract_metrics(self.mock_response, self.start_time)
        self.assertDictContainsSubset(metrics, expected_metrics)

    @patch('python_src.src.benchmarks.metrics.MetricsCollector.capture_metrics')
    def test_capture_metrics(self, mock_capture_metrics):
        result = self.mock_response['Items']
        metrics = extract_metrics(self.mock_response, self.start_time)
        end_time = metrics['end_time']
        metrics_collector = MetricsCollector()
        metrics_collector.capture_metrics(result, metrics, self.start_time, end_time)
        mock_capture_metrics.assert_called_once()


if __name__ == '__main__':
    unittest.main()
