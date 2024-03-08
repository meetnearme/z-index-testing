import os
from python_src.src.visualizations.visualizations import Visualizer

if __name__ == "__main__":
    # Instantiate the visualizer
    visualizer = Visualizer()

    # Load the metrics from files
    metric_files = [
            'metrics/z_order.csv',
    ]

    visualizer.load_metrics(metric_files)

    # Generate and export the visualizations
    visualizer.plot_latency()
    visualizer.plot_read_capacity()
    visualizer.plot_item_count()
    visualizer.plot_scanned_items()
    visualizer.plot_all()
    visualizer.export_plots('benchmark_results')


