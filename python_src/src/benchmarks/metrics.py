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
        directory = 'src/benchmarks/metrics_results'
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, file_name)
        with open(file_path, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=self.metrics[0].keys())
            writer.writeheader()
            writer.writerows(self.metrics)


def extract_metrics(response, start_time):
    """
    Extract relevant metrics from the DynamoDB response.

    Args:
        response (dict): The response received from the DynamoDB query using boto3
        start_time (float):  The start time of the query in seconds since the epoch

    Returns:
        dict: A dictionary containing the extracted metrics.
    """
    end_time = time.time()
    metrics = {
        'start_time': start_time,
        'end_time': end_time,
        'read_capacity_units': response.get('ConsumedCapacity', {}).get('CapacityUnits', 0),
        'write_capacity_units': 0,
        'conditional_check_failed': response.get('ConditionalCheckFailedCount', 0),
        'item_size_bytes': sum(len(str(item).encode('utf-8')) for item in response.get('Items', [])),
        'latency': time.time() - start_time,
        'item_count': len(response.get('Items', [])),
        'timestamp': time.time()
    }
    return metrics


