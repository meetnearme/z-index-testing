import json
import time
import os
import csv

from datetime import datetime

class MetricsCollector:
    def __init__(self):
        self.metrics = []

    def capture_metrics(self, result, metrics, start_time, end_time):
        print(f"Result in the capture metrics: {metrics}")
        metric = {
            'read_capacity_units': metrics.get('CapacityUnits', 0),
            'write_capacity_units': metrics.get('CapacityUnits', 0),
            'conditional_check_failed': metrics.get('ConditionalCheckFailedCount', 0),
            'item_size_bytes': sum(len(str(item).encode('utf-8')) for item in result),
            'latency': end_time - start_time,
            'item_count': len(result),
            'timestamp': time.time()
        }
        self.metrics.append(metric)

    def store_metrics(self, file_name):
        directory = 'src/benchmarks/metrics_result'
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, file_name)
        with open(file_path, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=self.metrics[0].keys())
            writer.writeheader()
            writer.writerows(self.metrics)
