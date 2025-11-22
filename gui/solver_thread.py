

import time
import traceback
from PyQt5.QtCore import QThread, pyqtSignal

# Import các thuật toán
from algorithms.hill_climbing_tsp import HillClimbingSolver
from algorithms.pso_tsp import PSOSolver
from models.tour import Tour

class SolverThread(QThread):
    """
    Luồng xử lý chạy thuật toán trong nền.
    Đã cập nhật tính năng: Tự động xoay Tour về điểm xuất phát người dùng chọn.
    """
    
    # Tín hiệu gửi kết quả về GUI
    result_signal = pyqtSignal(object, list, list, float)
    log_signal = pyqtSignal(str)

    def __init__(self, algo_name, params, cities, distance_matrix):
        super().__init__()
        self.algo_name = algo_name
        self.params = params
        self.cities = cities
        self.distance_matrix = distance_matrix

    def run(self):
        self.log_signal.emit(f"[THREAD] Đang khởi tạo {self.algo_name}...")
        
        start_time = time.perf_counter()
        best_tour = None
        history = []
        solution_log = []
        
        try:
            # 1. CHẠY THUẬT TOÁN 
            
            if "Hill" in self.algo_name:
                solver = HillClimbingSolver(self.cities, self.distance_matrix)
                
                method = self.params.get('initial_method', 'random')
                seed = self.params.get('seed', 42)
                no_improve = self.params.get('max_no_improve', 100)
                start_city_id = self.params.get('start_city_id', None)
                
                best_tour, history, solution_log, _ = solver.run(
                    initial_method=method, 
                    start_city_id=start_city_id,
                    seed=seed, 
                    max_no_improve=no_improve
                )

            elif "PSO" in self.algo_name:
                swarm_size = self.params.get('swarm_size', 30)
                iterations = self.params.get('num_iterations', 100)
                w = self.params.get('w', 0.7)
                c1 = self.params.get('c1', 1.5)
                c2 = self.params.get('c2', 1.5)
                
                solver = PSOSolver(self.cities, self.distance_matrix, 
                                   swarm_size, iterations, w, c1, c2)
                
                best_tour, best_dist, history = solver.solve()

                solution_log = []
                if history:
                    current_best = history[0]
                    solution_log.append((0, current_best, "Khởi tạo bầy đàn"))
                    for i, dist in enumerate(history):
                        if dist < current_best:
                            current_best = dist
                            solution_log.append((i, dist, "Cập nhật gBest mới"))

            user_start_id = self.params.get('start_city_id')
            
            
            if best_tour and user_start_id is not None:
                cities_list = best_tour.cities
                # Tìm vị trí của thành phố xuất phát trong danh sách kết quả
                start_index = -1
                for i, city in enumerate(cities_list):
                    if city.id == user_start_id:
                        start_index = i
                        break
                
                if start_index != -1:
                    # Xoay danh sách: Cắt từ start_index đến cuối + từ đầu đến start_index
                    rotated_cities = cities_list[start_index:] + cities_list[:start_index]
                    best_tour.cities = rotated_cities
                    # self.log_signal.emit(f"ℹ️ Đã điều chỉnh lộ trình bắt đầu từ: {rotated_cities[0].name}")

            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            
            self.result_signal.emit(best_tour, history, solution_log, elapsed_time)
            
        except Exception as e:
            error_msg = f"LỖI THUẬT TOÁN: {str(e)}"
            self.log_signal.emit(error_msg)
            print(traceback.format_exc())