import json
import time

from datetime import datetime

class MetricsCollector:
    def __init__(self):
        self.metrics = []

    def capture_metrics(self, result, start_time, end_time):
        metric = {
            'read_capacity_units': result['ConsumedCapacity']['CapacityUnits'],
            'write_capacity_units': result.get('ConsumedCapacity', {}).get('CapacityUnits', 0),
            'throttled_requests': result['ConsumedCapacity'].get('ThrottledRequests', 0),
            'conditional_check_failed': result.get('ConditionalCheckFailedCount', 0),
            'item_size_bytes': sum(len(item.encode('utf-8')) for item in result['Items']),
            'latency': end_time - start_time,
            'item_count': len(result['Items']),
            'timestamp': time.time()
        }
        self.metrics.append(metric)

    def store_metrics(self, file_path):
        with open(file_path, 'w') as f:
            for metric in self.metrics:
                f.write(json.dumps(metric))
                f.write('\n')
