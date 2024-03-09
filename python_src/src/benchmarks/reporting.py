import os 
import datetime

import pandas as pd
import matplotlib.pyplot as plt

def aggregate_metrics(metrics):
    """
    Aggregate metrics across multiple benchmark runs.
    """
    df = pd.DataFrame(metrics)
    aggregated = {
       'avg_latency': df['latency'].mean(),
       'total_read_capacity': df['read_capacity_units'].sum(),
       'total_write_capacity': df['write_capacity_units'].sum(),
       'total_conditional_check_failed': df['conditional_check_failed'].sum(),
       'total_item_size_bytes': df['item_size_bytes'].sum(),
       'total_items': df['item_count'].sum(),
       'total_scanned_count': df['scanned_count'].sum(),
    }
    return aggregated

def generate_report(indexing_schemes, query_type):
    """
    Generate a benchmark report based on aggregated metrics.
    """
    num_schemes = len(indexing_schemes)
    num_rows = 2 
    num_cols = 3


    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    report_filename = f'{timestamp}_{query_type}_benchmark_report.png'
    os.makedirs('benchmark_reports', exist_ok=True)

    # create visulaizations, charts and tables to present the results
    plt.figure(figsize=(16,8))

    # latency, read capacity, write capacity, etc
    plt.subplot(num_rows, num_cols, 1)
    metric_values = [scheme['metrics']['avg_latency'] for scheme in indexing_schemes]
    plt.bar(range(num_schemes), metric_values, tick_label=[scheme['name'] for scheme in indexing_schemes])
    plt.title('Average Latency')
    plt.xlabel('Indexing Scheme')
    plt.ylabel('Average Latency (seconds)')

     # Read Capacity Units
    plt.subplot(num_rows, num_cols, 2)
    metric_values = [scheme['metrics']['total_read_capacity'] for scheme in indexing_schemes]
    plt.bar(range(num_schemes), metric_values, tick_label=[scheme['name'] for scheme in indexing_schemes])
    plt.title('Total Read Capacity Units')
    plt.xlabel('Indexing Scheme')
    plt.ylabel('Total Read Capacity Units')

    # Write Capacity Units
    plt.subplot(num_rows, num_cols, 3)
    metric_values = [scheme['metrics']['total_write_capacity'] for scheme in indexing_schemes]
    plt.bar(range(num_schemes), metric_values, tick_label=[scheme['name'] for scheme in indexing_schemes])
    plt.title('Total Write Capacity Units')
    plt.xlabel('Indexing Scheme')
    plt.ylabel('Total Write Capacity Units')

    # Scanned Count Comparison
    plt.subplot(num_rows, num_cols, 4)
    metric_values = [scheme['metrics']['total_scanned_count'] for scheme in indexing_schemes]
    plt.bar(range(num_schemes), metric_values, tick_label=[scheme['name'] for scheme in indexing_schemes])
    plt.title(f'Scanned Count Comparison ({query_type})')
    plt.xlabel('Indexing Scheme')
    plt.ylabel('Total Scanned Count')

    # Total Items
    plt.subplot(num_rows, num_cols, 5)
    metric_values = [scheme['metrics']['total_items'] for scheme in indexing_schemes]
    plt.bar(range(num_schemes), metric_values, tick_label=[scheme['name'] for scheme in indexing_schemes])
    plt.title('Total Items')
    plt.xlabel('Indexing Scheme')
    plt.ylabel('Total Items')

    plt.tight_layout()
    plt.savefig(f'benchmark_reports/{report_filename}')
