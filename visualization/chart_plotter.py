import matplotlib.pyplot as plt
from typing import List, Dict, Any
import numpy as np


class ChartPlotter:
    """
    Lớp chịu trách nhiệm vẽ các biểu đồ phân tích hiệu năng thuật toán.
    """
    
    @staticmethod
    def plot_convergence(iterations: List[int], 
                        distances: List[float],
                        title: str = "Convergence Chart",
                        algorithm_name: str = "Algorithm") -> plt.Figure:
        """
        Vẽ biểu đồ convergence (quá trình hội tụ) của thuật toán.
        
        Args:
            iterations (List[int]): Danh sách số iteration
            distances (List[float]): Khoảng cách tương ứng
            title (str): Tiêu đề biểu đồ
            algorithm_name (str): Tên thuật toán
            
        Returns:
            plt.Figure: Figure object của matplotlib
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(iterations, distances, 
                linewidth=2, 
                color='#2E86AB',
                marker='o',
                markersize=4,
                label=algorithm_name)
        
        ax.set_xlabel('Iteration', fontsize=12, fontweight='bold')
        ax.set_ylabel('Total Distance (km)', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=10)
        
        best_idx = np.argmin(distances)
        ax.annotate(f'Best: {distances[best_idx]:.2f} km',
                   xy=(iterations[best_idx], distances[best_idx]),
                   xytext=(10, -20),
                   textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_comparison(results: Dict[str, Dict[str, Any]],
                       metric: str = "distance") -> plt.Figure:
        """
        Vẽ biểu đồ so sánh giữa các thuật toán.
        
        Args:
            results (Dict): Dictionary chứa kết quả của các thuật toán
                           Format: {
                               "Algorithm1": {"distance": 100, "time": 5.2},
                               "Algorithm2": {"distance": 95, "time": 7.1}
                           }
            metric (str): Metric cần so sánh ("distance" hoặc "time")
            
        Returns:
            plt.Figure: Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        algorithms = list(results.keys())
        values = [results[alg][metric] for alg in algorithms]
        
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E', '#BC4B51']
        
        bars = ax.bar(algorithms, values, color=colors[:len(algorithms)], alpha=0.8)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}',
                   ha='center', va='bottom', fontweight='bold')
        
        ylabel = "Total Distance (km)" if metric == "distance" else "Time (seconds)"
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.set_title(f'Algorithm Comparison - {metric.capitalize()}', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, axis='y', alpha=0.3, linestyle='--')
        
        plt.xticks(rotation=15, ha='right')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_multiple_runs(run_results: List[Dict[str, Any]],
                          algorithm_name: str = "Algorithm") -> plt.Figure:
        """
        Vẽ biểu đồ cho nhiều lần chạy của cùng một thuật toán.
        
        Args:
            run_results (List[Dict]): Danh sách kết quả các lần chạy
                                     Mỗi dict chứa: {"iterations": [...], "distances": [...]}
            algorithm_name (str): Tên thuật toán
            
        Returns:
            plt.Figure: Figure object
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        colors = plt.cm.viridis(np.linspace(0, 1, len(run_results)))
        
        for idx, result in enumerate(run_results):
            iterations = result['iterations']
            distances = result['distances']
            ax.plot(iterations, distances, 
                   linewidth=1.5, 
                   alpha=0.6,
                   color=colors[idx],
                   label=f'Run {idx+1}')
        
        ax.set_xlabel('Iteration', fontsize=12, fontweight='bold')
        ax.set_ylabel('Total Distance (km)', fontsize=12, fontweight='bold')
        ax.set_title(f'{algorithm_name} - Multiple Runs', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=8, ncol=2)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_box_plot(data: Dict[str, List[float]],
                     ylabel: str = "Distance") -> plt.Figure:
        """
        Vẽ box plot để so sánh phân phối kết quả của các thuật toán.
        
        Args:
            data (Dict): Dictionary với key là tên thuật toán, value là list kết quả
            ylabel (str): Label cho trục y
            
        Returns:
            plt.Figure: Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        algorithms = list(data.keys())
        values = [data[alg] for alg in algorithms]
        
        box_plot = ax.boxplot(values, labels=algorithms, patch_artist=True)
        
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E', '#BC4B51']
        for patch, color in zip(box_plot['boxes'], colors[:len(algorithms)]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.set_title('Algorithm Performance Distribution', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, axis='y', alpha=0.3, linestyle='--')
        
        plt.xticks(rotation=15, ha='right')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_dual_metric_comparison(results: Dict[str, Dict[str, Any]]) -> plt.Figure:
        """
        Vẽ biểu đồ so sánh 2 metric (distance và time) cùng lúc.
        
        Args:
            results (Dict): Dictionary chứa kết quả của các thuật toán
                           Format: {
                               "Algorithm1": {"distance": 100, "time": 5.2},
                               "Algorithm2": {"distance": 95, "time": 7.1}
                           }
            
        Returns:
            plt.Figure: Figure object với 2 subplots
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        algorithms = list(results.keys())
        distances = [results[alg]["distance"] for alg in algorithms]
        times = [results[alg]["time"] for alg in algorithms]
        
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E', '#BC4B51']
        
        bars1 = ax1.bar(algorithms, distances, color=colors[:len(algorithms)], alpha=0.8)
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom', fontweight='bold')
        
        ax1.set_ylabel('Total Distance (km)', fontsize=12, fontweight='bold')
        ax1.set_title('Distance Comparison', fontsize=13, fontweight='bold')
        ax1.grid(True, axis='y', alpha=0.3, linestyle='--')
        ax1.tick_params(axis='x', rotation=15)
        
        bars2 = ax2.bar(algorithms, times, color=colors[:len(algorithms)], alpha=0.8)
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.3f}',
                    ha='center', va='bottom', fontweight='bold')
        
        ax2.set_ylabel('Time (seconds)', fontsize=12, fontweight='bold')
        ax2.set_title('Time Comparison', fontsize=13, fontweight='bold')
        ax2.grid(True, axis='y', alpha=0.3, linestyle='--')
        ax2.tick_params(axis='x', rotation=15)
        
        fig.suptitle('Algorithm Performance Comparison', fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_convergence_comparison(results: Dict[str, List[float]],
                                   title: str = "Convergence Comparison") -> plt.Figure:
        """
        Vẽ biểu đồ so sánh quá trình convergence của nhiều thuật toán.
        
        Args:
            results (Dict): Dictionary với key là tên thuật toán, 
                          value là list distances theo iteration
            title (str): Tiêu đề biểu đồ
            
        Returns:
            plt.Figure: Figure object
        """
        fig, ax = plt.subplots(figsize=(12, 7))
        
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E', '#BC4B51']
        markers = ['o', 's', '^', 'D', 'v', 'p']
        
        for idx, (algorithm, distances) in enumerate(results.items()):
            iterations = list(range(len(distances)))
            ax.plot(iterations, distances,
                   linewidth=2,
                   color=colors[idx % len(colors)],
                   marker=markers[idx % len(markers)],
                   markersize=4,
                   alpha=0.7,
                   label=algorithm)
        
        ax.set_xlabel('Iteration', fontsize=12, fontweight='bold')
        ax.set_ylabel('Total Distance (km)', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=10, loc='best')
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def save_figure(fig: plt.Figure, filepath: str, dpi: int = 300):
        """
        Lưu figure ra file.
        
        Args:
            fig (plt.Figure): Figure object cần lưu
            filepath (str): Đường dẫn file (bao gồm tên và extension)
            dpi (int): Độ phân giải (dots per inch)
        """
        fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
        print(f"Biểu đồ đã được lưu tại: {filepath}")