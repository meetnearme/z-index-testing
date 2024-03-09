import os
import sys
from python_src.src.visualizations.visualizations import Visualizer
from python_src.src.benchmarks.reporting import generate_report, aggregate_metrics

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if __name__ == "__main__":
    # Instantiate the visualizer
    visualizer = Visualizer()

    # Load the metrics from files
    metric_files = [
        os.path.join('python_src', 'src', 'benchmarks', 'metrics_results', 'z_order_point.csv'),
        os.path.join('python_src', 'src', 'benchmarks', 'metrics_results', 'z_order_range.csv'),
    ]

    visualizer.load_metrics(metric_files)

    # Generate and export the visualizations
    visualizer.plot_latency()
    visualizer.plot_read_capacity()
    visualizer.plot_item_count()
    visualizer.plot_scanned_items()
    visualizer.plot_all()
    visualizer.export_plots('benchmark_results')

    # prepare the indexing schemes list for point
    indexing_schemes = [
            {'name': 'Z-Order Index Point', 'metrics': aggregate_metrics(visualizer.metrics['z_order_point'])},
    ]

    # Generate report
    generate_report(indexing_schemes, 'point')

    # prepare the indexing schemes list for range
    indexing_schemes = [
            {'name': 'Z-Order Index Range', 'metrics': aggregate_metrics(visualizer.metrics['z_order_range'])},
    ]

    generate_report(indexing_schemes, 'range')
