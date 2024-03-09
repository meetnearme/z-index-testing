import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime


class Visualizer:
    def __init__(self):
        self.metrics = {}

    def load_metrics(self, metric_files):
        for file_path in metric_files:
            scheme_name = os.path.splitext(os.path.basename(file_path))[0]
            df = pd.read_csv(file_path)
            self.metrics[scheme_name] = df

    def plot_latency(self):
        fig, ax = plt.subplots()
        for scheme, df in self.metrics.items():
            ax.plot(df['latency'], label=scheme)
        ax.set_xlabel('Query Number')
        ax.set_ylabel('Latency (seconds)')
        ax.set_title('Latency Comparison')
        ax.legend()
        return fig
            


    def plot_read_capacity(self):
        fig, ax = plt.subplots()
        for scheme, df in self.metrics.items():
            ax.plot(df['read_capacity_units'], label=scheme)
        ax.set_xlabel('Query Number')
        ax.set_ylabel('Read Capacity Units')
        ax.set_title('Read Capacity Units Comparison')
        ax.legend()
        return fig


    def plot_item_count(self):
        fig, ax = plt.subplots()
        for scheme, df in self.metrics.items():
            ax.plot(df['item_count'], label=scheme)
        ax.set_xlabel('Query Number')
        ax.set_ylabel('Item Count')
        ax.set_title('Item Count Comparison')
        ax.legend()
        return fig

    def plot_all(self):
        fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(12, 12))

        axes[0].set_title('Latency Comparison')
        for scheme, df in self.metrics.items():
            axes[0].plot(df['latency'], label=scheme)
        axes[0].set_xlabel('Query Number')
        axes[0].set_ylabel('Latency (seconds)')
        axes[0].legend()

        axes[1].set_title('Read Capacity Units Comparison')
        for scheme, df in self.metrics.items():
            axes[1].plot(df['read_capacity_units'], label=scheme)
        axes[1].set_xlabel('Query Number')
        axes[1].set_ylabel('Read Capacity Units')
        axes[1].legend()

        axes[2].set_title('Item Count Comparison')
        for scheme, df in self.metrics.items():
            axes[2].plot(df['item_count'], label=scheme)
        axes[2].set_xlabel('Query Number')
        axes[2].set_ylabel('Item Count')
        axes[2].legend()

        fig.tight_layout()
        return fig


    def plot_scanned_items(self):
        fig, ax = plt.subplots()
        for scheme, df in self.metrics.items():
            ax.plot(df['scanned_count'], label=scheme)
        ax.set_xlabel('Query Number')
        ax.set_ylabel('Scanned Items')
        ax.set_title('Scanned Items Comparison')
        ax.legend()
        return fig

    def export_plots(self, query_type):
           os.makedirs('visualizations', exist_ok=True)

           timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

           latency_fig = self.plot_latency()
           latency_fig.savefig(f'visualizations/{timestamp}_{query_type}_latency.png')

           read_capacity_fig = self.plot_read_capacity()
           read_capacity_fig.savefig(f'visualizations/{timestamp}_{query_type}_read_capacity.png')

           item_count_fig = self.plot_item_count()
           item_count_fig.savefig(f'visualizations/{timestamp}_{query_type}_item_count.png')

           all_fig = self.plot_all()
           all_fig.savefig(f'visualizations/{timestamp}_{query_type}_all.png')

