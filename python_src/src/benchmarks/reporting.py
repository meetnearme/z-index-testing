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
       'total_throttled_requests': df['throttled_requests'].sum(),
       'total_conditional_check_failed': df['conditional_check_failed'].sum(),
       'total_item_size_bytes': df['item_size_bytes'].sum(),
       'total_items': df['item_count'].sum()
    }
    return aggregated

def generate_report(aggregated_metrics):
    """
    Generate a benchmark report based on aggregated metrics.
    """
    # create visulaizations, charts and tables to present the results
    plt.figure(figsize=(12,6))
    plt.bar(['Latency', 'Read Capacity', 'Write Capacity', 'Throttled Requests',
             'Conditional Check Failed', 'Item Size', 'Total Items'],
                list(aggregated_metrics.values())
            )
    plt.title('Benchmark Results')
    plt.xlabel('Metric')
    plt.ylabel('Value')
    plt.savefig('benchmark_report.png')

