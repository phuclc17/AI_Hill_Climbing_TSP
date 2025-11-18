# File: algorithms/hill_climbing_tsp.py

import time
import random
from models.tour import Tour
from utils.tour_generator import random_tour, nearest_neighbor_tour

def two_opt_swap(cities, i, k):
    new = cities[:i] + list(reversed(cities[i:k + 1])) + cities[k + 1:]
    return new

class HillClimbingSolver:
    def __init__(self, cities, distance_matrix):
        self.cities = cities
        self.distance_matrix = distance_matrix

    def run(self, initial_method='random', start_city_id=None, seed=None, max_no_improve=100):
        """
        Cải tiến: Trả về thêm 'log_history' để in ra GUI.
        """
        if seed is not None:
            random.seed(seed)

        # 1. Tạo Tour ban đầu
        if initial_method == 'nn':
            # Tìm object city tương ứng với start_city_id
            start_node = next((c for c in self.cities if c.id == start_city_id), None)
            current_cities = nearest_neighbor_tour(self.cities, self.distance_matrix, start_node)
        else:
            current_cities = random_tour(self.cities, seed)

        current_tour = Tour(current_cities, self.distance_matrix)
        best_tour = current_tour
        
        # Danh sách lưu lịch sử để vẽ biểu đồ: [ (iteration, distance), ... ]
        history = [current_tour.distance]
        # Danh sách lưu log để in ra màn hình: [ (step, distance, path_str), ... ]
        solution_log = []

        n = len(current_tour.cities)
        no_improve = 0
        step = 0

        start_time = time.time()
        
        # Ghi lại trạng thái đầu tiên
        solution_log.append((0, current_tour.distance, str(current_tour)))

        while no_improve < max_no_improve:
            improved = False
            step += 1
            
            # Duyệt qua các lân cận (2-opt)
            for i in range(0, n - 1):
                for k in range(i + 1, n):
                    new_cities = two_opt_swap(current_tour.cities, i, k)
                    new_tour = Tour(new_cities, self.distance_matrix)
                    
                    if new_tour.distance < best_tour.distance:
                        best_tour = new_tour
                        current_tour = new_tour
                        improved = True
                        no_improve = 0
                        
                        # Lưu log khi tìm thấy đường tốt hơn
                        history.append(best_tour.distance)
                        solution_log.append((step, best_tour.distance, str(best_tour)))
                        break # First improvement
                if improved:
                    break

            if not improved:
                no_improve += 1
                history.append(best_tour.distance) # Vẫn lưu để vẽ biểu đồ dài ra

        elapsed = time.time() - start_time
        return best_tour, history, solution_log, elapsed