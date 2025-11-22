# File: comparison/performance_analyzer.py

import time
import numpy as np
from typing import List, Dict, Any

from models.city import City
from utils.distance_matrix import DistanceMatrix
from algorithms.hill_climbing_tsp import HillClimbingSolver
from algorithms.pso_tsp import PSOSolver

class PerformanceAnalyzer:
    """
    Lớp chịu trách nhiệm chạy các thuật toán nhiều lần 
    để thu thập dữ liệu thống kê về hiệu năng.
    """
    
    def __init__(self, cities: List[City], distance_matrix: DistanceMatrix):
        self.cities = cities
        self.distance_matrix = distance_matrix
        self.results: Dict[str, Dict[str, List]] = {
            "Hill Climbing": {"distances": [], "times": []},
            "PSO": {"distances": [], "times": []}
        }

    def run_analysis(self, hc_params: dict, pso_params: dict, num_runs: int = 5):
        """
        Chạy so sánh.
        num_runs: Số lần chạy (Mặc định là 5 cho nhanh, bạn có thể đổi)
        """
        self.results = { "Hill Climbing": {"distances": [], "times": []},
                         "PSO": {"distances": [], "times": []} }
        
        print(f"Bắt đầu phân tích so sánh ({num_runs} lần chạy)...")
        
        for i in range(num_runs):
            # --- Chạy Hill Climbing ---
            hc_solver = HillClimbingSolver(self.cities, self.distance_matrix)
            start_time_hc = time.perf_counter()
            
            # [SỬA LỖI TẠI ĐÂY]: Nhận 4 giá trị trả về (tour, history, log, time)
            # Chúng ta dùng dấu _ để bỏ qua những thứ không cần thiết cho thống kê
            best_tour_hc, _, _, _ = hc_solver.run(**hc_params)
            
            time_hc = time.perf_counter() - start_time_hc
            
            if best_tour_hc:
                self.results["Hill Climbing"]["distances"].append(best_tour_hc.distance)
                self.results["Hill Climbing"]["times"].append(time_hc)

            # --- Chạy PSO ---
            pso_solver = PSOSolver(self.cities, self.distance_matrix, **pso_params)
            start_time_pso = time.perf_counter()
            
            # PSO trả về 3 giá trị (tour, distance, history)
            best_tour_pso, best_dist_pso, _ = pso_solver.solve()
            
            time_pso = time.perf_counter() - start_time_pso
            
            if best_tour_pso:
                self.results["PSO"]["distances"].append(best_dist_pso)
                self.results["PSO"]["times"].append(time_pso)
        
        print("Phân tích so sánh hoàn tất.")

    def get_statistics(self) -> Dict[str, Dict[str, float]]:
        stats = {}
        for algo_name, data in self.results.items():
            if not data["distances"]:
                continue
            
            stats[algo_name] = {
                "distance": float(np.mean(data["distances"])),
                "best_distance": float(np.min(data["distances"])),
                "worst_distance": float(np.max(data["distances"])),
                "std_dev_distance": float(np.std(data["distances"])),
                "time": float(np.mean(data["times"]))
            }
        return stats