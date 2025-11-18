# File: comparison/performance_analyzer.py

import time
import numpy as np
from typing import List, Dict, Any

# Import các lớp cơ sở và models
from models.city import City
from models.tour import Tour
from utils.distance_matrix import DistanceMatrix
from algorithms.base_tsp_solver import BaseTspSolver

# Import các solver cụ thể để chạy
from algorithms.hill_climbing_tsp import HillClimbingSolver
from algorithms.pso_tsp import PSOSolver

class PerformanceAnalyzer:
    """
    Lớp này chịu trách nhiệm chạy các thuật toán nhiều lần 
    để thu thập dữ liệu thống kê về hiệu năng.
    """
    
    def __init__(self, cities: List[City], distance_matrix: DistanceMatrix):
        """
        Khởi tạo Analyzer với dữ liệu bài toán.
        
        Args:
            cities (List[City]): Danh sách các đối tượng City
            distance_matrix (DistanceMatrix): Ma trận khoảng cách đã tính
        """
        self.cities = cities
        self.distance_matrix = distance_matrix
        # self.results dùng để lưu kết quả thô
        self.results: Dict[str, Dict[str, List]] = {
            "Hill Climbing": {"distances": [], "times": []},
            "PSO": {"distances": [], "times": []}
        }

    def run_analysis(self, hc_params: dict, pso_params: dict, num_runs: int = 10):
        """
        Chạy so sánh 2 thuật toán N lần.
        
        Args:
            hc_params (dict): Tham số cho Hill Climbing
            pso_params (dict): Tham số cho PSO
            num_runs (int): Số lần lặp lại bài kiểm tra.
        """
        self.results = { "Hill Climbing": {"distances": [], "times": []},
                         "PSO": {"distances": [], "times": []} }
        
        print(f"Bắt đầu phân tích so sánh ({num_runs} lần chạy)...")
        
        for i in range(num_runs):
            print(f"--- Lần chạy Phân tích {i + 1}/{num_runs} ---")
            
            # --- Chạy Hill Climbing ---
            print("Đang chạy Hill Climbing...")
            #
            hc_solver = HillClimbingSolver(self.cities, self.distance_matrix)
            start_time_hc = time.perf_counter()
            best_tour_hc, best_dist_hc, _ = hc_solver.run(**hc_params)
            time_hc = time.perf_counter() - start_time_hc
            
            if best_tour_hc:
                self.results["Hill Climbing"]["distances"].append(best_dist_hc)
                self.results["Hill Climbing"]["times"].append(time_hc)

            # --- Chạy PSO ---
            print("Đang chạy PSO...")
            #
            pso_solver = PSOSolver(self.cities, self.distance_matrix, **pso_params)
            start_time_pso = time.perf_counter()
            best_tour_pso, best_dist_pso, _ = pso_solver.solve()
            time_pso = time.perf_counter() - start_time_pso
            
            if best_tour_pso:
                self.results["PSO"]["distances"].append(best_dist_pso)
                self.results["PSO"]["times"].append(time_pso)
        
        print("Phân tích so sánh hoàn tất.")

    def get_statistics(self) -> Dict[str, Dict[str, float]]:
        """
        Tính toán các chỉ số thống kê (trung bình, tốt nhất, v.v.)
        từ kết quả thô.
        
        Returns:
            Dict: Dữ liệu đã được tổng hợp, sẵn sàng cho chart_plotter
                  Format: {"Hill Climbing": {"distance": 123, "time": 0.5}, ...}
        """
        stats = {}
        for algo_name, data in self.results.items():
            if not data["distances"]:
                print(f"Cảnh báo: {algo_name} không có kết quả.")
                continue
            
            stats[algo_name] = {
                # "distance" sẽ là giá trị trung bình
                "distance": float(np.mean(data["distances"])),
                "best_distance": float(np.min(data["distances"])),
                "worst_distance": float(np.max(data["distances"])),
                "std_dev_distance": float(np.std(data["distances"])),
                "time": float(np.mean(data["times"]))
            }
        return stats